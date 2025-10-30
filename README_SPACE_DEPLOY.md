# 🚀 Guia de Deploy - Radar Legislativo LGBTQIA+

## Passo a Passo para Criar Space no Hugging Face

### 1. Criar Novo Space

1. Acesse: https://huggingface.co/spaces
2. Clique em **"Create new Space"**
3. Configure:
   - **Name**: `radar-legislativo-lgbtqia` (ou outro nome de sua preferência)
   - **SDK**: **Gradio**
   - **Hardware**: **CPU Standard** (suficiente para os modelos)
   - **Visibility**: **Público** (recomendado)

### 2. Arquivos para Upload

Faça upload destes arquivos no repositório do Space:

```
📁 radar-legislativo-lgbtqia/
├── app.py                      ✅ Principal
├── ensemble_híbrido.py         ✅ Sistema de classificação
├── api_radar.py                ✅ Integração com APIs
├── requirements.txt            ✅ Dependências
├── README.md                   ✅ Documentação
└── .gitignore                  (opcional, já configurado)
```

**Arquivos necessários:**
- ✅ `app.py` - Interface Gradio
- ✅ `ensemble_híbrido.py` - Lógica de classificação
- ✅ `api_radar.py` - Busca nas APIs do Congresso
- ✅ `requirements.txt` - Dependências Python

**NÃO faça upload de:**
- ❌ `resultados1.md`, `resultados2.md`, `resultadoscompilados.md` (dados locais)
- ❌ `pls_processadas.csv` (dados locais)
- ❌ `processar_pls.py`, `teste_*.py` (scripts auxiliares locais)
- ❌ `GUIA_SWAGGER_SENADO.md`, `testar_endpoint_senado.py` (documentação local)

### 3. Ajustar app.py para Hugging Face

No Space, o `app.launch()` deve ser sem parâmetros ou com configuração específica para Spaces:

```python
if __name__ == "__main__":
    app.launch()
```

Ou se necessário:
```python
if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860)
```

### 4. Verificar requirements.txt

Certifique-se de que contém:
```
gradio>=4.0.0
transformers>=4.30.0
torch>=2.0.0
pandas>=2.0.0
numpy>=1.24.0
tabulate>=0.9.0
protobuf
requests>=2.31.0
```

### 5. README.md do Space

Crie um `README.md` simples e direto:

```markdown
# 🏳️‍🌈 Radar Legislativo LGBTQIA+

Sistema de busca e análise automática de Projetos de Lei relacionados a direitos LGBTQIA+ no Congresso Nacional.

## Como Usar

1. Selecione o período de busca (anos)
2. Escolha as fontes (Câmara dos Deputados e/ou Senado Federal)
3. Defina o limite de resultados
4. Clique em "Buscar e Analisar PLs"

O sistema buscará automaticamente PLs relacionadas a direitos LGBTQIA+ nas APIs oficiais e classificará cada uma como **Favorável**, **Desfavorável** ou **Revisão Necessária**.

## Modelos Utilizados

- **Radar Social LGBTQIA+ V2.1** por [Veronyka](https://huggingface.co/Veronyka/radar-social-lgbtqia-v2.1)
- **IA Feminista AzMina/QuiterIA** por [AzMina](https://huggingface.co/azmina/ia-feminista-bert-posicao)

## Aviso

Este sistema requer revisão humana para decisões finais. Use como ferramenta de apoio, não como decisão automática.
```

### 6. Aguardar Build

O Space vai:
1. Instalar dependências do `requirements.txt`
2. Fazer download dos modelos:
   - `Veronyka/radar-social-lgbtqia-v2.1`
   - `azmina/ia-feminista-bert-posicao`
3. Iniciar o Gradio app

**Tempo estimado**: 5-10 minutos no primeiro build (download dos modelos)

### 7. Testar

1. Acesse a URL do Space: `https://huggingface.co/spaces/[seu-usuario]/radar-legislativo-lgbtqia`
2. Teste buscando PLs:
   - Selecione período: 2020-2024
   - Marque Câmara e/ou Senado
   - Clique em "Buscar e Analisar PLs"
3. Verifique se os resultados aparecem corretamente

## 📝 Checklist Pré-Deploy

- [ ] `app.py` usa `app.launch()` sem parâmetros locais
- [ ] `requirements.txt` tem todas as dependências
- [ ] `README.md` está atualizado com descrição do Space
- [ ] Nomes dos modelos estão corretos
- [ ] Arquivos locais de teste não foram commitados
- [ ] `.gitignore` está configurado (opcional)

## 🔧 Troubleshooting

### Erro: "Model not found"
- Verifique se os nomes dos modelos estão corretos
- Confirme que os modelos são públicos:
  - https://huggingface.co/Veronyka/radar-social-lgbtqia-v2.1
  - https://huggingface.co/azmina/ia-feminista-bert-posicao

### Erro: "Module not found"
- Verifique `requirements.txt` tem todas as dependências
- Garanta que `ensemble_híbrido.py` e `api_radar.py` estão no repositório

### Timeout durante build
- Normal no primeiro build (download dos modelos ~500MB total)
- Aguarde ou verifique logs do build

### Erro de API (Câmara/Senado)
- O Space precisa de conexão com internet para acessar APIs
- Verifique se as URLs das APIs estão corretas em `api_radar.py`

## 🎯 Próximos Passos Após Deploy

1. **Testar com períodos diferentes** (2020-2024, 2015-2020, etc.)
2. **Validar resultados** comparando com PLs conhecidas
3. **Coletar feedback** da comunidade
4. **Monitorar uso** no Space analytics

## 📚 Recursos

- [Documentação Gradio](https://www.gradio.app/docs/)
- [Hugging Face Spaces Docs](https://huggingface.co/docs/hub/spaces)
- [Modelo Radar Social](https://huggingface.co/Veronyka/radar-social-lgbtqia-v2.1)
- [Modelo AzMina](https://huggingface.co/azmina/ia-feminista-bert-posicao)

---

**Boa sorte com o deploy!** 🏳️‍🌈

