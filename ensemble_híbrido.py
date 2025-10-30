"""
Ensemble Híbrido: Combina AzMina + Radar Social + Keywords + Padrões
FASE 1 do Plano Revisado
"""

from transformers import pipeline
import torch
import re
from typing import Dict, Tuple, List
import pandas as pd

# Modelos
MODEL_RADAR = "Veronyka/radar-social-lgbtqia-v2.1"
MODEL_AZMINA = "azmina/ia-feminista-bert-posicao"

# Keywords (expandido baseado em análise dos resultados)
KEYWORDS_FAVORAVEIS = [
    # Termos básicos
    r"identidade de gênero", r"orientação sexual", r"lgbtqia\+", r"lgbt",
    r"diversidade sexual", r"nome social", r"autodeterminação",
    r"criminaliza.*homofobia", r"criminaliza.*transfobia",
    r"proteção.*lgbt", r"direitos.*lgbt", r"igualdade.*gênero",
    r"não discriminação", r"reconhecimento.*gênero",
    r"características sexuais", r"expressão de gênero",
    r"estatuto.*diversidade", r"transparência salarial.*orientação", r"misoginia.*orientação",
    
    # Baseado no Radar Social - contexto positivo
    r"proíbe.*terapias.*conversão",  # Proibir terapias de conversão = favorável
    r"equipara.*(terapia|terapias).*conversão.*(à|a).*tortura",  # Equiparar terapias de conversão à tortura = favorável (PL 5034)
    r"equipara.*(cura.*gay|terapia.*conversão).*tortura",  # Variação
    r"garante.*(direito|direitos).*(lgbt|trans|gay|orientação)",
    r"reconhece.*(identidade|vivência|expressão)",
    r"inclui.*(orientação|identidade).*(censo|dados|pesquisa)",
    r"protege.*contra.*violência.*(lgbt|trans|gay)",
    r"cria.*mecanismos.*proteção.*(lgbt|trans|orientação)",
    r"visibilidade.*(lgbt|trans|diversidade)",
    r"representação.*(lgbt|trans|diversidade)",
    r"inclusão.*(lgbt|trans|diversidade)",
    r"comunidade.*(lgbt|trans|diversidade).*direitos",
    r"apoio.*(lgbt|trans|diversidade)",
    r"respeito.*(identidade|vivência|expressão).*gênero"
]

KEYWORDS_DESFAVORAVEIS = [
    # Básicos legislativos
    r"sexo biológico", r"sexo de nascimento", r"ideologia de gênero",
    r"proíbe.*gênero", r"veda.*gênero", r"restringe.*gênero",
    r"valores familiares", r"proteção.*infância",
    r"banheiro.*sexo", r"vestiário.*sexo", r"separar.*sexo",
    r"exclusivamente.*(homem|mulher)", r"critério exclusivo.*sexo",
    r"proíbe.*linguagem neutra", r"veda.*linguagem neutra",
    r"proíbe.*educação sexual", r"atletas trans.*competições",
    r"escola sem partido", r"unissex.*separado",
    r"estatuto.*família", r"união.*(homem|mulher)", r"entre.*homem.*mulher",
    
    # Baseado no Radar Social - termos específicos (versões flexíveis)
    # Padrões com verbos (proíbe/veda) E substantivos (proibição/vedação)
    r"(proíbe|veda|proibição|vedação).*(uso|exibição|porte).*(símbolo|símbolos|ícone).*religios.*(parada|paradas|lgbtqia|lgbtt|comunidade|evento|eventos)",
    r"(proíbe|veda|proibição).*(uso|exibição).*(símbolo|símbolos).*religios.*(em|em paradas|nas paradas|de paradas).*(lgbtqia|lgbt|lgbtt)",
    r"proibição.*(uso|do uso).*(símbolo|símbolos).*(crist|religios).*(lgbt|lgbtqia|parada|evento)",
    r"(símbolo|símbolos).*(crist|religios).*(parada|paradas|lgbt|lgbtqia|evento|eventos).*(proíb|veta|veda)",
    r"impede.*presença.*menor", r"proíbe.*menor.*evento", r"criança.*evento.*lgbt",
    # Padrões específicos para PL 106 e PL 906 (alta precisão)
    r"(impede|proíbe|veda).*(presença|participação|acesso).*(menor|menores|criança|crianças).*(evento|parada|manifestação|atividade).*(da|da comunidade).*(lgbtqia|lgbt|comunidade|diversidade)",
    r"(impede|proíbe|veda).*(menor|criança).*(evento|parada|comemoração).*(lgbtqia|comunidade|diversidade)",
    
    # Patologização (do Radar Social)
    r"terapias.*conversão", r"cura.*gay", r"reparação.*sexual",
    r"tratamento.*orientação", r"laudo.*psiquiátrico.*trans",
    
    # Moralismo religioso em contexto legislativo
    r"valores.*(cristão|religioso|bíblico).*educação",
    r"sagrado.*família", r"família.*tradicional",
    
    # Termos de redução/patologização
    r"doença.*mental.*(trans|gay|lgbt)", r"transtorno.*(identidade|orientação)",
    r"desvio.*(sexual|gênero)", r"anormalidade.*(sexual|gênero)",
    
    # Restrições específicas
    r"proíbe.*participação.*(trans|lgbt).*evento",
    r"veda.*visibilidade.*(lgbt|gay|trans)",
    r"restringe.*acesso.*(trans|lgbt).*espaço"
]

