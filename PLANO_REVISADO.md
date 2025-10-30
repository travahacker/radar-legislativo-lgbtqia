# 🏳️‍🌈 Plano Revisado: QuiterIA Transfeminista

## 📊 Diagnóstico do Problema Atual

### Por que os resultados não foram bons?

1. **Domínio diferente**: Radar Social treinado em Instagram, não em legislação
2. **Linguagem jurídica**: Formal, técnica, sem gírias de ódio explícitas
3. **Contexto ausente**: Modelo não entende implicações políticas, históricas
4. **Viés de gênero**: Modelo AzMina focado em mulheres cis, não em toda comunidade LGBTQIA+

### Dados disponíveis

- ✅ **37 PLs anotadas** (18 favoráveis, 19 desfavoráveis) - arquivo `resultadoscompilados.md`
- ✅ **Modelo AzMina**: `azmina/ia-feminista-bert-posicao` (Favorável/Desfavorável a direitos de mulheres)
- ✅ **Modelo Radar Social**: `Veronyka/radar-social-lgbtqia-v2.1` (Ódio LGBTQIA+ em redes sociais)
- ⚠️ **Limitação**: Dataset pequeno para treinamento direto (ideal: 100-200 PLs)

---

## 🎯 Plano em 3 Fases

### FASE 1: Ensemble Híbrido (2-3 semanas)

**Objetivo**: Combinar os dois modelos existentes de forma inteligente

#### 1.1 Análise por Múltiplos Sinais

Criar um sistema que combina:

```python
# Pseudo-código do ensemble
def classificar_pl_ensemble(pl_texto):
    # Sinal 1: Radar Social (detecção de ódio)
    score_odio = radar_social(pl_texto)
    
    # Sinal 2: AzMina (direitos de mulheres - proxy para transfeminismo)
    score_mulheres = azmina(pl_texto)
    
    # Sinal 3: Palavras-chave específicas LGBTQIA+
    keywords_pro = extract_keywords_pro(pl_texto)
    keywords_anti = extract_keywords_anti(pl_texto)
    
    # Sinal 4: Padrões linguísticos legislativos
    padrao_restritivo = detectar_padroes_restritivos(pl_texto)
    
    # Combinar com pesos aprendidos ou heurísticos
    score_final = (
        0.40 * normalizar(score_odio) +           # 40% - detecção de ódio
        0.30 * normalizar(score_mulheres) +        # 30% - perspectiva feminista
        0.20 * (keywords_anti - keywords_pro) +    # 20% - keywords
        0.10 * padrao_restritivo                    # 10% - padrões
    )
    
    return classificar(score_final)
```

#### 1.2 Keywords LGBTQIA+ Específicas

**Keywords Favoráveis:**
- `identidade de gênero`, `orientação sexual`, `LGBTQIA+`, `diversidade sexual`
- `nome social`, `autodeterminação`, `direitos humanos`
- `discriminação`, `violência`, `proteção` (em contexto positivo)

**Keywords Desfavoráveis:**
- `sexo biológico`, `sexo de nascimento`, `ideologia de gênero`
- `proíbe`, `veda`, `restringe` + termos LGBTQIA+
- `valores familiares`, `proteção à infância` (em contexto anti-LGBTQIA+)

#### 1.3 Padrões Legislativos

Detectar estruturas típicas de PLs desfavoráveis:
- "Define X como Y" onde Y é critério biológico exclusivo
- "Proíbe o ensino de..."
- "Veda o uso de... por pessoas de..."

### FASE 2: Fine-tuning Supervisionado (1-2 meses)

**Objetivo**: Treinar modelo específico para PLs com os dados anotados

#### 2.1 Expandir Dataset (CRÍTICO)

**Atualmente**: 30 PLs (MUITO POUCO para treinamento)

**Necessário**: 
- **Mínimo ideal**: 200-300 PLs anotadas
- **Mínimo viável**: 100 PLs (50/50)
- **Considerando augmentation**: 50 PLs com técnicas de data augmentation

**Como coletar mais PLs:**
1. Buscar PLs similares nos sites do Congresso
2. Organizações LGBTQIA+ podem ter mapeamentos
3. Tentar encontrar datasets públicos de análise legislativa

#### 2.2 Estratégia de Treinamento

**Opção A: Fine-tune do Radar Social**
```python
# Começar do Radar Social (já entende LGBTfobia)
model = AutoModelForSequenceClassification.from_pretrained(
    "Veronyka/radar-social-lgbtqia-v2.1",
    num_labels=2  # FAVORÁVEL / DESFAVORÁVEL
)
# Treinar com PLs anotadas
```

**Opção B: Multi-task Learning**
```python
# Treinar modelo que faz duas tarefas:
# 1. Detecção de ódio (Radar Social)
# 2. Classificação legislativa (AzMina-style)
```

**Opção C: Continuação do AzMina**
```python
# Adaptar modelo AzMina (já entende legislação)
# Expandir de "direitos mulheres" para "direitos LGBTQIA+"
model = AutoModelForSequenceClassification.from_pretrained(
    "azmina/ia-feminista-bert-posicao",
    num_labels=2
)
```

