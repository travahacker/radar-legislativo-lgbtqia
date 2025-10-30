# ✅ Checklist de Deploy - Radar Legislativo LGBTQIA+

Space criado: https://huggingface.co/spaces/Veronyka/radar-legislativo-lgbtqi

## 📦 Arquivos para Upload no Space

### ✅ OBRIGATÓRIOS (fazer upload)

1. **app.py** ✅
   - Interface Gradio principal
   - Detecta automaticamente ambiente HF Space

2. **ensemble_híbrido.py** ✅
   - Sistema de classificação ensemble
   - Carrega modelos do Hugging Face

3. **api_radar.py** ✅
   - Integração com APIs da Câmara e Senado

4. **requirements.txt** ✅
   - Todas as dependências necessárias

5. **README.md** ✅
   - Documentação do Space

### ❌ NÃO ENVIAR (arquivos locais/debug)

- `resultados1.md`, `resultados2.md`, `resultadoscompilados.md`
- `pls_processadas.csv`
- `processar_pls.py`
- `teste_*.py`
- `GUIA_*.md`
- `testar_*.py`
- `README_SPACE_DEPLOY.md`, `README_SPACE.md` (só local)
- `CHECKLIST_DEPLOY.md` (só local)

## 🚀 Passos para Upload

### Opção 1: Upload Manual (Web Interface)

1. Acesse: https://huggingface.co/spaces/Veronyka/radar-legislativo-lgbtqi
2. Vá para a aba **"Files"**
3. Clique em **"Add file"** → **"Upload file"**
4. Faça upload de cada arquivo:
   - `app.py`
   - `ensemble_híbrido.py`
   - `api_radar.py`
   - `requirements.txt`
   - `README.md`

### Opção 2: Git (Recomendado para futuras atualizações)

```bash
# No diretório do projeto local
cd "/Users/vektra/Desenvolvimento/AzMina QuiterIA"

# Adicionar remote do Space (se ainda não tiver)
git remote add hf-space https://huggingface.co/spaces/Veronyka/radar-legislativo-lgbtqi

# Ou se já tiver, atualizar
git remote set-url hf-space https://huggingface.co/spaces/Veronyka/radar-legislativo-lgbtqi

# Fazer commit dos arquivos necessários
git add app.py ensemble_híbrido.py api_radar.py requirements.txt README.md

# Commit
git commit -m "Initial deploy: Radar Legislativo LGBTQIA+"

# Push para o Space
git push hf-space main
```

**Nota:** Se o Space ainda não tem repositório Git, você precisará inicializar:
```bash
cd /tmp
git clone https://huggingface.co/spaces/Veronyka/radar-legislativo-lgbtqi
cd radar-legislativo-lgbtqi
# Copiar arquivos...
git add .
git commit -m "Initial deploy"
git push
```

## ⏱️ Após Upload

1. **Aguardar Build**: 5-10 minutos na primeira vez
   - Vai baixar os modelos (~500MB total)
   - Instalar dependências

2. **Verificar Logs**: 
   - Clique em **"Logs"** no Space
   - Verifique se há erros

3. **Testar**: 
   - Acesse a interface web do Space
   - Teste uma busca (ex: 2020-2024, Câmara)

## 🔍 Verificações Pós-Deploy

- [ ] Interface carrega sem erros
- [ ] Modelos baixam corretamente
- [ ] Busca na Câmara funciona
- [ ] Busca no Senado funciona (pode retornar 0 - normal se não houver PLs recentes)
- [ ] Classificação aparece corretamente

## 🐛 Troubleshooting

### Erro: "Model not found"
- Verifique se os modelos estão públicos e acessíveis
- Links: 
  - https://huggingface.co/Veronyka/radar-social-lgbtqia-v2.1
  - https://huggingface.co/azmina/ia-feminista-bert-posicao

### Erro: "Module not found"
- Verifique se `requirements.txt` tem todas as dependências
- Confirme que `ensemble_híbrido.py` e `api_radar.py` estão no Space

### Timeout
- Normal no primeiro build (download dos modelos)
- Aguarde e verifique logs

### "No module named 'ensemble_híbrido'"
- Confirme que `ensemble_híbrido.py` está no diretório raiz do Space
- Não deve estar em subpasta

---

**Boa sorte com o deploy!** 🏳️‍🌈

