# 📚 Termos e Padrões Regex do Radar Social LGBTQIA+

Extraídos das versões iniciais do projeto para enriquecer o ensemble híbrido.

## 🔍 Termos LGBTQIA+ Detectados

### Termos Positivos (Contexto de Apoio)
- `orgulho`, `pride`, `amor`, `love`, `respeito`, `respect`
- `beleza`, `beautiful`, `lindo`, `maravilhoso`, `wonderful`
- `coragem`, `courage`, `força`, `strength`, `identidade`, `identity`
- `expressão`, `expression`, `liberdade`, `freedom`, `direito`, `right`
- `aceitar`, `accept`, `embrace`, `celebrar`, `celebrate`
- `apoio`, `support`, `solidariedade`, `solidarity`, `comunidade`, `community`
- `visibilidade`, `visibility`, `representação`, `representation`
- `diversidade`, `diversity`, `inclusão`, `inclusion`, `igualdade`, `equality`

### Termos LGBTQIA+ (Usados em Contexto Negativo = HATE)
- `viado`, `bicha`, `sapatão`, `paneleiro`
- `gay`, `lesbica`, `lésbica`, `bissexual`, `queer`
- `travesti`, `trans`, `transgênero`, `transgenero`
- `lgbt`, `lgbtqia`, `lgbtqia+`

## 🎯 Padrões Regex para Hate Speech

### Padrões de Ódio Explícito
```python
hate_patterns = [
    r'\b(viado|bicha|sapatão|paneleiro|gay|lesbica|bissexual|queer|travesti|trans)\b.*\b(doente|nojento|escroto|desgraçado|de merda)\b',
    r'\b(que porra|que merda|que bosta|que droga)\b',
    r'\b(desgraça|desgraçado|nojento|escroto|filho da puta)\b',
    r'\b(vai se foder|vai tomar no cu|vai pro inferno)\b',
    r'\b(odeio|detesto|repudio|rejeito)\b.*\b(lgbt|gay|lesbica|trans|queer)\b',
    r'\b(palhaçada|palhaçade|ridículo|ridícula|patético|patética)\b'
]
```

### Padrões de Patologização
```python
pathologizing_patterns = [
    r'\b(psiquiatra|psicologo|terapeuta|médico|doutor)\b',
    r'\b(doença|doente|patologia|síndrome|distúrbio|transtorno)\b',
    r'\b(tratamento|terapia|cura|laudo psiquiátrico)\b.*\b(trans|gay|lgbt)\b',
    r'\b(doente mental|doença mental|transtorno mental)\b'
]
```

### Padrões de Moralismo Religioso
```python
religious_patterns = [
    r'\b(jesus|pai|deus|senhor|cristo)\b.*\b(pecado|condenado|inferno|demônio)\b',
    r'\b(pecado|pecador|condenado|inferno|demônio)\b.*\b(lgbt|gay|trans)\b',
    r'\b(igreja|bíblia|cristão|pastor|padre)\b.*\b(pecado|errado|proibido)\b'
]
```

### Padrões de Redução Anatômica
```python
anatomical_patterns = [
    r'\b(homem com buceta|mulher com pênis)\b',
    r'\b(genitália|genital|órgão sexual|parte íntima)\b',
    r'\b(é só|nada mais que|apenas|somente)\b.*\b(pênis|buceta|vagina)\b'
]
```

### Padrões de Linguagem Neutra (Ódio)
```python
neutral_language_hate_patterns = [
    r'\b(todes|lules|mussum|linguagem neutra)\b.*\b(porcarie|nojento|escroto|desgraçado)\b',
    r'\b(modinha|frescura|babaquice)\b.*\b(todes|lules|linguagem neutra)\b',
    r'\b(fim da picada|chega|basta)\b.*\b(todes|lules|linguagem neutra)\b',
    r'\btodes\b.*\b(meu|meus)\b.*\b(ovo|ovos|oves|egg|eggs)\b',  # Machismo disfarçado
    r'\b(proíbe|veda)\b.*\b(linguagem neutra|todes|lules)\b'
]
```

### Padrões de Machismo
```python
machismo_patterns = [
    r'\b(meu|meus)\b.*\b(ovo|ovos|oves|egg|eggs|roles|rola|pinto)\b',
    r'\b(ovo|ovos|oves|egg|eggs|roles|rola|pinto)\b.*\b(meu|meus)\b',
    r'\b(vai lavar louça|vai cozinhar|vai cuidar da casa|mulher tem que)\b'
]
```