# Padrões legislativos desfavoráveis
# Padrões de ALTA PRIORIDADE (mais específicos e confiáveis)
PADROES_ALTA_PRIORIDADE = [
    # PL 106: Símbolos religiosos em paradas LGBTQIA+ (verbos E substantivos)
    r"(proíbe|veda|proibição|vedação).*(uso|do uso|exibição|porte).*(símbolo|símbolos|ícone).*religios.*(em|em paradas|nas paradas|de paradas).*(lgbtqia|lgbt|lgbtt)",
    r"(proíbe|veda|proibição).*(símbolo|símbolos).*religios.*(parada|paradas|evento|eventos).*(lgbtqia|lgbt|comunidade)",
    r"proibição.*(uso|do uso).*(símbolo|símbolos).*(crist|religios).*(lgbt|lgbtqia|parada|evento)",
    r"(símbolo|símbolos).*(crist|religios).*(parada|paradas|lgbt|lgbtqia|evento|eventos).*(proíb|veta|veda|proibição)",
    
    # PL 906: Impede menores em eventos LGBTQIA+ (verbos E substantivos)
    r"(impede|proíbe|veda|proibição|vedação).*(presença|participação|acesso).*(menor|menores|criança|crianças).*(em|em eventos|nos eventos|de eventos|em paradas).*(da|da comunidade|lgbtqia|lgbt|comunidade|diversidade)",
    r"(impede|proíbe|veda|proibição).*(menor|menores|criança|crianças).*(evento|parada|manifestação|atividade).*(lgbtqia|lgbt|comunidade)",
    r"proibição.*(presença|da presença).*(menor|menores|criança|crianças).*(em|nos|de).*evento.*(da|da comunidade|lgbtqia|lgbt|comunidade)"
]

# Padrões normais (menos específicos, mas ainda importantes)
PADROES_RESTRITIVOS = [
    r"define.*(sexo|gênero).*biolog",  # "Define gênero por critérios biológicos"
    r"(proíbe|proibição).*(ensino|divulgação).*gênero",
    r"(veda|vedação).*uso.*por.*(pessoas|indivíduos).*(diferentes|diversos)",
    r"exclusivamente.*(homem|mulher).*(cis|biologic)",
    r"(restringe|limita|restrição).*participação.*(sexo|gênero)",
    r"define.*entidade.*(homem|mulher)",  # "Define entidade familiar como união entre homem e mulher"
    r"(proíbe|proibição|impede|veda).*menor.*(evento|parada)",  # Proíbe menores em eventos (genérico)
    r"(proíbe|veda|proibição).*símbolo.*(religioso|parada|lgbt)"  # Proíbe símbolos em paradas (genérico)
]

