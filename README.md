---
title: Radar Legislativo LGBTQIA+🏳️‍🌈 v1.0
emoji: 📡
colorFrom: purple
colorTo: pink
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: cc-by-nc-sa-4.0
short_description: Busca e análise (IA) de PLs LGBTQIA+ no Congresso e em SP
tags:
  - lgbtqia
  - legislacao
  - congresso-nacional
  - hate-speech-detection
  - ensemble
  - radar-social
---

# 🏳️‍🌈 Radar Legislativo LGBTQIA+

Sistema de busca e análise automática de Projetos de Lei relacionados a direitos LGBTQIA+ no **Congresso Nacional** (Câmara dos Deputados e Senado Federal).

## 📋 Sobre

Este sistema utiliza um **Ensemble Híbrido** que combina:
- **Radar Social LGBTQIA+ V2.1**: Modelo de detecção de discurso de ódio (98.44% recall)
- **AzMina/QuiterIA**: Modelo de análise feminista de PLs
- **Keywords**: Palavras-chave específicas LGBTQIA+
- **Padrões Legislativos**: Heurísticas para identificar estruturas restritivas

Para identificar se PLs são **favoráveis** ou **desfavoráveis** aos direitos da comunidade LGBTQIA+.

## 🚀 Como Usar

### Radar Automático
1. **Selecione o período:** Escolha o ano inicial e final (2010-2025)
2. **Escolha as fontes:** Marque Câmara dos Deputados e/ou Senado Federal
3. **Defina o limite:** Quantas PLs você quer encontrar (recomendado: 50-100)
4. **Clique em "Buscar e Analisar PLs"**

O sistema:
- Busca PLs nas APIs oficiais usando termos relacionados a LGBTQIA+
- Filtra PLs que contêm termos relevantes na ementa
- Analisa automaticamente cada PL encontrada com o Ensemble Híbrido
- Exibe resultados com classificação (Favorável/Desfavorável/Revisão)

## 📊 Thresholds de Classificação

- **≥50%**: DESFAVORÁVEL
- **30-50%**: REVISÃO NECESSÁRIA
- **<30%**: FAVORÁVEL

## ⚠️ Limitações Importantes

- **Requer revisão humana**: Classificações são sugestões, não decisões definitivas
- **Contexto limitado**: Não considera histórico completo de tramitação
- **Modelos não específicos**: Treinados em outros contextos (redes sociais, PLs gerais)
- **Falsos positivos possíveis**: Linguagem técnica pode gerar alertas incorretos

## 📊 Modelos Utilizados

- **Radar Social LGBTQIA+ V2.1** por [Veronyka](https://huggingface.co/Veronyka/radar-social-lgbtqia-v2.1)
  - 98.44% de recall na detecção de hate speech
  - Threshold: 0.30
  - Treinado com 1.891 comentários anotados manualmente
  
- **IA Feminista AzMina** por [AzMina](https://huggingface.co/azmina/ia-feminista-bert-posicao)
  - Análise de PLs sob perspectiva feminista
  - Proxy para direitos LGBTQIA+

## 🔧 Tecnologias

- **Gradio 4.44.0**: Interface web
- **Transformers**: Modelos BERT-based
- **Pandas**: Processamento de dados
- **Requests**: Integração com APIs do Congresso

## 📚 API do Congresso Nacional

### Câmara dos Deputados
- **Base URL**: `https://dadosabertos.camara.leg.br/api/v2`
- **Endpoint**: `/proposicoes`
- **Documentação**: https://dadosabertos.camara.leg.br/swagger/api.html

### Senado Federal
- **Base URL**: `https://legis.senado.leg.br/dadosabertos`
- **Endpoint**: `/materia/atualizadas`
- **Swagger**: https://legis.senado.leg.br/dadosabertos/api-docs/swagger-ui/index.html

## 📈 Recomendações de Uso

- **Período pequeno (1-2 anos):** Rápido, poucos resultados
- **Período médio (3-5 anos):** Balanceado, mais resultados
- **Período grande (2010-2025):** Pode levar alguns minutos, muitos resultados

## 💡 Exemplo de Uso

```python
# Buscar PLs de 2020 a 2025 na Câmara e Senado
# Limite: 50 PLs
# Resultado: Lista de PLs classificadas como Favorável/Desfavorável/Revisão
```

## 📝 Estrutura do Projeto

```
├── app.py                  # Interface Gradio principal
├── ensemble_híbrido.py     # Lógica de classificação ensemble
├── api_radar.py           # Integração com APIs do Congresso
├── requirements.txt        # Dependências Python
└── README.md              # Documentação
```

## 📄 Licença

Este projeto utiliza modelos públicos disponíveis no Hugging Face:
- **Radar Social LGBTQIA+ V2.1**: Treinado por [Veronyka](https://huggingface.co/Veronyka)
- **AzMina/QuiterIA**: Treinado pela equipe [AzMina](https://huggingface.co/azmina)

Licença: CC-BY-NC-SA-4.0

## 🙏 Agradecimentos

- **AzMina** pelo modelo feminista de análise de PLs
- **Comunidade LGBTQIA+** pela inspiração e necessidade de ferramentas como esta
- **LabHacker da Câmara** pela inspiração em soluções de dados abertos
- **Hugging Face** pela infraestrutura de hospedagem

## 🔗 Links Relacionados

- **Radar Social LGBTQIA+ V2.1**: https://huggingface.co/spaces/Veronyka/radar-social-lgbtqia-v2.1
- **Análise de Base de Dados**: https://huggingface.co/spaces/Veronyka/radar-social-lgbtqia-v2-analise
- **Dataset Base**: https://huggingface.co/datasets/Veronyka/base-dados-odio-lgbtqia

---

**Use como ferramenta de apoio, sempre com revisão humana.** 🏳️‍🌈⚖️

*Desenvolvido com ❤️ para a comunidade LGBTQIA+*
