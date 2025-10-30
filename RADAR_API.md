# 🔍 Radar Automático de PLs LGBTQIA+

Sistema de busca automática de Projetos de Lei relacionados a direitos LGBTQIA+ nas casas legislativas do Brasil.

## 📋 Funcionalidades

### ✅ Implementado
- **Câmara dos Deputados**: Busca automática via API de Dados Abertos
  - Filtra PLs do ano atual e anterior
  - Busca termos específicos LGBTQIA+ na ementa
  - Análise automática com Ensemble Híbrido

### 🚧 Em Desenvolvimento
- **Senado Federal**: API disponível, implementação em andamento
- **Câmara Municipal de São Paulo**: Verificando disponibilidade de API
- **ALESP (Assembleia Legislativa de SP)**: Verificando disponibilidade de API

## 🎯 Como Usar

### Via Interface Gradio

1. Inicie o app:
   ```bash
   python app.py
   ```

2. Acesse: http://127.0.0.1:7860

3. Vá para a aba **"🔍 Radar Automático"**

4. Configure:
   - **Últimos N dias**: Quantos dias atrás buscar (padrão: 90)
   - **Limite por fonte**: Máximo de PLs por fonte (padrão: 20)

5. Clique em **"🔍 Buscar PLs nas APIs"**

6. O sistema vai:
   - Buscar PLs recentes na Câmara dos Deputados
   - Filtrar por termos LGBTQIA+
   - Analisar cada PL encontrado
   - Mostrar resultados com classificação

### Via Python Direto

```python
from api_radar import buscar_todas_fontes, filtrar_pls_relevantes

# Buscar PLs dos últimos 90 dias
pls = buscar_todas_fontes(dias_atras=90, limite_por_fonte=20)

# Filtrar por relevância
pls_relevantes = filtrar_pls_relevantes(pls, termos_minimos=1)

print(f"Encontradas {len(pls_relevantes)} PLs relevantes")
```

## 🔍 Termos de Busca

### Termos Específicos (Alta Relevância)
- `lgbt`, `lgbtqia`, `trans`, `transgênero`, `transexual`, `travesti`
- `homofobia`, `transfobia`, `homossexual`
- `identidade de gênero`, `orientação sexual`, `diversidade sexual`
- `nome social`, `terapia de conversão`, `cura gay`

### Termos Contextuais (Relevância Média)
- `ideologia de gênero`, `banheiro`, `vestiário`
- `atleta trans`, `esporte feminino`, `competição feminina`
- `linguagem neutra`, `símbolos religiosos.*parada`

**Nota:** Termos contextuais só são aceitos quando combinados com palavras legislativas como "proíbe", "veda", "garante", "reconhece", etc.

## 📊 API da Câmara dos Deputados

**URL Base:** `https://dadosabertos.camara.leg.br/api/v2`

**Endpoint:** `/proposicoes`

**Parâmetros:**
- `siglaTipo`: Tipo de proposição (PL, PLS, PEC, etc)
- `ano`: Ano da proposição
- `itens`: Número de itens por página (máximo recomendado: 100)

**Limitações:**
- Não suporta busca textual direta na API
- Estratégia: buscar PLs recentes e filtrar localmente por termos
- Pode retornar muitos resultados sem filtro

## 🧪 Testando

```bash
# Teste básico de busca
python -c "from api_radar import buscar_camara_deputados; pls = buscar_camara_deputados(limite=5); print(f'Encontradas: {len(pls)} PLs')"

# Teste completo
python -c "from api_radar import buscar_todas_fontes; pls = buscar_todas_fontes(limite_por_fonte=10); print(f'Total: {len(pls)} PLs')"
```

## ⚠️ Limitações Atuais

1. **API da Câmara**: Funciona, mas requer filtragem manual (API não faz busca textual)
2. **Senado**: API disponível, mas estrutura diferente - precisa implementar parser
3. **Câmara SP / ALESP**: Pode não ter API pública - pode precisar de scraping web
4. **Rate Limiting**: Evitar muitas requisições simultâneas (código já tem delay)
5. **Falsos Positivos**: Filtro evita termos ambíguos (ex: "transporte" não é capturado)

## 🚀 Próximos Passos

1. **Implementar Senado Federal**
   - Pesquisar estrutura da API
   - Adaptar parser para formato XML/JSON do Senado

2. **Câmara Municipal de SP**
   - Verificar se há API pública
   - Se não houver, implementar scraping (respeitando ToS)

3. **ALESP**
   - Verificar se há API pública
   - Se não houver, implementar scraping

4. **Melhorias no Filtro**
   - Adicionar mais termos específicos
   - Melhorar detecção de contexto LGBTQIA+
   - Reduzir falsos positivos

5. **Cache de Resultados**
   - Salvar resultados para não buscar repetidamente
   - Atualizar apenas PLs novas

## 📚 Referências

- [API Dados Abertos Câmara](https://dadosabertos.camara.leg.br/swagger/api.html)
- [Dados Abertos Senado](https://www12.senado.leg.br/dados-abertos/conjuntos)
- [Portal LexML](https://www.lexml.gov.br/)