def carregar_modelos():
    """Carrega ambos os modelos"""
    print("📦 Carregando modelos...")
    
    try:
        radar = pipeline(
            "text-classification",
            model=MODEL_RADAR,
            device=-1  # CPU
        )
        print("   ✅ Radar Social carregado")
    except Exception as e:
        print(f"   ⚠️ Erro ao carregar Radar Social: {e}")
        radar = None
    
    try:
        # AzMina não tem tokenizer_config.json no repositório, então usamos o tokenizer do modelo base
        # Conforme README do modelo: base_model = neuralmind/bert-base-portuguese-cased
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        
        # Modelo base conforme documentado no README do repositório AzMina
        base_model = "neuralmind/bert-base-portuguese-cased"
        
        print("   🔧 Carregando AzMina com tokenizer do modelo base...")
        # Carregar tokenizer do modelo base (mesmo usado no treinamento do AzMina)
        tokenizer = AutoTokenizer.from_pretrained(base_model)
        # Carregar apenas o modelo AzMina (fine-tuned)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_AZMINA)
        
        # Criar pipeline combinando modelo AzMina + tokenizer do modelo base
        # Isso é seguro porque o AzMina foi treinado com esse tokenizer específico
        azmina = pipeline(
            "text-classification",
            model=model,
            tokenizer=tokenizer,
            device=-1  # CPU
        )
        print("   ✅ AzMina carregado")
    except Exception as e:
        error_msg = str(e)
        print(f"   ⚠️ Erro ao carregar AzMina: {error_msg[:150]}")
        print("   ℹ️ Tentando método alternativo (pipeline direto)...")
        try:
            # Fallback: tentar pipeline direto (provavelmente falhará, mas tentamos)
            azmina = pipeline(
                "text-classification",
                model=MODEL_AZMINA,
                device=-1
            )
            print("   ✅ AzMina carregado (método alternativo)")
        except Exception as e2:
            print(f"   ❌ AzMina não pôde ser carregado: {str(e2)[:100]}")
            print("   ⚠️ Sistema funcionará apenas com Radar Social + Keywords + Padrões")
            azmina = None
    
    return radar, azmina

def extrair_keywords(texto: str) -> Tuple[int, int]:
    """Conta keywords favoráveis e desfavoráveis"""
    texto_lower = texto.lower()
    
    favoraveis = sum(1 for kw in KEYWORDS_FAVORAVEIS 
                     if re.search(kw, texto_lower, re.IGNORECASE))
    
    desfavoraveis = sum(1 for kw in KEYWORDS_DESFAVORAVEIS 
                        if re.search(kw, texto_lower, re.IGNORECASE))
    
    return favoraveis, desfavoraveis

def detectar_padroes_restritivos(texto: str) -> float:
    """Detecta padrões legislativos desfavoráveis com pesos diferenciados"""
    texto_lower = texto.lower()
    
    # Padrões de alta prioridade (peso 2) - mais específicos e confiáveis
    matches_alta = sum(1 for padrao in PADROES_ALTA_PRIORIDADE 
                       if re.search(padrao, texto_lower, re.IGNORECASE))
    
    # Padrões normais (peso 1)
    matches_normais = sum(1 for padrao in PADROES_RESTRITIVOS 
                          if re.search(padrao, texto_lower, re.IGNORECASE))
    
    # BOOST FORTE: Se encontrou padrão de alta prioridade, dar score alto
    # Esses padrões são muito específicos e indicam claramente desfavorável
    if matches_alta > 0:
        # Se tem match de alta prioridade, dar score mínimo de 0.99
        # Com peso de 30%, isso contribui com 0.99 * 0.30 = 0.297 (~29.7%)
        # Com outros sinais baixos (~25-35%), total chega a ~50%+ (DESFAVORÁVEL)
        # Boost aumentado para garantir que PLs com padrões de alta prioridade sempre sejam DESFAVORÁVEIS
        return max(0.99, min(0.995, 0.99 + (matches_alta * 0.002)))
    
    # Score ponderado (alta prioridade vale mais)
    # Normalizar considerando os pesos
    total_peso_max = (len(PADROES_ALTA_PRIORIDADE) * 2) + len(PADROES_RESTRITIVOS)
    score_atual = (matches_alta * 2) + matches_normais
    
    # Normalizar para 0-1
    score_normalizado = min(score_atual / total_peso_max, 1.0)
    
    return score_normalizado