### Padrões de Ridicularização
```python
ridicule_patterns = [
    r'\b(engraçado|hilário|hilariante|cômico|ridículo)\b.*\b(trans|gay|lgbt)\b',
    r'\b(zoar|zombar|rir de|rindo de|piada)\b.*\b(trans|gay|lgbt)\b',
    r'\b(brincadeira|zoação|zoeira)\b.*\b(trans|gay|lgbt)\b'
]
```

### Padrões de Palavrões (Contexto de Hate)
```python
curse_words_hate = [
    r'\b(bosta|merda|porra|caralho)\b.*\b(trans|gay|lgbt|viado|bicha)\b',
    r'\b(viado|bicha|gay|trans)\b.*\b(bosta|merda|porra|caralho)\b',
    r'\b(filho da puta|filha da puta|arrombado)\b.*\b(trans|gay|lgbt)\b'
]
```

### Padrões de Emojis Negativos
```python
negative_emoji_patterns = [
    r'😂+.*\b(trans|gay|lgbt|viado|bicha|nojo|asco)\b',
    r'\b(trans|gay|lgbt)\b.*😂+',
    r'🤢🤮|🤮🤢',  # Emojis de vômito
    r'😈|👹|👺|💀|☠️',  # Emojis de demônio/morte
    r'🤡.*\b(trans|gay|lgbt)\b',  # Emoji de palhaço
]
```

### Padrões de Comandos Condescendentes
```python
condescending_patterns = [
    r'\b(vai estudar|vai trabalhar|vai procurar o que fazer)\b',
    r'\b(vai cuidar da sua vida|vai se ocupar)\b',
    r'\b(vai ler um livro|vai se informar)\b',
    r'\b(vai se tratar|vai procurar ajuda)\b.*\b(trans|gay|lgbt)\b'
]
```

### Padrões de Shame/Vergonha
```python
shame_patterns = [
    r'\b(vergonha|vergonhoso|vergonhosa)\b.*\b(trans|gay|lgbt)\b',
    r'\b(sem vergonha|desvergonhado)\b',
    r'\b(envergonhado|atrevido|ousado)\b.*\b(trans|gay|lgbt)\b'
]
```

## 🔄 Contexto Positivo (NÃO é Hate)

### Indicadores de Contexto Positivo
```python
positive_context_patterns = [
    r'\b(meu|minha|nosso|nossa)\b.*\b(bar|restaurante|local|lugar|favorito|preferido)\b.*\b(sapatão|gay|lgbt)\b',
    r'\b(amo|adoro|gosto|aprecio|respeito|apoio|defendo)\b.*\b(lgbt|gay|trans)\b',
    r'\b(orgulho|pride|diversidade|inclusão|igualdade)\b',
    r'\b(comunidade|grupo|coletivo|movimento)\b.*\b(lgbt|gay|trans)\b',
    r'\b(direitos|direito de ser|vivência|identidade)\b.*\b(trans|gay|lgbt)\b',
    r'\b(visibilidade|representação|aceitação|tolerância)\b',
    r'\b(sapatão|gay|lesbica|trans)\b.*\b(favorito|preferido|legal|bom|ótimo)\b'
]
```

### Emojis Positivos
```python
positive_emojis = [
    '❤️', '🧡', '💛', '💚', '💙', '💜', '🖤', '🤍', '🤎',
    '💕', '💖', '💗', '💘', '🏳️‍⚧️', '🏳️‍🌈', '⚧️',
    '🔥', '🌶️', '👏', '🙌', '💪', '✨', '🌟', '⭐', '💫', '🎉', '🎊', '🌈', '🦄'
]
```

## 🎯 Padrões para Análise Legislativa

Adaptando termos do Radar Social para contexto de PLs:

### Termos Legislativos Favoráveis (Adaptados)
```python
legislative_positive_keywords = [
    r'criminaliza.*(homofobia|transfobia|lgbtfobia)',
    r'protege.*(orientação.*sexual|identidade.*gênero)',
    r'garante.*(direito|direitos).*(lgbt|trans|gay)',
    r'reconhece.*(identidade.*gênero|nome.*social)',
    r'inclui.*(orientação.*sexual|identidade.*gênero)',
    r'equipara.*(terapia.*conversão|cura.*gay).*tortura',
    r'estatuto.*diversidade',
    r'autodeterminação.*gênero',
    r'proíbe.*terapias.*conversão',  # Proibir = favorável
    r'visibilidade.*(lgbt|trans|diversidade)',
    r'cria.*mecanismos.*proteção.*(lgbt|trans)'
]
```

