"""
Módulo de integração com APIs legislativas para busca automática de PLs
Integra com: Câmara dos Deputados, Senado Federal, Câmara Municipal SP, ALESP
"""

import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re
import time

# URLs das APIs
API_CAMARA = "https://dadosabertos.camara.leg.br/api/v2"
API_SENADO = "https://legis.senado.leg.br/dadosabertos"
API_CAMARA_SP = None  # Verificar se há API pública
API_ALESP = None  # Verificar se há API pública

# Termos para filtrar PLs relacionadas a LGBTQIA+
# TERMOS ESPECÍFICOS primeiro (mais relevantes)
TERMOS_BUSCA_ESPECIFICOS = [
    "lgbt",
    "lgbtqia",
    "lgbtqia+",
    "trans",
    "transgênero",
    "transexual",
    "travesti",
    "homofobia",
    "transfobia",
    "homossexual",
    "identidade de gênero",
    "orientação sexual",
    "diversidade sexual",
    "nome social",
    "terapia de conversão",
    "cura gay",
    "reparação sexual"
]

# TERMOS CONTEXTUAIS (podem indicar questões LGBTQIA+ em contexto legislativo)
TERMOS_BUSCA_CONTEXTUAIS = [
    "ideologia de gênero",
    "banheiro",
    "vestiário",
    "atleta trans",
    "esporte feminino",
    "competição feminina",
    "linguagem neutra",
    "todes",
    "lules",
    "símbolos religiosos.*parada",
    "menor.*evento.*lgbt",
    "comunidade lgbt"
]

TERMOS_BUSCA = TERMOS_BUSCA_ESPECIFICOS + TERMOS_BUSCA_CONTEXTUAIS