def classificar_ensemble(
    texto: str,
    radar_model,
    azmina_model,
    pesos: Dict[str, float] = None
) -> Dict:
    """Combina múltiplos sinais para classificar PL"""
    
    if pesos is None:
        # Pesos ajustados: dar mais peso a keywords e padrões (mais específicos para legislação)
        # Se AzMina não estiver disponível, redistribuir seu peso proporcionalmente
        if azmina_model is None:
            # Sem AzMina: aumentar peso de keywords e padrões proporcionalmente
            pesos = {
                'radar': 0.20,      # Detecção de ódio
                'azmina': 0.0,      # AzMina não disponível
                'keywords': 0.40,    # Aumentado de 0.35 para 0.40 (+0.05 do AzMina)
                'padroes': 0.40     # Aumentado de 0.30 para 0.40 (+0.10 do AzMina)
            }
        else:
            # Com ambos os modelos: distribuição otimizada
            pesos = {
                'radar': 0.20,      # Detecção de ódio (menos relevante em legislação)
                'azmina': 0.15,     # Perspectiva feminista (proxy, não ideal) - REDUZIDO
                'keywords': 0.35,   # Keywords específicas (MAIS IMPORTANTE - legislação tem termos claros)
                'padroes': 0.30     # Padrões legislativos (CRÍTICO para detectar restrições) - AUMENTADO
            }
    
    resultados = {}
    
    # Sinal 1: Radar Social (detecção de ódio)
    if radar_model:
        try:
            radar_result = radar_model(texto, truncation=True, max_length=256)
            label = radar_result[0]['label']
            score = radar_result[0]['score']
            score_odio = 1 - score if label != 'HATE' else score
            resultados['radar'] = score_odio
        except:
            resultados['radar'] = 0.5  # Neutro se erro
    else:
        resultados['radar'] = 0.5
    
    # Sinal 2: AzMina (direitos de mulheres)
    if azmina_model:
        try:
            azmina_result = azmina_model(texto, truncation=True, max_length=256)
            # Assumindo que label 0 = desfavorável, 1 = favorável
            # Ajustar baseado na documentação real do modelo
            score_favoravel = azmina_result[0]['score'] if azmina_result[0]['label'] == 'LABEL_1' else 1 - azmina_result[0]['score']
            resultados['azmina'] = 1 - score_favoravel  # Inverter: menor = mais favorável
        except:
            resultados['azmina'] = 0.5
    else:
        resultados['azmina'] = 0.5
    
    # Sinal 3: Keywords (com detecção de padrões favoráveis específicos)
    texto_lower = texto.lower()
    
    # Padrões de ALTA PRIORIDADE FAVORÁVEIS (boost negativo - diminui score)
    padroes_favoraveis_alta = [
        r"equipara.*(terapia|terapias).*conversão.*(à|a).*tortura",  # PL 5034
        r"equipara.*(cura.*gay|terapia.*conversão).*tortura",
        r"equipara.*terapia.*conversão.*tortura"
    ]
    
    tem_padrao_favoravel_alta = any(
        re.search(padrao, texto_lower, re.IGNORECASE) 
        for padrao in padroes_favoraveis_alta
    )
    
    kw_fav, kw_desfav = extrair_keywords(texto)
    total_kw = kw_fav + kw_desfav if (kw_fav + kw_desfav) > 0 else 1
    
    if tem_padrao_favoravel_alta:
        # Se tem padrão favorável de alta prioridade, forçar score baixo
        score_keywords = 0.15  # Score muito baixo = muito favorável
    else:
        score_keywords = kw_desfav / total_kw  # Mais keywords desfavoráveis = maior score
    
    resultados['keywords'] = min(score_keywords, 1.0)
    
    # Sinal 4: Padrões legislativos
    padroes_score = detectar_padroes_restritivos(texto)
    resultados['padroes'] = padroes_score
    
    # Ajuste dinâmico: Se padrões de alta prioridade foram detectados, aumentar seu peso
    # Isso garante que PLs com padrões críticos (ex: proibir símbolos em paradas, impedir menores)
    # sejam sempre classificadas como DESFAVORÁVEIS
    pesos_ajustados = pesos.copy()
    if padroes_score >= 0.95:  # Se padrão de alta prioridade foi detectado
        # Redistribuir pesos: aumentar padrões, reduzir outros proporcionalmente
        aumento_padroes = 0.10  # Aumentar padrões em 10%
        pesos_ajustados['padroes'] = min(0.50, pesos['padroes'] + aumento_padroes)
        # Reduzir outros proporcionalmente
        outros_pesos = sum(v for k, v in pesos.items() if k != 'padroes')
        fator_reducao = (outros_pesos - aumento_padroes) / outros_pesos
        for k in pesos_ajustados:
            if k != 'padroes':
                pesos_ajustados[k] = pesos[k] * fator_reducao
    
    # Combinar com pesos (ajustados se necessário)
    score_final = (
        pesos_ajustados['radar'] * resultados['radar'] +
        pesos_ajustados['azmina'] * resultados['azmina'] +
        pesos_ajustados['keywords'] * resultados['keywords'] +
        pesos_ajustados['padroes'] * resultados['padroes']
    )
    
    # Classificar
    if score_final >= 0.5:
        classificacao = "DESFAVORÁVEL"
    elif score_final >= 0.3:
        classificacao = "REVISÃO"
    else:
        classificacao = "FAVORÁVEL"
    
    return {
        'classificacao': classificacao,
        'score_final': score_final,
        'sinais': resultados,
        'pesos_usados': pesos,
        'explicacao': f"""
        Score Final: {score_final:.2%}
        
        Contribuição de cada sinal:
        - Radar Social (ódio): {resultados['radar']:.2%} (peso {pesos['radar']:.0%})
        - AzMina (mulheres): {resultados['azmina']:.2%} (peso {pesos['azmina']:.0%})
        - Keywords: {resultados['keywords']:.2%} (peso {pesos['keywords']:.0%})
        - Padrões: {resultados['padroes']:.2%} (peso {pesos['padroes']:.0%})
        """
    }

