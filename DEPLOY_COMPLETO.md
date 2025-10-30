# 🚀 Deploy Completo: Radar Legislativo LGBTQIA+

## ✅ Status: CONCLUÍDO

O Radar Legislativo LGBTQIA+ foi clonado do experimento AzMina QuiterIA e deployado com sucesso no Hugging Face Spaces!

## 📋 O Que Foi Feito

### 1. **Clonagem do Projeto**
- ✅ Copiado de `/Users/vektra/Desenvolvimento/AzMina QuiterIA`
- ✅ Destino: `pacote-radar-social-lgbtqia-v2.1/radar-legislativo-lgbtqia/`
- ✅ Excluídos: `__pycache__`, `.git`, `venv`, `pls_processadas.csv`

### 2. **Arquivos Principais Incluídos**
- ✅ `app.py`: Interface Gradio com busca automática
- ✅ `ensemble_híbrido.py`: Lógica de classificação ensemble
- ✅ `api_radar.py`: Integração com APIs do Congresso
- ✅ `requirements.txt`: Dependências Python
- ✅ `README.md`: Documentação completa com YAML metadata
- ✅ `.huggingface.yml`: Configuração do Space

### 3. **Configuração do Space**
```yaml
title: "Radar Legislativo LGBTQIA+ 🏳️‍🌈⚖️"
emoji: "🏳️‍🌈"
sdk: gradio
sdk_version: "4.44.0"
app_file: app.py
license: cc-by-nc-sa-4.0
short_description: "Busca e análise de PLs LGBTQIA+ no Congresso Nacional"
```

### 4. **Deploy no Hugging Face**
- ✅ Repositório Git inicializado
- ✅ Remote adicionado: `https://huggingface.co/spaces/Veronyka/radar-legislativo-lgbtqia`
- ✅ Push realizado com sucesso (force push)
- ✅ Space ativo e funcional

## 🔧 Funcionalidades do Space

### Radar Automático
1. **Busca nas APIs oficiais:**
   - Câmara dos Deputados ✅
   - Senado Federal ✅

2. **Filtros:**
   - Período: 2010-2025 (selecionável)
   - Limite de resultados: 5-100 PLs
   - Fontes: Câmara e/ou Senado

3. **Análise com Ensemble Híbrido:**
   - **Radar Social LGBTQIA+ V2.1** (98.44% recall)
   - **AzMina/QuiterIA** (análise feminista)
   - **Keywords** (termos LGBTQIA+)
   - **Padrões Legislativos** (heurísticas)

4. **Classificação:**
   - **≥50%**: DESFAVORÁVEL
   - **30-50%**: REVISÃO NECESSÁRIA
   - **<30%**: FAVORÁVEL

## 📊 Modelos Utilizados

### Radar Social LGBTQIA+ V2.1
- **Modelo**: `Veronyka/radar-social-lgbtqia-v2.1`
- **Recall**: 98.44%
- **Threshold**: 0.30
- **Base**: 1.891 comentários anotados manualmente

### AzMina/QuiterIA
- **Modelo**: `azmina/ia-feminista-bert-posicao`
- **Função**: Análise feminista de PLs (proxy para LGBTQIA+)

## 🌐 URLs

### Space Principal
```
https://huggingface.co/spaces/Veronyka/radar-legislativo-lgbtqia
```

### Repositório Local
```
/Users/vektra/Desenvolvimento/Radar Social LGBTQIA/pacote-radar-social-lgbtqia-v2.1/radar-legislativo-lgbtqia/
```

### Projeto Original (Experimento)
```
/Users/vektra/Desenvolvimento/AzMina QuiterIA/
```

## 📝 Próximos Passos (Opcional)

### Melhorias Futuras
- [ ] Adicionar cache de resultados
- [ ] Implementar busca por autor/partido
- [ ] Adicionar gráficos de distribuição temporal
- [ ] Exportar resultados em CSV
- [ ] Adicionar histórico de buscas
- [ ] Integrar com Câmara Municipal SP
- [ ] Integrar com ALESP

### Otimizações
- [ ] Reduzir tempo de busca (paralelização)
- [ ] Melhorar filtros de relevância
- [ ] Adicionar mais padrões legislativos
- [ ] Expandir keywords LGBTQIA+

## ⚠️ Avisos Importantes

### Limitações
- **Requer revisão humana**: Classificações são sugestões
- **Contexto limitado**: Não considera histórico completo
- **Modelos não específicos**: Treinados em outros contextos
- **Falsos positivos**: Linguagem técnica pode gerar alertas

### Uso Responsável
- Use como **ferramenta de apoio**, não decisão final
- Sempre **revise manualmente** as classificações
- Considere o **contexto legislativo completo**
- Não use para **decisões automáticas**

## 🎯 Casos de Uso

### Ativistas LGBTQIA+
- Monitorar PLs desfavoráveis em tramitação
- Identificar ameaças aos direitos conquistados
- Mobilizar comunidade contra PLs prejudiciais

### Pesquisadores
- Analisar tendências legislativas
- Mapear posicionamentos de parlamentares
- Estudar evolução de direitos LGBTQIA+

### Jornalistas
- Investigar PLs em tramitação
- Identificar pautas relevantes
- Contextualizar debates legislativos

### ONGs e Coletivos
- Acompanhar agenda legislativa
- Planejar ações de advocacy
- Produzir relatórios de monitoramento

## 📚 Documentação Adicional

### Arquivos de Referência
- `CHECKLIST_DEPLOY.md`: Checklist de deploy
- `PLANO_REVISADO.md`: Plano de desenvolvimento
- `RADAR_API.md`: Documentação das APIs
- `GUIA_SWAGGER_SENADO.md`: Guia da API do Senado
- `termos_radar_social.md`: Termos e keywords
- `resultadoscompilados.md`: Resultados de testes

## 🙏 Agradecimentos

- **AzMina** pelo modelo feminista de análise de PLs
- **Comunidade LGBTQIA+** pela inspiração
- **LabHacker da Câmara** pela inspiração em dados abertos
- **Hugging Face** pela infraestrutura

---

## 🏳️‍🌈 Radar Legislativo LGBTQIA+

*Desenvolvido com ❤️ para a comunidade LGBTQIA+*

**Use como ferramenta de apoio, sempre com revisão humana.** ⚖️