def buscar_camara_deputados(
    termos: List[str] = None,
    data_inicio: Optional[str] = None,
    data_fim: Optional[str] = None,
    sigla_tipo: str = "PL",  # PL, PLS, PEC, etc
    limite: int = 50,
    dias_atras: Optional[int] = None,  # Para compatibilidade
    ano_inicio_manual: Optional[int] = None,  # Ano explícito para buscar
    ano_fim_manual: Optional[int] = None  # Ano explícito para buscar
) -> List[Dict]:
    """
    Busca PLs na API da Câmara dos Deputados
    
    Args:
        termos: Lista de termos para buscar
        data_inicio: Data início (formato: YYYY-MM-DD)
        data_fim: Data fim (formato: YYYY-MM-DD)
        sigla_tipo: Tipo de proposição (PL, PLS, PEC, etc)
        limite: Número máximo de resultados
        dias_atras: Quantos dias atrás buscar (usa para determinar quantos anos buscar)
    
    Returns:
        Lista de PLs encontradas
    """
    if termos is None:
        termos = TERMOS_BUSCA
    
    # Determinar quantos anos buscar
    ano_atual = datetime.now().year
    
    # Priorizar anos manuais se especificados
    if ano_inicio_manual is not None and ano_fim_manual is not None:
        anos_para_buscar = [ano_inicio_manual]  # Se ambos iguais, buscar só esse ano
        if ano_inicio_manual != ano_fim_manual:
            anos_para_buscar = list(range(ano_inicio_manual, ano_fim_manual + 1))
    elif dias_atras:
        # Se especificou dias_atras, calcular quantos anos anteriores buscar
        data_limite = datetime.now() - timedelta(days=dias_atras)
        anos_para_buscar = list(range(max(2010, data_limite.year), ano_atual + 1))
    elif data_inicio:
        # Se especificou data_inicio, usar o ano dela
        try:
            ano_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").year
            anos_para_buscar = list(range(max(2010, ano_inicio), ano_atual + 1))
        except:
            anos_para_buscar = [ano_atual]
    else:
        # Padrão: ano atual
        anos_para_buscar = [ano_atual]
    
    pls_encontradas = []
    url = f"{API_CAMARA}/proposicoes"
    
    # Buscar em cada ano (do mais antigo para o mais recente)
    for ano in reversed(anos_para_buscar):
        if len(pls_encontradas) >= limite:
            break
            
        try:
            # Buscar PLs deste ano
            # API da Câmara permite até 100 itens por página
            # Para garantir que temos PLs suficientes após filtrar, buscar múltiplas páginas se necessário
            itens_por_pagina = 100
            limite_busca_por_ano = max(limite * 15, 500)  # Buscar bem mais para garantir resultados após filtro
            
            params = {
                "siglaTipo": sigla_tipo,
                "ano": ano,
                "itens": itens_por_pagina,
                "pagina": 1
            }
            
            # Buscar múltiplas páginas se necessário
            # Calcular quantas páginas precisamos buscar baseado no limite
            # Se queremos 50 PLs, precisamos buscar muito mais antes do filtro (ex: 500-1000)
            paginas_para_buscar = max(1, (limite_busca_por_ano // itens_por_pagina) + 1)
            # Limitar a 20 páginas máx (2000 PLs por ano) para não exceder rate limits
            paginas_para_buscar = min(paginas_para_buscar, 20)
            
            todas_props_ano = []
            for pagina in range(1, paginas_para_buscar + 1):
                if len(pls_encontradas) >= limite:
                    break
                
                params['pagina'] = pagina
                try:
                    response = requests.get(url, params=params, timeout=15)
                    response.raise_for_status()
                    data = response.json()
                    
                    if 'dados' in data and len(data['dados']) > 0:
                        todas_props_ano.extend(data['dados'])
                        print(f"   📥 Buscando em {ano} (página {pagina}): {len(data['dados'])} PLs encontradas")
                    else:
                        break  # Não há mais páginas
                except Exception as e:
                    print(f"   ⚠️ Erro ao buscar página {pagina} de {ano}: {e}")
                    break
            
            if todas_props_ano:
                print(f"   📊 Total em {ano}: {len(todas_props_ano)} PLs (antes do filtro)")
                
                for prop in todas_props_ano:
                    if len(pls_encontradas) >= limite:
                        break
                    
                    # Filtrar por termos na ementa
                    ementa = prop.get('ementa', '').lower()
                    
                    # Verificar termos específicos primeiro (mais confiável)
                    tem_termo_especifico = False
                    for termo in TERMOS_BUSCA_ESPECIFICOS:
                        # Para "trans", evitar falsos positivos mas ser menos restritivo
                        if termo == 'trans' and 'trans' in ementa:
                            # Aceitar "trans" se aparecer com palavras LGBTQIA+ OU sozinho em contexto legislativo
                            if re.search(r'\btrans\b', ementa) and (
                                any(palavra in ementa for palavra in ['gênero', 'sexual', 'identidade', 'lgbt', 'transfobia', 'transexual', 'transgênero']) or
                                any(palavra in ementa for palavra in ['proíbe', 'veda', 'restringe', 'garante', 'reconhece', 'criminaliza', 'direito', 'direitos'])
                            ):
                                tem_termo_especifico = True
                                break
                        elif termo.lower() in ementa:
                            tem_termo_especifico = True
                            break
                    
                    # Verificar termos contextuais com palavras-chave legislativas (mais flexível)
                    palavras_legislativas = ['proíbe', 'veda', 'restringe', 'garante', 'reconhece', 'criminaliza', 
                                            'orientação', 'identidade', 'gênero', 'sexual', 'direito', 'direitos',
                                            'dispõe', 'altera', 'estabelece', 'define']
                    tem_termo_contextual = any(
                        termo.lower() in ementa 
                        for termo in TERMOS_BUSCA_CONTEXTUAIS[:8]  # Mais termos contextuais
                    ) and any(
                        palavra in ementa for palavra in palavras_legislativas
                    )
                    
                    # Aceitar se tem termo específico OU termo contextual válido
                    if tem_termo_especifico or tem_termo_contextual:
                        # Adicionar sem buscar detalhes completos (para performance)
                        pls_encontradas.append({
                            'Nº': f"{prop.get('siglaTipo', 'PL')} {prop.get('numero', 'N/A')}/{prop.get('ano', 'N/A')}",
                            'Ano': str(prop.get('ano', 'N/A')),
                            'Casa': 'Câmara',
                            'Ementa': prop.get('ementa', 'Sem ementa'),
                            'Autores': prop.get('siglaTipo', ''),
                            'Data': prop.get('dataApresentacao', 'N/A'),
                            'Link': f"https://www.camara.leg.br/proposicoesWeb/fichadetramitacao?idProposicao={prop.get('id', '')}",
                            'Status': prop.get('statusProposicao', {}).get('descricaoSituacao', 'N/A') if prop.get('statusProposicao') else 'N/A',
                            'Fonte': 'Câmara dos Deputados'
                        })
                        
                        if len(pls_encontradas) >= limite:
                            break
            
        except requests.exceptions.HTTPError as e:
            print(f"   ⚠️ Erro ao buscar na Câmara (ano {ano}): {e.response.status_code}")
        except Exception as e:
            print(f"   ⚠️ Erro ao buscar na Câmara (ano {ano}): {e}")
    
    # Remover duplicatas
    pls_unicas = []
    ids_vistos = set()
    for pl in pls_encontradas:
        id_pl = pl['Nº']
        if id_pl not in ids_vistos:
            ids_vistos.add(id_pl)
            pls_unicas.append(pl)
    
    return pls_unicas[:limite]

def obter_detalhes_camara(id_proposicao: str) -> Optional[Dict]:
    """Obtém detalhes completos de uma proposição da Câmara"""
    try:
        url = f"{API_CAMARA}/proposicoes/{id_proposicao}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('dados', {})
    except:
        return None

def buscar_senado_federal(
    termos: List[str] = None,
    data_inicio: Optional[str] = None,
    data_fim: Optional[str] = None,
    limite: int = 50,
    ano_inicio_manual: Optional[int] = None,
    ano_fim_manual: Optional[int] = None
) -> List[Dict]:
    """
    Busca PLs no Senado Federal
    
    API: https://legis.senado.leg.br/dadosabertos
    Nota: API do Senado é mais complexa, esta é uma implementação básica que busca PLS por ano
    """
    if termos is None:
        termos = TERMOS_BUSCA
    
    # Determinar anos para buscar
    ano_atual = datetime.now().year
    if ano_inicio_manual is not None and ano_fim_manual is not None:
        anos_para_buscar = [ano_inicio_manual] if ano_inicio_manual == ano_fim_manual else list(range(ano_inicio_manual, ano_fim_manual + 1))
    else:
        anos_para_buscar = [ano_atual]
    
    pls_encontradas = []
    
    # API do Senado Federal
    # Endpoint: /dadosabertos/materia/atualizadas
    # Retorna matérias atualizadas com ementa completa
    # Estrutura: ListaMateriasAtualizadas -> Materias -> Materia[] -> DadosBasicosMateria.EmentaMateria
    # Documentação: https://legis.senado.leg.br/dadosabertos/api-docs/swagger-ui/index.html
    
    print(f"   📥 Buscando matérias atualizadas no Senado...")
    
    url_base = "https://legis.senado.leg.br/dadosabertos/materia/atualizadas"
    
    try:
        headers = {"Accept": "application/json"}
        response = requests.get(url_base, headers=headers, timeout=20)
        response.raise_for_status()
        
        data = response.json()
        
        if 'ListaMateriasAtualizadas' not in data:
            print(f"   ⚠️ Estrutura de resposta inesperada do Senado")
            return []
        
        lista = data['ListaMateriasAtualizadas']
        materias_data = lista.get('Materias', {})
        
        if isinstance(materias_data, dict) and 'Materia' in materias_data:
            materias_list = materias_data['Materia']
            materias_list = materias_list if isinstance(materias_list, list) else [materias_list]
        elif isinstance(materias_data, list):
            materias_list = materias_data
        else:
            materias_list = []
        
        if not materias_list:
            print(f"   ℹ️ Nenhuma matéria encontrada no Senado")
            return []
        
        print(f"   📊 Total de matérias atualizadas: {len(materias_list)} (antes do filtro)")
        
        # Filtrar por ano e termos LGBTQIA+
        for materia in materias_list:
            if len(pls_encontradas) >= limite:
                break
            
            # Extrair informações
            ident = materia.get('IdentificacaoMateria', {})
            dados = materia.get('DadosBasicosMateria', {})
            
            ano_materia = ident.get('AnoMateria', '')
            sigla = ident.get('SiglaSubtipoMateria', '')
            numero = ident.get('NumeroMateria', '')
            codigo = ident.get('CodigoMateria', '')
            
            # Filtrar por ano se especificado
            if ano_inicio_manual is not None and ano_fim_manual is not None:
                try:
                    ano_int = int(ano_materia) if ano_materia else 0
                    if not (ano_inicio_manual <= ano_int <= ano_fim_manual):
                        continue
                except:
                    continue
            
            # Filtrar apenas PLS (ou outras siglas de projeto de lei)
            if sigla not in ['PLS', 'PLC', 'PL']:
                continue
            
            # Obter ementa
            ementa = dados.get('EmentaMateria', '')
            if not ementa or len(ementa) < 10:
                continue
            
            ementa_lower = ementa.lower()
            
            # Filtrar por termos LGBTQIA+ (mesma lógica da Câmara)
            tem_termo_especifico = False
            for termo in TERMOS_BUSCA_ESPECIFICOS:
                if termo == 'trans' and 'trans' in ementa_lower:
                    if re.search(r'\btrans\b', ementa_lower) and (
                        any(palavra in ementa_lower for palavra in ['gênero', 'sexual', 'identidade', 'lgbt', 'transfobia', 'transexual', 'transgênero']) or
                        any(palavra in ementa_lower for palavra in ['proíbe', 'veda', 'restringe', 'garante', 'reconhece', 'criminaliza', 'direito', 'direitos'])
                    ):
                        tem_termo_especifico = True
                        break
                elif termo.lower() in ementa_lower:
                    tem_termo_especifico = True
                    break
            
            palavras_legislativas = ['proíbe', 'veda', 'restringe', 'garante', 'reconhece', 'criminaliza', 
                                    'orientação', 'identidade', 'gênero', 'sexual', 'direito', 'direitos',
                                    'dispõe', 'altera', 'estabelece', 'define']
            tem_termo_contextual = any(
                termo.lower() in ementa_lower 
                for termo in TERMOS_BUSCA_CONTEXTUAIS[:8]
            ) and any(
                palavra in ementa_lower for palavra in palavras_legislativas
            )
            
            if tem_termo_especifico or tem_termo_contextual:
                autor = 'N/A'
                if 'AutoresPrincipais' in materia:
                    autor_data = materia.get('AutoresPrincipais', {})
                    if isinstance(autor_data, dict) and 'AutorPrincipal' in autor_data:
                        autor_obj = autor_data['AutorPrincipal']
                        if isinstance(autor_obj, dict):
                            autor = autor_obj.get('NomeAutor', 'N/A')
                
                data_apresentacao = dados.get('DataApresentacao', 'N/A')
                
                link = f"https://www25.senado.leg.br/web/atividade/materias/-/materia/{codigo}" if codigo else f"https://www25.senado.leg.br/web/atividade/materias"
                
                pls_encontradas.append({
                    'Nº': f"{sigla} {numero}/{ano_materia}",
                    'Ano': str(ano_materia),
                    'Casa': 'Senado',
                    'Ementa': ementa,
                    'Autores': autor,
                    'Data': data_apresentacao,
                    'Link': link,
                    'Status': ident.get('DescricaoIdentificacaoMateria', 'N/A'),
                    'Fonte': 'Senado Federal'
                })
        
        print(f"   ✅ {len(pls_encontradas)} PLs relevantes encontradas no Senado")
        
        return pls_encontradas[:limite]
        
    except requests.exceptions.HTTPError as e:
        print(f"   ⚠️ Erro HTTP ao buscar no Senado: {e.response.status_code}")
        return []
    except Exception as e:
        print(f"   ⚠️ Erro ao buscar no Senado: {str(e)[:100]}")
        return []

def buscar_camara_sao_paulo(
    termos: List[str] = None,
    limite: int = 50
) -> List[Dict]:
    """
    Busca PLs na Câmara Municipal de São Paulo
    
    Nota: Pode não ter API pública - implementação futura via scraping
    """
    print("⚠️ Busca na Câmara Municipal de SP ainda não implementada")
    return []

def buscar_alesp(
    termos: List[str] = None,
    limite: int = 50
) -> List[Dict]:
    """
    Busca PLs na ALESP
    
    Nota: Pode não ter API pública - implementação futura via scraping
    """
    print("⚠️ Busca na ALESP ainda não implementada")
    return []

def buscar_todas_fontes(
    termos: List[str] = None,
    dias_atras: int = 90,
    limite_por_fonte: int = 20
) -> List[Dict]:
    """
    Busca PLs em todas as fontes disponíveis
    
    Args:
        termos: Termos para buscar (None = usar TERMOS_BUSCA padrão)
        dias_atras: Quantos dias atrás buscar
        limite_por_fonte: Limite por fonte
    
    Returns:
        Lista consolidada de PLs encontradas
    """
    print(f"🔍 Iniciando busca em todas as fontes (últimos {dias_atras} dias)...")
    
    todas_pls = []
    
    # 1. Câmara dos Deputados
    print("📥 Buscando na Câmara dos Deputados...")
    pls_camara = buscar_camara_deputados(
        termos=termos,
        dias_atras=dias_atras,  # Passar dias_atras para buscar múltiplos anos
        limite=limite_por_fonte
    )
    todas_pls.extend(pls_camara)
    print(f"   ✅ Encontradas {len(pls_camara)} PLs relevantes na Câmara")
    
    # 2. Senado (quando implementado)
    # pls_senado = buscar_senado(termos=termos, limite=limite_por_fonte)
    # todas_pls.extend(pls_senado)
    
    # 3. Câmara Municipal SP (quando implementado)
    # pls_camara_sp = buscar_camara_sao_paulo(termos=termos, limite=limite_por_fonte)
    # todas_pls.extend(pls_camara_sp)
    
    # 4. ALESP (quando implementado)
    # pls_alesp = buscar_alesp(termos=termos, limite=limite_por_fonte)
    # todas_pls.extend(pls_alesp)
    
    print(f"\n✅ Total encontrado: {len(todas_pls)} PLs")
    
    return todas_pls

def filtrar_pls_relevantes(pls: List[Dict], termos_minimos: int = 1) -> List[Dict]:
    """
    Filtra PLs que contêm termos mínimos relacionados a LGBTQIA+
    """
    pls_filtradas = []
    
    for pl in pls:
        ementa_lower = pl.get('Ementa', '').lower()
        
        # Contar quantos termos estão presentes
        termos_encontrados = sum(1 for termo in TERMOS_BUSCA if termo.lower() in ementa_lower)
        
        if termos_encontrados >= termos_minimos:
            pl['Termos_Encontrados'] = termos_encontrados
            pls_filtradas.append(pl)
    
    return pls_filtradas

if __name__ == "__main__":
    # Teste básico
    print("🧪 Testando busca na Câmara dos Deputados...\n")
    pls = buscar_camara_deputados(limite=5)
    
    if pls:
        print(f"\n✅ Encontradas {len(pls)} PLs:")
        for pl in pls[:3]:
            print(f"\n{pl['Nº']}")
            print(f"Ementa: {pl['Ementa'][:100]}...")
            print(f"Link: {pl['Link']}")
    else:
        print("⚠️ Nenhuma PL encontrada na busca de teste")

