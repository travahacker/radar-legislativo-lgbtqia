#!/usr/bin/env python3
"""
Script para testar endpoints do Senado encontrados no Swagger UI
Execute após verificar o Swagger e identificar o endpoint correto
"""

import requests
import json
from typing import Optional

def testar_endpoint_senado(
    endpoint: str,
    params: dict = None,
    headers: dict = None
):
    """
    Testa um endpoint do Senado
    
    Args:
        endpoint: URL completa do endpoint (ex: https://legis.senado.leg.br/dadosabertos/api/v2/materia/...)
        params: Parâmetros da requisição (ex: {"ano": 2024, "sigla": "PLS"})
        headers: Headers HTTP (ex: {"Accept": "application/json"})
    
    Returns:
        dict: Resposta do servidor
    """
    if params is None:
        params = {}
    
    if headers is None:
        headers = {"Accept": "application/json"}
    
    print(f"🧪 Testando endpoint do Senado...")
    print(f"📡 URL: {endpoint}")
    print(f"📋 Parâmetros: {params}")
    print(f"📋 Headers: {headers}")
    print()
    
    try:
        response = requests.get(endpoint, params=params, headers=headers, timeout=15)
        
        print(f"✅ Status Code: {response.status_code}")
        print(f"📦 Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        print()
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ Resposta JSON recebida!")
                print(f"📊 Estrutura:")
                print(f"   Tipo: {type(data).__name__}")
                
                if isinstance(data, dict):
                    print(f"   Chaves principais: {list(data.keys())[:10]}")
                    # Tentar encontrar matérias
                    if 'dados' in data:
                        print(f"   Total de itens em 'dados': {len(data['dados']) if isinstance(data['dados'], list) else 'N/A'}")
                    elif 'Materias' in data or 'materias' in data:
                        materias = data.get('Materias') or data.get('materias')
                        if isinstance(materias, list):
                            print(f"   Total de matérias: {len(materias)}")
                            if len(materias) > 0:
                                print(f"   Exemplo primeira matéria: {list(materias[0].keys())[:5]}")
                
                print()
                print("📄 Resposta completa (primeiros 500 chars):")
                print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
                print("...")
                
                return data
            except json.JSONDecodeError:
                print(f"⚠️ Resposta não é JSON")
                print(f"📄 Resposta (primeiros 300 chars):")
                print(response.text[:300])
                return None
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(f"📄 Resposta: {response.text[:300]}")
            return None
    
    except requests.exceptions.Timeout:
        print(f"❌ Timeout - servidor não respondeu a tempo")
        return None
    except requests.exceptions.ConnectionError:
        print(f"❌ Erro de conexão - não foi possível conectar ao servidor")
        return None
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None


if __name__ == "__main__":
    print("=" * 60)
    print("🔍 TESTE DE ENDPOINT - SENADO FEDERAL")
    print("=" * 60)
    print()
    print("ℹ️  Este script testa um endpoint do Senado identificado no Swagger UI")
    print("📚 Swagger: https://legis.senado.leg.br/dadosabertos/api-docs/swagger-ui/index.html")
    print()
    print("=" * 60)
    print()
    
    # EXEMPLO: Substituir pelo endpoint encontrado no Swagger
    endpoint_exemplo = "https://legis.senado.leg.br/dadosabertos/api/v2/materia/listaMateriasTramitando"
    
    print("💡 Para testar:")
    print("   1. Abra o Swagger UI no navegador")
    print("   2. Encontre o endpoint (ex: listaMateriasTramitando)")
    print("   3. Copie a URL completa mostrada no Swagger")
    print("   4. Edite este script e substitua 'endpoint_exemplo'")
    print("   5. Execute novamente: python testar_endpoint_senado.py")
    print()
    print("-" * 60)
    print()
    
    # Descomentar e editar quando tiver o endpoint:
    """
    # COLE AQUI O ENDPOINT ENCONTRADO NO SWAGGER:
    endpoint = "https://legis.senado.leg.br/dadosabertos/[COLE_AQUI]"
    
    # Parâmetros típicos (ajustar conforme Swagger):
    params = {
        "ano": 2024,
        "sigla": "PLS"
    }
    
    # Executar teste
    resultado = testar_endpoint_senado(endpoint, params=params)
    
    if resultado:
        print("\n✅ Teste bem-sucedido!")
        print("📝 Próximo passo: atualizar api_radar.py com este endpoint")
    else:
        print("\n❌ Teste falhou - verificar endpoint e parâmetros")
    """
    
    print("⚠️  Endpoint ainda não configurado")
    print("   Edite este script com o endpoint encontrado no Swagger UI")

