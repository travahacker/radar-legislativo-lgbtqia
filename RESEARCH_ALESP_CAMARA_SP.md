# 🔍 Pesquisa: APIs ALESP e Câmara Municipal de São Paulo

**Data da pesquisa**: Outubro 2025

## 📋 Resumo Executivo

Após investigação detalhada, a situação das APIs/dados abertos é:

### ✅ ALESP (Assembleia Legislativa de São Paulo) - IMPLEMENTADO

**Status**: **✅ Portal encontrado e implementado!**

- **Portal Correto**: https://www.al.sp.gov.br/dados-abertos/
- **Arquivo de Proposituras**: https://www.al.sp.gov.br/repositorioDados/processo_legislativo/proposituras.zip
- **Formato**: ZIP contendo XML com todas as proposituras (253.496 proposituras!)
- **Tamanho**: ~16MB ZIP, ~115MB XML descompactado
- **Atualização**: Diária
- **Última atualização**: 29-10-2025 21:26:06

**Implementação:**
- Função `buscar_alesp()` implementada em `api_radar.py`
- Baixa arquivo ZIP, extrai XML, parseia e filtra por termos LGBTQIA+
- Integrada no `app.py` com checkbox para ativar/desativar
- Testada e funcionando: encontrou 10 PLs relevantes em teste (2020-2024)

**Performance:**
- Download do ZIP: ~5-10 segundos
- Parse do XML: ~5-8 segundos
- Total: ~10-20 segundos para busca completa

**Nota**: O arquivo contém TODAS as proposituras históricas. Filtro por ano é aplicado após download para otimizar processamento.

### ✅ Câmara Municipal de São Paulo - WEB SERVICE PÚBLICO ENCONTRADO E IMPLEMENTADO!

**Status**: **✅ Web Service público funcionando sem autenticação!**

- **Portal de Dados Abertos**: https://www.saopaulo.sp.leg.br/transparencia/dados-abertos/dados-disponibilizados-em-formato-aberto/
- **Web Service Público**: https://splegisws.saopaulo.sp.leg.br/ws/ws2.asmx ✅
- **Método Principal**: `ProjetosPorAnoJSON` ✅ (funcionando, retorna JSON!)
- **SPLEGIS Consulta (Interface Web)**: https://splegisconsulta.saopaulo.sp.leg.br/
- **Base legal**: Ato da Mesa nº 1156/2011
- **Resultado da investigação**:
  - ✅ Portal de dados abertos listou o web service SPLEGIS
  - ✅ **Web Service PÚBLICO** (`splegisws.saopaulo.sp.leg.br/ws/ws2.asmx`) **funcionando sem autenticação!**
  - ✅ Método `ProjetosPorAnoJSON` retorna todos os projetos de um ano (ex: 18.929 projetos em 2020)
  - ✅ Testado e funcionando: encontrou 10 PLs relevantes em teste (2020-2024)

**Links relevantes encontrados no portal:**
- Menu menciona "Projetos Apresentados (desde 1948)" na seção "Atividade Legislativa"
- Portal menciona Programa de Dados Abertos do Parlamento
- Referências a formato aberto (Open Knowledge Foundation, W3C)

**Estrutura identificada:**
- **Web Service Público** (`ws2.asmx`) com múltiplos métodos JSON
- **Método principal**: `ProjetosPorAnoJSON` - retorna todos os projetos de um ano
- **Métodos disponíveis**: `ProjetosPorAnoJSON`, `ProjetoResumoJSON`, `ProjetosAssuntosJSON`, etc.
- Interface web SPLEGIS Consulta também disponível

**Implementação:**
- ✅ Função `buscar_camara_sao_paulo()` implementada em `api_radar.py`
- ✅ Usa método `ProjetosPorAnoJSON` para buscar projetos por ano
- ✅ Filtra localmente por termos LGBTQIA+ na ementa
- ✅ Integrada no `app.py` com checkbox para ativar/desativar
- ✅ Testada e funcionando: encontrou 10 PLs relevantes em teste (2020-2024)

**Performance:**
- Busca por ano: ~2-5 segundos por ano
- Filtro local: ~1-3 segundos (depende do número de projetos - pode ter 20k+ por ano)
- Total: ~5-15 segundos para busca completa (1-2 anos)

**Nota**: O método retorna TODOS os projetos do ano (ex: 18.929 em 2020). O filtro por termos LGBTQIA+ é aplicado localmente após o download.

