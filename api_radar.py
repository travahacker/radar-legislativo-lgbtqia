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
import xml.etree.ElementTree as ET
import zipfile
from io import BytesIO

# URLs das APIs
API_CAMARA = "https://dadosabertos.camara.leg.br/api/v2"
API_SENADO = "https://legis.senado.leg.br/dadosabertos"
API_CAMARA_SP = None  # Verificar se há API pública
API_ALESP = None  # Verificar se há API pública

# Termos para filtrar PLs relacionadas a LGBTQIA+
# TERMOS ESPECÍFICOS primeiro (mais relevantes)
TERMOS_BUSCA_ESPECIFICOS = [
    # Termos básicos
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
    
    # Identidade e orientação
    "identidade de gênero",
    "orientação sexual",
    "diversidade sexual",
    "bissexual",
    "pansexual",
    "não-binário",
    "não binário",
    "cisgênero",
    
    # Direitos e procedimentos
    "nome social",
    "casamento igualitário",
    "união homoafetiva",
    "adoção homoafetiva",
    "mudança de nome",
    "retificação de registro",
    
    # Discriminação e violência
    "discriminação sexual",
    "preconceito sexual",
    "criminalização da homofobia",
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
    "comunidade lgbt",
    "sexo biológico",
    "gênero biológico",
    "família tradicional",
    "masculino e feminino"
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
    Endpoint: /materia/pesquisa/lista
    
    ✅ Este endpoint permite buscar matérias por ano de apresentação, resolvendo 
    o problema de lacunas em dados históricos.
    """
    if termos is None:
        termos = TERMOS_BUSCA
    
    # Determinar anos para buscar
    ano_atual = datetime.now().year
    if ano_inicio_manual is not None and ano_fim_manual is not None:
        anos_para_buscar = list(range(ano_inicio_manual, ano_fim_manual + 1))
    else:
        anos_para_buscar = [ano_atual]
    
    pls_encontradas = []
    
    # API do Senado Federal - endpoint /materia/pesquisa/lista
    url_base = "https://legis.senado.leg.br/dadosabertos/materia/pesquisa/lista"
    
    print(f"   📥 Buscando no Senado (anos {min(anos_para_buscar)}-{max(anos_para_buscar)})...")
    
    try:
        for ano in reversed(anos_para_buscar):
            if len(pls_encontradas) >= limite:
                break
            
            try:
                # Buscar todas as matérias apresentadas no ano especificado
                params = {'ano': str(ano)}
                
                response = requests.get(url_base, params=params, headers={'Accept': 'application/json'}, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                
                if 'PesquisaBasicaMateria' not in data:
                    print(f"   ℹ️ Resposta inesperada do Senado em {ano}")
                    continue
                
                materias_data = data['PesquisaBasicaMateria'].get('Materias', {})
                
                if isinstance(materias_data, dict) and 'Materia' in materias_data:
                    materias = materias_data['Materia']
                    materias = materias if isinstance(materias, list) else [materias]
                elif isinstance(materias_data, list):
                    materias = materias_data
                else:
                    materias = []
                
                if not materias:
                    print(f"   ℹ️ Nenhuma matéria encontrada no Senado em {ano}")
                    continue
                
                print(f"   📊 Senado {ano}: {len(materias)} matérias (antes do filtro)")
                
                # Processar cada matéria
                materias_ano = 0
                for materia in materias:
                    if len(pls_encontradas) >= limite:
                        break
                    
                    try:
                        # Extrair informações da matéria (estrutura simplificada da API /pesquisa/lista)
                        sigla = materia.get('Sigla', '')
                        numero = materia.get('Numero', '')
                        ano_materia = materia.get('Ano', '')
                        codigo = materia.get('Codigo', '')
                        ementa = materia.get('Ementa', '')
                        autor = materia.get('Autor', 'N/A')
                        data = materia.get('Data', 'N/A')
                        
                        # Filtrar apenas Projetos de Lei (PL, PLS, PLC, PLP)
                        if sigla not in ['PLS', 'PLC', 'PL', 'PLP']:
                            continue
                        
                        if not ementa or len(ementa) < 10:
                            continue
                        
                        ementa_lower = ementa.lower()
                        
                        # Filtrar por termos LGBTQIA+ (mesma lógica das outras fontes)
                        tem_termo_especifico = False
                        for termo in TERMOS_BUSCA_ESPECIFICOS:
                            if termo == 'trans' and 'trans' in ementa_lower:
                                if re.search(r'\btrans\b', ementa_lower) and (
                                    any(p in ementa_lower for p in ['gênero', 'sexual', 'identidade', 'lgbt', 'transfobia', 'transexual', 'transgênero']) or
                                    any(p in ementa_lower for p in ['proíbe', 'veda', 'restringe', 'garante', 'reconhece', 'criminaliza', 'direito', 'direitos'])
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
                            # Construir link para matéria
                            link = f"https://www25.senado.leg.br/web/atividade/materias/-/materia/{codigo}" if codigo else "https://www25.senado.leg.br/web/atividade/materias"
                            
                            pls_encontradas.append({
                                'Nº': f"{sigla} {numero}/{ano_materia}",
                                'Ano': str(ano_materia),
                                'Casa': 'Senado',
                                'Ementa': ementa,
                                'Autores': autor,
                                'Data': data[:10] if isinstance(data, str) and len(data) >= 10 else str(data),
                                'Link': link,
                                'Status': materia.get('DescricaoIdentificacao', 'N/A'),
                                'Fonte': 'Senado Federal'
                            })
                            
                            materias_ano += 1
                    
                    except Exception as e:
                        # Pular matéria se houver erro no parse
                        continue
                
                if materias_ano > 0:
                    print(f"   ✅ Senado {ano}: {materias_ano} PLs relevantes")
                
            except requests.exceptions.HTTPError as e:
                print(f"   ⚠️ Erro HTTP no Senado ({ano}): {e.response.status_code}")
                continue
            except Exception as e:
                print(f"   ⚠️ Erro no Senado ({ano}): {str(e)[:80]}")
                continue
        
        print(f"   📊 Total Senado: {len(pls_encontradas)} PLs")
        return pls_encontradas[:limite]
        
    except Exception as e:
        print(f"   ⚠️ Erro geral ao buscar no Senado: {str(e)[:100]}")
        return []

def buscar_camara_sao_paulo(
    termos: List[str] = None,
    ano_inicio_manual: Optional[int] = None,
    ano_fim_manual: Optional[int] = None,
    limite: int = 50
) -> List[Dict]:
    """
    Busca PLs na Câmara Municipal de São Paulo
    
    Web Service: https://splegisws.saopaulo.sp.leg.br/ws/ws2.asmx
    Método: ProjetosPorAnoJSON
    Portal de Dados Abertos: https://www.saopaulo.sp.leg.br/transparencia/dados-abertos/dados-disponibilizados-em-formato-aberto/
    """
    if termos is None:
        termos = TERMOS_BUSCA
    
    print(f"📥 Buscando projetos na Câmara Municipal de SP...")
    
    # URL do web service
    base_url = "https://splegisws.saopaulo.sp.leg.br/ws/ws2.asmx/ProjetosPorAnoJSON"
    
    pls_encontradas = []
    
    # Determinar anos para buscar
    ano_atual = datetime.now().year
    
    if ano_inicio_manual is not None and ano_fim_manual is not None:
        anos_para_buscar = list(range(ano_inicio_manual, ano_fim_manual + 1))
    else:
        # Padrão: ano atual
        anos_para_buscar = [ano_atual]
    
    try:
        # Buscar projetos por ano
        for ano in reversed(anos_para_buscar):
            if len(pls_encontradas) >= limite:
                break
            
            print(f"   📅 Buscando projetos de {ano}...")
            
            try:
                # Chamar web service
                params = {'Ano': ano}
                response = requests.get(base_url, params=params, timeout=30)
                response.raise_for_status()
                
                projetos = response.json()
                if not isinstance(projetos, list):
                    print(f"   ⚠️ Resposta não é lista: {type(projetos)}")
                    continue
                
                print(f"   📊 {len(projetos)} projetos encontrados em {ano} (antes do filtro)")
                
                # Filtrar por termos LGBTQIA+
                for projeto in projetos:
                    if len(pls_encontradas) >= limite:
                        break
                    
                    ementa = projeto.get('ementa', '')
                    if not ementa or len(ementa) < 10:
                        continue
                    
                    ementa_lower = ementa.lower()
                    
                    # Filtrar por termos específicos primeiro
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
                    
                    # Verificar termos contextuais
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
                        tipo = projeto.get('tipo', 'PL')
                        numero = projeto.get('numero', 'N/A')
                        ano_projeto = projeto.get('ano', 'N/A')
                        data_projeto = projeto.get('data', 'N/A')
                        chave = projeto.get('chave', '')
                        
                        # Construir link (baseado na estrutura comum da Câmara SP)
                        link = f"https://www.saopaulo.sp.leg.br/vereadores/projetos-de-lei/?projeto={chave}" if chave else f"https://www.saopaulo.sp.leg.br/"
                        
                        pls_encontradas.append({
                            'Nº': f"{tipo} {numero}/{ano_projeto}",
                            'Ano': str(ano_projeto),
                            'Casa': 'Câmara Municipal SP',
                            'Ementa': ementa,
                            'Autores': 'N/A',  # Pode obter via ProjetosAutoresJSON se necessário
                            'Data': data_projeto[:10] if isinstance(data_projeto, str) and len(data_projeto) >= 10 else str(data_projeto),
                            'Link': link,
                            'Status': 'N/A',
                            'Fonte': 'Câmara Municipal de São Paulo'
                        })
                
                if pls_encontradas:
                    print(f"   ✅ {len(pls_encontradas)} projetos relevantes encontrados em {ano}")
                    
            except requests.exceptions.HTTPError as e:
                print(f"   ⚠️ Erro HTTP ao buscar projetos de {ano}: {e.response.status_code}")
                continue
            except Exception as e:
                print(f"   ⚠️ Erro ao buscar projetos de {ano}: {str(e)[:100]}")
                continue
        
        print(f"   ✅ Total: {len(pls_encontradas)} projetos relevantes encontrados na Câmara Municipal SP")
        
        return pls_encontradas[:limite]
        
    except Exception as e:
        print(f"   ⚠️ Erro geral ao buscar na Câmara Municipal SP: {str(e)[:150]}")
        return []

def buscar_alesp(
    termos: List[str] = None,
    ano_inicio_manual: Optional[int] = None,
    ano_fim_manual: Optional[int] = None,
    limite: int = 50
) -> List[Dict]:
    """
    Busca PLs na ALESP (Assembleia Legislativa de São Paulo)
    
    Portal: https://www.al.sp.gov.br/dados-abertos/
    Arquivo: https://www.al.sp.gov.br/repositorioDados/processo_legislativo/proposituras.zip
    Formato: ZIP contendo XML com todas as proposituras (atualizado diariamente)
    
    Frequência de atualização: Diária
    Portal de dados abertos: https://www.al.sp.gov.br/dados-abertos/recurso/56
    """
    if termos is None:
        termos = TERMOS_BUSCA
    
    print(f"   📥 Buscando proposituras na ALESP...")
    # NOTA: O arquivo proposituras.zip é atualizado DIARIAMENTE no portal da ALESP.
    # Para garantir dados atualizados, baixamos o arquivo toda vez que uma busca é feita.
    # Isso garante que mesmo no Hugging Face Space, sempre teremos os dados mais recentes.
    
    # URL do arquivo ZIP
    url_zip = "https://www.al.sp.gov.br/repositorioDados/processo_legislativo/proposituras.zip"
    
    pls_encontradas = []
    
    try:
        # Baixar arquivo ZIP (sob demanda - sempre busca a versão mais recente)
        print(f"   📦 Baixando arquivo proposituras.zip atualizado (última atualização do portal)...")
        print(f"   ⏱️ Isso garante dados atualizados diariamente (pode levar 10-20 segundos)")
        response = requests.get(url_zip, timeout=120, stream=True)
        response.raise_for_status()
        
        zip_data = BytesIO(response.content)
        
        with zipfile.ZipFile(zip_data, 'r') as zip_ref:
            files = zip_ref.namelist()
            if not files:
                print(f"   ⚠️ ZIP vazio")
                return []
            
            xml_file = files[0]
            print(f"   📄 Extraindo {xml_file}...")
            
            # Ler XML (pode ser grande, mas preciso parsear)
            xml_content = zip_ref.read(xml_file)
            print(f"   📊 XML extraído: {len(xml_content)/1024/1024:.1f}MB")
            
            # Parsear XML
            root = ET.fromstring(xml_content)
            
            # Buscar todas as proposituras
            proposituras = root.findall('.//propositura')
            total_props = len(proposituras)
            print(f"   📋 Total de proposituras no arquivo: {total_props}")
            
            # Filtrar proposituras
            for propositura in proposituras:
                if len(pls_encontradas) >= limite:
                    break
                
                # Extrair campos do XML
                ano_text = propositura.findtext('AnoLegislativo', '')
                numero_text = propositura.findtext('NroLegislativo', '')
                ementa = propositura.findtext('Ementa', '')
                id_doc = propositura.findtext('IdDocumento', '')
                data_entrada = propositura.findtext('DtEntradaSistema', '')
                natureza_id = propositura.findtext('IdNatureza', '')
                
                if not ementa or len(ementa) < 10:
                    continue
                
                # Filtrar por ano se especificado
                if ano_inicio_manual is not None and ano_fim_manual is not None:
                    try:
                        ano_int = int(ano_text) if ano_text else 0
                        if not (ano_inicio_manual <= ano_int <= ano_fim_manual):
                            continue
                    except:
                        continue
                
                # Filtrar por termos LGBTQIA+
                ementa_lower = ementa.lower()
                
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
                    # Determinar sigla do tipo (pode estar em outros campos)
                    sigla = 'PL'  # Padrão
                    tipo_text = propositura.findtext('Sigla', '') or propositura.findtext('Tipo', '')
                    if tipo_text:
                        sigla = tipo_text.upper()
                    
                    # Link para propositura (formato comum da ALESP)
                    link = f"https://www.al.sp.gov.br/propositura/?id={id_doc}" if id_doc else "https://www.al.sp.gov.br/"
                    
                    pls_encontradas.append({
                        'Nº': f"{sigla} {numero_text}/{ano_text}" if numero_text and ano_text else f"Nº {id_doc}",
                        'Ano': ano_text or 'N/A',
                        'Casa': 'ALESP',
                        'Ementa': ementa,
                        'Autores': propositura.findtext('Autor', 'N/A'),
                        'Data': data_entrada[:10] if data_entrada else 'N/A',  # Apenas data, sem hora
                        'Link': link,
                        'Status': 'N/A',
                        'Fonte': 'ALESP'
                    })
        
        print(f"   ✅ {len(pls_encontradas)} proposituras relevantes encontradas na ALESP")
        
        return pls_encontradas[:limite]
        
    except requests.exceptions.HTTPError as e:
        print(f"   ⚠️ Erro HTTP ao buscar na ALESP: {e.response.status_code}")
        return []
    except Exception as e:
        print(f"   ⚠️ Erro ao buscar na ALESP: {str(e)[:150]}")
        import traceback
        print(f"   Detalhes: {traceback.format_exc()[:200]}")
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

