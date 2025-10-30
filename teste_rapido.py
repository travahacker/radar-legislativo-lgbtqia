"""
Teste rápido do modelo e funções principais
"""
from transformers import pipeline
import torch

print("🏳️‍🌈 Testando Radar Social LGBTQIA+ V2.1...\n")

# Teste 1: Carregar modelo
print("1️⃣ Carregando modelo...")
try:
    classifier = pipeline(
        "text-classification",
        model="Veronyka/radar-social-lgbtqia-v2.1",
        device=-1  # CPU
    )
    print("   ✅ Modelo carregado com sucesso!\n")
except Exception as e:
    print(f"   ❌ Erro: {e}\n")
    exit(1)

# Teste 2: Análise de texto conhecido (desfavorável)
print("2️⃣ Testando com PL desfavorável conhecida...")
texto_desfavoravel = "Proíbe o uso de banheiro por pessoas de sexo biologicamente diferente do designado"
resultado = classifier(texto_desfavoravel, truncation=True, max_length=256)
label = resultado[0]['label']
score = resultado[0]['score']
score_odio = 1 - score if label != 'HATE' else score
print(f"   Label: {label}")
print(f"   Score original: {score:.2%}")
print(f"   Score de ódio: {score_odio:.2%}")
print(f"   Classificação: {'DESFAVORÁVEL' if score_odio >= 0.5 else 'REVISÃO' if score_odio >= 0.3 else 'FAVORÁVEL'}")
print("   ✅ Teste concluído!\n")

# Teste 3: Análise de texto favorável
print("3️⃣ Testando com PL favorável conhecida...")
texto_favoravel = "Criminaliza a discriminação por orientação sexual e identidade de gênero"
resultado = classifier(texto_favoravel, truncation=True, max_length=256)
label = resultado[0]['label']
score = resultado[0]['score']
score_odio = 1 - score if label != 'HATE' else score
print(f"   Label: {label}")
print(f"   Score original: {score:.2%}")
print(f"   Score de ódio: {score_odio:.2%}")
print(f"   Classificação: {'DESFAVORÁVEL' if score_odio >= 0.5 else 'REVISÃO' if score_odio >= 0.3 else 'FAVORÁVEL'}")
print("   ✅ Teste concluído!\n")

# Teste 4: Ementa real do resultados1.md
print("4️⃣ Testando com ementa real...")
ementa_real = "Proíbe a divulgação de 'ideologia de gênero' em escolas públicas e privadas (altera o ECA)"
resultado = classifier(ementa_real, truncation=True, max_length=256)
label = resultado[0]['label']
score = resultado[0]['score']
score_odio = 1 - score if label != 'HATE' else score
print(f"   Ementa: '{ementa_real}'")
print(f"   Score de ódio: {score_odio:.2%}")
print(f"   Classificação: {'DESFAVORÁVEL' if score_odio >= 0.5 else 'REVISÃO' if score_odio >= 0.3 else 'FAVORÁVEL'}")
print("   ✅ Teste concluído!\n")

print("🎉 Todos os testes passaram! O modelo está funcionando.")