**Observações técnicas:**
- Site usa WordPress (wp-includes detectado)
- Possui proteção Cloudflare/proteção anti-bot
- Requer navegador real ou user-agent completo para acesso

### ✅ Portal Prefeitura SP (CKAN) - Funcionando

**Status**: **API CKAN disponível e funcionando**

- Portal: https://dados.prefeitura.sp.gov.br
- API CKAN: https://dados.prefeitura.sp.gov.br/api/3
- **Resultado**: ✅ API funcionando, 271 datasets encontrados

**Próximos passos:**
1. Explorar quais datasets contêm informações legislativas
2. Verificar se há dados de projetos de lei/proposições
3. Implementar busca via API CKAN padrão

## 🔧 Implementação Realizada

### Funções Atualizadas em `api_radar.py`

#### `buscar_alesp()` 
- Status: Retorna lista vazia com mensagem informativa
- Motivo: Portal não acessível publicamente
- Próxima ação: Requer verificação manual

#### `buscar_camara_sao_paulo()`
- Status: Retorna lista vazia com mensagem informativa
- Motivo: API REST não documentada publicamente
- Próxima ação: Implementar Opção A (downloads) ou Opção B (scraping controlado)

#### `buscar_ckan_prefeitura_sp()` (TODO)
- Status: Não implementado
- Prioridade: Baixa (verificar se há dados legislativos relevantes)

## 📝 Links Verificados

### ALESP
- ❌ https://dadosabertos.alesp.gov.br (não resolve)
- ❌ https://dadosabertos.alesp.gov.br/swagger (não resolve)
- ✅ https://www.alesp.sp.gov.br (site oficial - requer verificação manual)

### Câmara Municipal SP
- ✅ https://www.camara.sp.gov.br/transparencia/dados-abertos/ (portal existe)
- ✅ https://www.camara.sp.gov.br (site oficial)

### Prefeitura SP
- ✅ https://dados.prefeitura.sp.gov.br (portal CKAN funcionando)
- ✅ https://dados.prefeitura.sp.gov.br/api/3 (API CKAN funcionando)

## 🎯 Recomendações de Priorização

### Alta Prioridade: Câmara Municipal SP
**Por quê:**
- Portal existe e é oficial
- Provavelmente tem dados disponíveis (mesmo que não via API)
- Impacto alto (é nível municipal, complementa o escopo federal/estadual)

**Ação recomendada:**
1. Explorar o portal manualmente no navegador
2. Verificar se há seção de "downloads" ou arquivos CSV/XML
3. Se houver, implementar função de download e parser
4. Se não houver, considerar scraping controlado da listagem de proposições

### Média Prioridade: ALESP
**Por quê:**
- Portal mencionado mas não acessível
- Pode ser que tenha sido migrado ou esteja em manutenção
- Impacto médio (complementa federal, mas estadual já está parcialmente coberto)

**Ação recomendada:**
1. Contatar ALESP via email/telefone para verificar status
2. Verificar site oficial para downloads manuais
3. Monitorar futuras atualizações do portal

### Baixa Prioridade: Portal Prefeitura SP
**Por quê:**
- CKAN funcionando, mas pode não ter dados legislativos
- Impacto baixo (dados podem ser de outros órgãos municipais)

**Ação recomendada:**
1. Explorar datasets do CKAN procurando por "legislacao", "camara", "projetos"
2. Se encontrar dados relevantes, implementar busca via API CKAN

## 🧪 Testes Realizados

### ALESP
- ❌ DNS não resolve para `dadosabertos.alesp.gov.br`
- ❌ Site oficial também não resolve (`www.alesp.sp.gov.br`)
- ❌ Variações de URL testadas, nenhuma funcionou

### Câmara Municipal SP
- ⚠️ Portal acessível, mas certificado SSL com problema
- ⚠️ Não testado via scraping (requer verificação de ToS)

### Prefeitura SP CKAN
- ✅ API CKAN responde (200 OK)
- ✅ 271 datasets encontrados
- ✅ Estrutura CKAN padrão confirmada

## 📚 Referências

- CKAN API Documentation: https://docs.ckan.org/en/2.9/api/
- Câmara Municipal SP - Ato da Mesa 1156/2011
- Portal Dados Abertos Prefeitura SP: https://dados.prefeitura.sp.gov.br

---

**Conclusão**: Focar em Câmara Municipal SP como próxima implementação. ALESP requer contato direto ou verificação manual futura.
