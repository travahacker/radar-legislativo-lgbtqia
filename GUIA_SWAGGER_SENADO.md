# 🔍 Guia de Verificação - Swagger API do Senado

## 📚 Links Importantes

- **Swagger UI**: https://legis.senado.leg.br/dadosabertos/api-docs/swagger-ui/index.html
- **Portal de Dados Abertos**: https://www12.senado.leg.br/dados-abertos
- **Documentação**: https://legis.senado.leg.br/dadosabertos

## 🎯 O Que Procurar

### 1. Endpoints de Busca de Matérias

Procurar por métodos relacionados a:
- `listaMateriasTramitando` (mencionado no link anterior)
- `materias`
- `buscar`
- `listagem`
- `search`

### 2. Verificar Parâmetros

Quando encontrar um endpoint promissor, verificar:
- ✅ **Parâmetros aceitos**: `ano`, `sigla`, `texto`, `dataInicio`, `dataFim`
- ✅ **Método HTTP**: GET, POST
- ✅ **Formato de resposta**: JSON, XML
- ✅ **Exemplo de resposta**: estrutura dos dados retornados

### 3. Testar no Swagger UI

1. Abrir o Swagger UI no navegador
2. Expandir a seção de **MateriaService** ou similar
3. Procurar pelo método `listaMateriasTramitando`
4. Clicar em "Try it out"
5. Preencher parâmetros (ex: `ano: 2024`, `sigla: PLS`)
6. Executar e ver a resposta
7. Copiar o **endpoint completo** mostrado (ex: `/dadosabertos/api/v2/materia/...`)

## 📝 Checklist de Verificação

- [ ] Acessei o Swagger UI
- [ ] Encontrei seção de matérias/proposições
- [ ] Identifiquei endpoint `listaMateriasTramitando` ou similar
- [ ] Testei no Swagger UI com parâmetros: `ano=2024`, `sigla=PLS`
- [ ] Recebi resposta JSON válida
- [ ] Anotei o endpoint completo (URL base + path)
- [ ] Anotei os parâmetros aceitos
- [ ] Verifiquei estrutura da resposta

## 💾 Quando Encontrar o Endpoint

**Copie aqui:**
- Endpoint completo: `https://legis.senado.leg.br/dadosabertos/...`
- Parâmetros aceitos: `ano`, `sigla`, etc.
- Exemplo de resposta JSON:

```json
{
  "exemplo": "estrutura da resposta"
}
```

## 🧪 Script de Teste

Depois de identificar o endpoint, execute:

```bash
python testar_endpoint_senado.py
```

Ou teste diretamente:

```python
import requests

# Substituir pelo endpoint encontrado
url = "https://legis.senado.leg.br/dadosabertos/[ENDPOINT_ENCONTRADO]"
params = {
    "ano": 2024,
    "sigla": "PLS"
}
headers = {"Accept": "application/json"}

response = requests.get(url, params=params, headers=headers)
print(f"Status: {response.status_code}")
print(f"Resposta: {response.json()}")
```

