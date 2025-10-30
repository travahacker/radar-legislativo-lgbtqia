"""
Script auxiliar para processar o arquivo resultados1.md e criar CSV
"""
import pandas as pd
import re

def processar_resultados_md(arquivo_md: str) -> pd.DataFrame:
    """Converte tabela markdown em DataFrame"""
    with open(arquivo_md, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    # Pular linhas iniciais até encontrar tabela
    dados = []
    em_tabela = False
    
    for linha in linhas:
        linha = linha.strip()
        
        # Detectar início da tabela
        if linha.startswith('|') and 'Nº' in linha:
            em_tabela = True
            headers = [h.strip() for h in linha.split('|')[1:-1]]
            continue
        
        # Pular separador de tabela
        if em_tabela and linha.startswith('|---'):
            continue
        
        # Processar linhas de dados
        if em_tabela and linha.startswith('|') and not linha.startswith('| Nº'):
            valores = [v.strip() for v in linha.split('|')[1:-1]]
            if len(valores) == len(headers):
                dados.append(dict(zip(headers, valores)))
    
    df = pd.DataFrame(dados)
    return df

def salvar_csv(df: pd.DataFrame, arquivo_csv: str):
    """Salva DataFrame como CSV"""
    df.to_csv(arquivo_csv, index=False, encoding='utf-8')
    print(f"✅ Arquivo salvo: {arquivo_csv}")
    print(f"   Total de PLs: {len(df)}")

if __name__ == "__main__":
    # Processar resultados1.md
    try:
        df = processar_resultados_md("resultados1.md")
        salvar_csv(df, "pls_processadas.csv")
        
        # Mostrar preview
        print("\n📊 Preview dos dados:")
        print(df.head(5))
        
        # Estatísticas
        if 'Posição' in df.columns:
            print(f"\n📈 Distribuição:")
            print(df['Posição'].value_counts())
            
    except Exception as e:
        print(f"❌ Erro: {e}")