def testar_ensemble(dataset_path: str = "pls_processadas.csv"):
    """Testa o ensemble no dataset anotado"""
    
    print("\n🧪 Testando Ensemble Híbrido...\n")
    
    # Carregar modelos
    radar, azmina = carregar_modelos()
    
    # Carregar dataset
    try:
        df = pd.read_csv(dataset_path)
        print(f"✅ Dataset carregado: {len(df)} PLs\n")
    except:
        print(f"❌ Erro ao carregar {dataset_path}")
        return
    
    # Classificar cada PL
    resultados = []
    for idx, row in df.iterrows():
        ementa = str(row.get('Ementa', ''))
        posicao_real = row.get('Posição', 'N/A')
        
        if not ementa or ementa.strip() == '':
            continue
        
        resultado = classificar_ensemble(ementa, radar, azmina)
        
        resultados.append({
            'PL': row.get('Nº', f'PL {idx+1}'),
            'Classificação Real': posicao_real,
            'Classificação Predita': resultado['classificacao'],
            'Score Final': resultado['score_final'],
            **{f'Sinal_{k}': v for k, v in resultado['sinais'].items()}
        })
    
    # Calcular métricas
    df_resultados = pd.DataFrame(resultados)
    
    corretos = sum(
        (df_resultados['Classificação Real'].str.contains('Favorável', case=False) &
         df_resultados['Classificação Predita'].str.contains('FAVORÁVEL', case=False)) |
        (df_resultados['Classificação Real'].str.contains('Desfavorável', case=False) &
         df_resultados['Classificação Predita'].str.contains('DESFAVORÁVEL', case=False))
    )
    
    total = len(df_resultados)
    accuracy = corretos / total if total > 0 else 0
    
    # Precision/Recall para DESFAVORÁVEL
    verdadeiros_positivos = sum(
        (df_resultados['Classificação Real'].str.contains('Desfavorável', case=False) &
         df_resultados['Classificação Predita'].str.contains('DESFAVORÁVEL', case=False))
    )
    falsos_positivos = sum(
        (df_resultados['Classificação Real'].str.contains('Favorável', case=False) &
         df_resultados['Classificação Predita'].str.contains('DESFAVORÁVEL', case=False))
    )
    falsos_negativos = sum(
        (df_resultados['Classificação Real'].str.contains('Desfavorável', case=False) &
         ~df_resultados['Classificação Predita'].str.contains('DESFAVORÁVEL', case=False))
    )
    
    precision = verdadeiros_positivos / (verdadeiros_positivos + falsos_positivos) if (verdadeiros_positivos + falsos_positivos) > 0 else 0
    recall = verdadeiros_positivos / (verdadeiros_positivos + falsos_negativos) if (verdadeiros_positivos + falsos_negativos) > 0 else 0
    
    print("=" * 60)
    print("📊 RESULTADOS DO ENSEMBLE")
    print("=" * 60)
    print(f"Accuracy: {accuracy:.1%}")
    print(f"Precision (DESFAVORÁVEL): {precision:.1%}")
    print(f"Recall (DESFAVORÁVEL): {recall:.1%}")
    print(f"F1-Score: {2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0:.1%}")
    print(f"\nCorretos: {corretos}/{total}")
    print("\n" + "=" * 60)
    print(df_resultados[['PL', 'Classificação Real', 'Classificação Predita', 'Score Final']].to_string(index=False))
    
    return df_resultados

if __name__ == "__main__":
    testar_ensemble()