**Recomendação**: Opção A (Fine-tune do Radar Social) porque:
- Já entende LGBTfobia
- Base portuguesa (Tupi-BERT)
- Fácil de adaptar

#### 2.3 Data Augmentation

Para aumentar dataset pequeno:
- **Paráfrase**: Reescrever ementas mantendo sentido
- **Negação controlada**: Criar exemplos adversos
- **Sintaxe variada**: Mudar ordem, estruturas

#### 2.4 Validação Estruturada

- **Treino**: 70% (com augment)
- **Validação**: 15%
- **Teste**: 15%
- **Cross-validation** se dataset < 100 PLs

### FASE 3: Fine-tuning Transfer Learning (Futuro)

**Objetivo**: Modelo final especializado

#### 3.1 Ensemble Ensino-Aprendizagem

Treinar modelo final que aprende dos ensemblers:
1. Ensemble atual (Fase 1) gera "labels suaves"
2. Modelo de fine-tuning aprende desses labels + anotações humanas
3. Iteração até convergência

#### 3.2 Expansão Contínua

- Sistema de feedback: usuários corrigem classificações
- Active learning: identificar PLs que precisam anotação
- Re-treinar periodicamente com novos dados

---

## 📋 Checklist de Implementação

### Fase 1 (Ensemble) - EM ANDAMENTO

- [x] Unificar datasets (`resultadoscompilados.md` - 39 PLs)
- [x] Implementar função de ensemble combinando 4 sinais
- [x] Criar lista inicial de keywords favoráveis/desfavoráveis
- [x] Implementar detecção de padrões legislativos
- [x] Testar ensemble nas 39 PLs anotadas
- [x] Ajustar pesos do ensemble baseado em resultados (keywords: 35%, padrões: 20%)
- [x] Calcular métricas: Precision, Recall, F1 por classe
- [x] Expandir lista de keywords baseado em casos de erro
- [ ] Validar em casos edge (PL 6583, PL 106, PL 906)
- [ ] Criar interface mostrando contribuição de cada sinal

### Fase 2 (Fine-tuning) - Quando tiver 50+ PLs

- [ ] Expandir dataset para pelo menos 50 PLs anotadas
- [ ] Explorar data augmentation
- [ ] Escolher estratégia de fine-tuning (A, B ou C)
- [ ] Configurar ambiente de treinamento (GPU se possível)
- [ ] Treinar modelo piloto
- [ ] Validar em conjunto separado
- [ ] Comparar com ensemble (baseline)

### Fase 3 (Otimização) - Depois do MVP

- [ ] Implementar sistema de feedback
- [ ] Active learning para identificar casos difíceis
- [ ] Pipeline de re-treinamento automático
- [ ] Documentação completa de limitações

---

## 🎯 Métricas de Sucesso

### Fase 1 (Ensemble)

**Mínimo viável:**
- Accuracy >= 70% no conjunto de 30 PLs
- Recall >= 85% para classe DESFAVORÁVEL (prioritário!)
- Precision >= 65% para DESFAVORÁVEL

**Ideal:**
- Accuracy >= 80%
- F1-score >= 75%
- Concordância com anotação humana >= 85%

### Fase 2 (Fine-tuning)

**Mínimo viável:**
- Melhoria de pelo menos 5pp sobre ensemble
- Recall DESFAVORÁVEL >= 90%
- F1-score >= 80%

---

## ⚠️ Riscos e Mitigações

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| Dataset muito pequeno | Alto | Data augmentation + buscar mais PLs |
| Overfitting em treinamento | Médio | Validação rigorosa + early stopping |
| Viés nos dados de treinamento | Alto | Revisar anotações com equipe LGBTQIA+ |
| Modelo não generalizar | Médio | Testar com PLs fora do dataset original |
| Falsos positivos em linguagem técnica | Alto | Threshold conservador + revisão humana sempre |

---

## 📚 Recursos Necessários

### Humanos
- **Anotadores LGBTQIA+**: Validar e expandir dataset
- **Especialistas jurídicos**: Revisar contexto legislativo
- **Engenheiros ML**: Treinamento e validação

### Técnicos
- **GPU**: Para treinamento eficiente (Google Colab Pro ou similar)
- **Storage**: Para dataset e checkpoints
- **Computation**: ~2-4 horas de GPU para fine-tuning

---

## 🚀 Próximos Passos Imediatos

1. **Implementar ensemble híbrido** (Fase 1)
2. **Testar nos 30 PLs** anotadas
3. **Ajustar pesos** baseado em resultados
4. **Documentar erros** e casos de edge
5. **Planejar expansão** do dataset para Fase 2

---

## 💡 Alternativas se Fine-tuning Não For Viável

Se não conseguirmos coletar dados suficientes:

1. **Usar ensemble apenas** como ferramenta de triagem
2. **Focar em explicabilidade**: Por que classificou assim? (SHAP, LIME)
3. **Sistema híbrido humano+IA**: IA sugere, humano decide sempre
4. **Documentação de limitações**: Ser transparente sobre o que funciona e o que não funciona

---

**Última atualização**: 2025-01-XX
**Status**: Fase 1 - Em planejamento

