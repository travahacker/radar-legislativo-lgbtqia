"""
Teste da função de processamento de MD do Perplexity
"""
from app import processar_md_perplexity
import os

# Criar um objeto mock de arquivo
class MockFile:
    def __init__(self, path):
        self.name = path

# Testar com resultados2.md
arquivo_teste = MockFile("resultados2.md")

if os.path.exists("resultados2.md"):
    print("🧪 Testando processamento de resultados2.md...\n")
    resultado = processar_md_perplexity(arquivo_teste)
    print(resultado)
    print("\n✅ Teste concluído!")
else:
    print("❌ Arquivo resultados2.md não encontrado")