### Termos Legislativos Desfavoráveis (Adaptados)
```python
legislative_negative_keywords = [
    r'proíbe.*(gênero|orientação.*sexual|lgbt)',
    r'veda.*(gênero|lgbt|trans)',
    r'restringe.*(gênero|trans|lgbt)',
    r'define.*(sexo|gênero).*biológ',
    r'critério.*exclusivo.*sexo',
    r'separar.*por.*sexo',
    r'exclusivamente.*(homem|mulher).*(cis|biológ)',
    r'ideologia.*gênero',
    r'valores.*familiares.*educação',
    # Do Radar Social adaptados
    r'valores.*(cristão|religioso|bíblico).*educação',
    r'sagrado.*família',
    r'família.*tradicional',
    r'proteção.*infância.*gênero',  # Pode ser usado anti-LGBTQIA+
    r'restringe.*acesso.*(trans|lgbt).*espaço',
    r'veda.*visibilidade.*(lgbt|gay|trans)'
]
```

### Termos de Patologização (Adaptados para Legislação)
```python
pathologizing_legislative = [
    r'terapias.*conversão',  # Se não está proibindo, pode ser desfavorável
    r'cura.*gay',
    r'reparação.*sexual',
    r'tratamento.*orientação',
    r'laudo.*psiquiátrico.*trans',
    r'doença.*mental.*(trans|gay|lgbt)',
    r'transtorno.*(identidade|orientação)',
    r'desvio.*(sexual|gênero)',
    r'anormalidade.*(sexual|gênero)'
]
```

### Contexto Positivo (Adaptado para Legislação)
```python
# Quando uma PL menciona termos LGBTQIA+ mas em contexto de proteção
positive_legislative_context = [
    r'garante.*(direito|direitos).*(lgbt|trans|gay|orientação)',
    r'protege.*contra.*violência.*(lgbt|trans|gay)',
    r'reconhece.*(identidade|vivência|expressão)',
    r'cria.*mecanismos.*proteção',
    r'visibilidade.*(lgbt|trans|diversidade)',
    r'inclusão.*(lgbt|trans|diversidade)',
    r'comunidade.*(lgbt|trans|diversidade).*direitos',
    r'respeito.*(identidade|vivência|expressão).*gênero'
]
```

## 💡 Recomendações para Ensemble

### Para Adicionar ao Ensemble Híbrido:

1. **Expandir keywords desfavoráveis** com termos do Radar Social que fazem sentido em contexto legislativo:
   - Termos de moralismo religioso (se aparecerem em PLs)
   - Termos de patologização (terapias de conversão)
   - **Nota importante**: "proíbe terapias de conversão" = FAVORÁVEL, mas "legaliza terapias de conversão" ou "terapias de conversão" sem contexto = DESFAVORÁVEL

2. **Adicionar detecção de contexto positivo** para evitar falsos positivos:
   - Quando PL menciona "lgbt" mas em contexto de proteção/garantia de direitos
   - Distinguir entre "proíbe X" (onde X é discriminação) vs "proíbe Y" (onde Y é direitos)

3. **Detecção de padrões específicos legislativos**:
   - "Define X como Y" onde Y é restritivo
   - "Proíbe ensino de..." relacionado a gênero/LGBTQIA+
   - "Veda uso de..." por critério LGBTQIA+

4. **Termos-chave adicionais do Radar Social adaptados**:
   - `terapias de conversão`, `cura gay`, `reparação` (desfavorável, a menos que esteja proibindo)
   - `ideologia de gênero`, `família tradicional` (desfavorável)
   - `proteção da infância` (pode ser usado anti-LGBTQIA+)
   - `valores cristãos/bíblicos` em educação (desfavorável)

5. **Contextualização importante**:
   - Palavra-chave: "PROÍBE" pode ser favorável (se proíbe discriminação) ou desfavorável (se proíbe direitos)
   - Precisamos analisar o objeto da proibição, não apenas a palavra "proíbe"

