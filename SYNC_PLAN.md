# 🔄 Plano de Sincronização: Experimento → Space Deployado

## 📊 Mudanças Detectadas no Experimento Original

### 1. **app.py** - Mudanças Significativas
- ✅ **Novas fontes**: Adicionadas ALESP e Câmara Municipal SP
- ✅ **Melhor UX**: Campos com `interactive=True`, ano final dinâmico
- ✅ **Mais checkboxes**: 4 fontes (Câmara, Senado, ALESP, Câmara SP)
- ✅ **Debug melhorado**: Prints de debug adicionados
- ✅ **Descrições atualizadas**: Menciona todas as 4 fontes

### 2. **ensemble_híbrido.py** - Fix Crítico
- ✅ **Fix do AzMina**: Carrega tokenizer do modelo base (neuralmind/bert-base-portuguese-cased)
- ✅ **Fallback**: Sistema funciona mesmo se AzMina falhar
- ✅ **Pesos adaptativos**: Redistribui pesos se AzMina não carregar
- 🔥 **CRÍTICO**: Resolve erro de carregamento do modelo AzMina

### 3. **api_radar.py** - Expansão Massiva
- ✅ **Termos expandidos**: +20 novos termos LGBTQIA+
- ✅ **ALESP implementada**: Busca na Assembleia Legislativa de SP
- ✅ **Câmara SP implementada**: Busca na Câmara Municipal de SP
- ✅ **Senado melhorado**: Endpoint `/materia/pesquisa/lista` (mais robusto)
- ✅ **XML parsing**: Suporte a XML do Senado
- 🔥 **IMPORTANTE**: Implementações completas de ALESP e Câmara SP

## 🎯 Estratégia de Sincronização

### Opção Recomendada: Rsync Seletivo + Git

```bash
# 1. Backup do atual (segurança)
cd "/Users/vektra/Desenvolvimento/Radar Social LGBTQIA/pacote-radar-social-lgbtqia-v2.1"
cp -r radar-legislativo-lgbtqia radar-legislativo-lgbtqia-backup

# 2. Sync dos arquivos principais
rsync -av --exclude='__pycache__' --exclude='*.pyc' --exclude='.git' \
  "/Users/vektra/Desenvolvimento/AzMina QuiterIA/app.py" \
  "/Users/vektra/Desenvolvimento/AzMina QuiterIA/ensemble_híbrido.py" \
  "/Users/vektra/Desenvolvimento/AzMina QuiterIA/api_radar.py" \
  "radar-legislativo-lgbtqia/"

# 3. Git diff para revisar
cd radar-legislativo-lgbtqia
git diff

# 4. Se tudo ok, commit e push
git add app.py ensemble_híbrido.py api_radar.py
git commit -m "🔄 Sync: Fix AzMina + ALESP + Câmara SP + UX melhorada"
git push origin main
```

## 📋 Checklist de Mudanças

### Arquivos para Sincronizar
- [x] `app.py` ⭐ (novas fontes + UX)
- [x] `ensemble_híbrido.py` ⭐⭐⭐ (fix crítico AzMina)
- [x] `api_radar.py` ⭐⭐ (ALESP + Câmara SP implementadas)

### Arquivos Opcionais
- [ ] `requirements.txt` (verificar se precisa atualizar)
- [ ] README/docs (atualizar mencionando novas fontes)

### Validações Necessárias
- [ ] Testar carregamento do AzMina (não deve dar erro)
- [ ] Testar busca na Câmara (deve funcionar)
- [ ] Testar busca no Senado (endpoint novo)
- [ ] Testar busca na ALESP (nova implementação)
- [ ] Testar busca na Câmara SP (nova implementação)

## 🚨 Pontos de Atenção

### 1. Fix do AzMina é CRÍTICO
O modelo AzMina estava falhando ao carregar porque não tem `tokenizer_config.json`. 
A nova versão:
- Carrega explicitamente o tokenizer do modelo base
- Tem fallback se ainda assim falhar
- Redistribui pesos se AzMina não estiver disponível

**Status atual no Space**: Provavelmente está falhando sem esse fix

### 2. Novas Fontes (ALESP + Câmara SP)
Implementações completas com:
- Parsing de XML (Senado, ALESP)
- Estrutura de dados padronizada
- Tratamento de erros robusto

**Benefício**: Cobertura legislativa municipal e estadual (SP)

### 3. Termos LGBTQIA+ Expandidos
+20 novos termos incluindo:
- Identidades: bissexual, pansexual, não-binário
- Direitos: casamento igualitário, adoção homoafetiva
- Procedimentos: mudança de nome, retificação de registro

**Benefício**: Captura mais PLs relevantes

## 📈 Impacto Esperado Após Sync

### Performance
- ✅ AzMina carrega sem erro (fix crítico)
- ✅ Mais PLs encontradas (termos expandidos)
- ✅ Mais fontes disponíveis (4 vs 2)

### User Experience
- ✅ Campos interativos (sliders respondem melhor)
- ✅ Ano final dinâmico (sempre ano atual)
- ✅ 4 checkboxes (mais opções de busca)
- ✅ Descrições claras sobre cada fonte

### Cobertura
- 📊 **Antes**: Câmara + Senado (federal)
- 📊 **Depois**: Câmara + Senado + ALESP + Câmara SP (federal + estadual + municipal)

## ⚙️ Execução do Sync

### Método Automático (Recomendado)
```bash
cd "/Users/vektra/Desenvolvimento/Radar Social LGBTQIA/pacote-radar-social-lgbtqia-v2.1/radar-legislativo-lgbtqia"

# Copiar arquivos atualizados
cp "/Users/vektra/Desenvolvimento/AzMina QuiterIA/app.py" .
cp "/Users/vektra/Desenvolvimento/AzMina QuiterIA/ensemble_híbrido.py" .
cp "/Users/vektra/Desenvolvimento/AzMina QuiterIA/api_radar.py" .

# Revisar mudanças
git diff

# Commit
git add app.py ensemble_híbrido.py api_radar.py
git commit -m "🔄 Sync do experimento: Fix AzMina + ALESP + Câmara SP + UX melhorada

- Fix crítico: Carregamento do modelo AzMina com tokenizer explícito
- Novas fontes: ALESP e Câmara Municipal SP implementadas
- Termos expandidos: +20 novos termos LGBTQIA+
- UX melhorada: campos interativos, ano final dinâmico
- API Senado: endpoint mais robusto (/materia/pesquisa/lista)"

# Push para HF Space
git push origin main
```

### Método Manual (Mais Controle)
1. Abrir cada arquivo lado a lado
2. Copiar mudanças manualmente
3. Testar localmente antes de commit
4. Commit e push

## 🧪 Teste Local Antes de Deploy

```bash
cd "/Users/vektra/Desenvolvimento/Radar Social LGBTQIA/pacote-radar-social-lgbtqia-v2.1/radar-legislativo-lgbtqia"

# Instalar/atualizar dependências
pip install -r requirements.txt

# Testar app
python app.py

# Verificar:
# 1. AzMina carrega sem erro
# 2. Interface mostra 4 checkboxes
# 3. Busca funciona em todas as fontes
```

## 📝 Atualizar Documentação

Após sync, atualizar:
- [ ] `README.md`: Mencionar ALESP e Câmara SP
- [ ] `DEPLOY_COMPLETO.md`: Adicionar novas fontes
- [ ] Card do Space: Atualizar descrição

---

**Recomendação**: Executar sync automático agora, é safe e traz melhorias críticas! 🚀


