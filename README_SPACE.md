# 🚀 Guia de Deploy no Hugging Face Spaces

## Passo a Passo

### 1. Duplicar o Space Original (Opcional)

1. Acesse: https://huggingface.co/spaces/Veronyka/radar-social-lgbtqia-v2-analise
2. Clique nos três pontos (⋮) no canto superior direito
3. Selecione "Duplicate this Space"
4. Configure:
   - **Owner**: Seu usuário (Veronyka)
   - **Space name**: `quiteria-analise-pls` (ou outro nome)
   - **Visibility**: Público ou Privado
   - **Hardware**: CPU Standard (ou GPU T4 se tiver acesso)

### 2. Criar Space Novo (Recomendado)

1. Acesse: https://huggingface.co/spaces
2. Clique em "Create new Space"
3. Configure:
   - **Name**: `quiteria-analise-pls`
   - **SDK**: Gradio
   - **Hardware**: CPU Standard
   - **Visibility**: Público

### 3. Upload dos Arquivos

Faça upload destes arquivos para o repositório do Space:

```
📁 quiteria-analise-pls/
├── app.py              ✅ Principal
├── requirements.txt    ✅ Dependências
├── README.md           ✅ Documentação
└── .gitignore          (opcional)
```

**NÃO faça upload de:**
- `resultados1.md`, `resultados2.md` (dados locais)
- `pls_processadas.csv` (pode gerar confusão)
- `processar_pls.py` (script auxiliar local)

### 4. Configurar Variáveis (se necessário)

No menu Settings do Space:
- Não precisa de variáveis de ambiente para este projeto
- Se quiser configurar threshold customizado, pode adicionar via código

### 5. Aguardar Build

O Space vai:
1. Instalar dependências do `requirements.txt`
2. Fazer download do modelo `Veronyka/radar-social-lgbtqia-v2.1`
3. Iniciar o Gradio app

**Tempo estimado**: 3-5 minutos no primeiro build

### 6. Testar

1. Acesse a URL do Space
2. Teste com uma PL conhecida:
   - Cole uma ementa na aba "Análise Individual"
   - Ou use a tabela na aba "Análise em Lote"

## 📝 Checklist Pré-Deploy

- [ ] `app.py` está correto e sem erros
- [ ] `requirements.txt` tem todas as dependências
- [ ] `README.md` está atualizado
- [ ] Modelo está especificado corretamente: `Veronyka/radar-social-lgbtqia-v2.1`
- [ ] Thresholds estão configurados (0.30 e 0.50)

## 🔧 Troubleshooting

### Erro: "Model not found"
- Verifique se o nome do modelo está correto
- Confirme que o modelo existe: https://huggingface.co/Veronyka/radar-social-lgbtqia-v2.1

### Erro: "CUDA out of memory"
- Use `device=-1` no código (CPU)
- Ou diminua batch size

### Build demorando muito
- Normal no primeiro build (download do modelo)
- Modelo tem ~110MB (safetensors)

## 🎯 Próximos Passos

Depois do deploy:

1. **Testar com dados reais** dos 30 PLs coletados
2. **Validar resultados** comparando com classificação manual
3. **Coletar feedback** da comunidade LGBTQIA+
4. **Iterar** melhorias baseadas nos resultados

## 📚 Recursos

- [Documentação Gradio](https://www.gradio.app/docs/)
- [Hugging Face Spaces Docs](https://huggingface.co/docs/hub/spaces)
- [Modelo Radar Social](https://huggingface.co/Veronyka/radar-social-lgbtqia-v2.1)

---

**Boa sorte com o deploy!** 🏳️‍🌈

