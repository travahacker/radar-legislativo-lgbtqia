"""
Radar Legislativo LGBTQIA+
Sistema de busca e análise automática de Projetos de Lei relacionados a direitos LGBTQIA+
"""

import gradio as gr
import pandas as pd
import re
from datetime import datetime
from ensemble_híbrido import classificar_ensemble, carregar_modelos
from api_radar import buscar_camara_deputados, buscar_senado_federal, filtrar_pls_relevantes

# Carregar modelos uma vez no início
print("🏳️‍🌈 Carregando modelos...")
radar_model, azmina_model = carregar_modelos()
if radar_model is None:
    print("⚠️ Aviso: Radar Social não carregado. Algumas funcionalidades podem não funcionar.")

# Interface Gradio - Modo Radar
with gr.Blocks(
    theme=gr.themes.Soft(primary_hue="purple"),
    title="🏳️‍🌈 Radar Legislativo LGBTQIA+"
) as app:
    
    gr.Markdown("""
    # 🏳️‍🌈 Radar Legislativo LGBTQIA+
    
    Sistema de busca e análise automática de Projetos de Lei relacionados a direitos LGBTQIA+ 
    no **Congresso Nacional** (Câmara dos Deputados e Senado Federal).
    
    Utiliza **Ensemble Híbrido** (Radar Social + AzMina/QuiterIA + Keywords + Padrões) para identificar
    se PLs são **favoráveis** ou **desfavoráveis** aos direitos da comunidade LGBTQIA+.
    
    ## ⚠️ Aviso Importante
    - Requer **revisão humana** para decisões finais
    - Use como **ferramenta de apoio**, não como decisão automática
    """)
    
    
    # RADAR AUTOMÁTICO - Única aba
    with gr.Tab("🔍 Radar Automático - Congresso Nacional"):
        gr.Markdown("""
        ### 🔍 Radar Automático de PLs LGBTQIA+ - Congresso Nacional
        
        Busca e analisa automaticamente PLs relacionadas a direitos LGBTQIA+ nas APIs oficiais:
        - **Câmara dos Deputados** ✅
        - **Senado Federal** ✅
        
        ⚠️ **Atenção:** A busca pode levar alguns segundos, especialmente em períodos longos.
        """)
        
        with gr.Row():
            ano_inicio = gr.Slider(
                label="Ano Inicial",
                minimum=2010,
                maximum=2025,
                value=2020,
                step=1,
                info="Ano mais antigo para buscar"
            )
            
            ano_fim = gr.Slider(
                label="Ano Final",
                minimum=2010,
                maximum=2025,
                value=2025,
                step=1,
                info="Ano mais recente para buscar"
            )
            
            limite_resultados = gr.Slider(
                label="Limite de resultados",
                minimum=5,
                maximum=100,
                value=50,
                step=5,
                info="Número máximo de PLs encontradas"
            )
        
        with gr.Row():
            btn_buscar = gr.Button("🔍 Buscar e Analisar PLs", variant="primary", scale=2)
            checkbox_camara = gr.Checkbox(label="Câmara dos Deputados", value=True)
            checkbox_senado = gr.Checkbox(label="Senado Federal", value=True)
        
        output_busca = gr.Markdown(label="📊 PLs Encontradas e Analisadas")
        
        def buscar_e_analisar(ano_inicio, ano_fim, limite, buscar_camara, buscar_senado):
            """Busca PLs e analisa automaticamente"""
            import sys
            from io import StringIO
            
            # Validar anos
            if ano_inicio > ano_fim:
                return "❌ **Erro:** Ano inicial deve ser menor ou igual ao ano final."
            
            if ano_fim > datetime.now().year:
                return f"❌ **Erro:** Ano final não pode ser maior que {datetime.now().year}."
            
            if not buscar_camara and not buscar_senado:
                return "❌ **Erro:** Selecione pelo menos uma fonte (Câmara ou Senado)."
            
            # Capturar prints para exibir na interface
            old_stdout = sys.stdout
            sys.stdout = output_buffer = StringIO()
            
            try:
                pls_encontradas = []
                anos_para_buscar = list(range(int(ano_inicio), int(ano_fim) + 1))
                
                print(f"🔍 Buscando PLs LGBTQIA+ no Congresso Nacional...")
                print(f"📅 Período: {ano_inicio} a {ano_fim} ({len(anos_para_buscar)} anos)")
                
                # 1. Câmara dos Deputados
                if buscar_camara:
                    print(f"\n📥 Buscando na Câmara dos Deputados...")
                    for ano in reversed(anos_para_buscar):
                        if len(pls_encontradas) >= int(limite):
                            break
                        
                        limite_restante = int(limite) - len(pls_encontradas)
                        if limite_restante <= 0:
                            break
                        
                        pls_ano = buscar_camara_deputados(
                            sigla_tipo="PL",
                            limite=limite_restante,
                            ano_inicio_manual=ano,
                            ano_fim_manual=ano
                        )
                        pls_encontradas.extend(pls_ano)
                        if pls_ano:
                            print(f"   ✅ {len(pls_ano)} PLs encontradas na Câmara em {ano}")
                
                # 2. Senado Federal
                if buscar_senado and len(pls_encontradas) < int(limite):
                    print(f"\n📥 Buscando no Senado Federal...")
                    for ano in reversed(anos_para_buscar):
                        if len(pls_encontradas) >= int(limite):
                            break
                        
                        limite_restante = int(limite) - len(pls_encontradas)
                        if limite_restante <= 0:
                            break
                        
                        pls_ano = buscar_senado_federal(
                            limite=limite_restante,
                            ano_inicio_manual=ano,
                            ano_fim_manual=ano
                        )
                        pls_encontradas.extend(pls_ano)
                        if pls_ano:
                            print(f"   ✅ {len(pls_ano)} PLs encontradas no Senado em {ano}")
                
                # Restaurar stdout
                sys.stdout = old_stdout
                logs = output_buffer.getvalue()
                
                if not pls_encontradas:
                    fontes = []
                    if buscar_camara:
                        fontes.append("Câmara dos Deputados")
                    if buscar_senado:
                        fontes.append("Senado Federal")
                    fontes_str = " e ".join(fontes)
                    
                    return f"""⚠️ Nenhuma PL encontrada em {fontes_str} para o período {int(ano_inicio)}-{int(ano_fim)}.

**Logs da busca:**
```
{logs}
```

**Possíveis razões:**
- Pode não haver PLs LGBTQIA+ no período selecionado
- Tente aumentar o período (ex: 2010-2025)
- PLs podem estar em outros anos

**Dica:** Buscar em períodos maiores (ex: 2010-2025) aumenta as chances de encontrar resultados."""
                
                # Remover duplicatas
                pls_unicas = []
                ids_vistos = set()
                for pl in pls_encontradas:
                    pl_id = f"{pl['Nº']}_{pl['Ano']}"
                    if pl_id not in ids_vistos:
                        ids_vistos.add(pl_id)
                        pls_unicas.append(pl)
                
                pls_relevantes = filtrar_pls_relevantes(pls_unicas)
                
                if not pls_relevantes:
                    return f"""⚠️ Encontradas {len(pls_encontradas)} PLs, mas nenhuma passou pelo filtro de relevância.

**Logs da busca:**
```
{logs}
```

**Possíveis razões:**
- Filtro muito restritivo
- PLs podem não conter termos LGBTQIA+ na ementa

**Dica:** Os resultados já vêm filtrados da API. Se ainda assim não aparecer, tente aumentar o período de busca."""
                
                # Analisar cada PL encontrado
                resultados = []
                print(f"\n🔍 Analisando {len(pls_relevantes)} PLs encontradas...")
                
                for i, pl in enumerate(pls_relevantes, 1):
                    ementa = pl.get('Ementa', '')
                    if not ementa:
                        continue
                    
                    resultado = classificar_ensemble(ementa, radar_model, azmina_model)
                    
                    resultados.append({
                        'Nº': pl.get('Nº', 'N/A'),
                        'Ano': pl.get('Ano', 'N/A'),
                        'Casa': pl.get('Casa', 'N/A'),
                        'Fonte': pl.get('Fonte', 'N/A'),
                        'Classificação': resultado['classificacao'],
                        'Score': f"{resultado['score_final']:.1%}",
                        'Ementa': ementa[:100] + '...' if len(ementa) > 100 else ementa,
                        'Link': pl.get('Link', 'N/A')
                    })
                    
                    if i % 5 == 0:
                        print(f"   📊 {i}/{len(pls_relevantes)} PLs analisadas...")
                
                df_resultados = pd.DataFrame(resultados)
                
                # Estatísticas
                total = len(resultados)
                favoraveis = sum(1 for r in resultados if r['Classificação'] == 'FAVORÁVEL')
                desfavoraveis = sum(1 for r in resultados if r['Classificação'] == 'DESFAVORÁVEL')
                revisao = sum(1 for r in resultados if r['Classificação'] == 'REVISÃO')
                
                fontes_usadas = []
                if buscar_camara:
                    fontes_usadas.append("Câmara")
                if buscar_senado:
                    fontes_usadas.append("Senado")
                
                relatorio = f"""## 🔍 Radar de PLs LGBTQIA+ - Resultados

**Total de PLs encontradas e analisadas:** {total}  
**Fontes consultadas:** {", ".join(fontes_usadas) if fontes_usadas else "Nenhuma"}

### 📈 Distribuição:
- **✅ FAVORÁVEL:** {favoraveis} ({favoraveis/total*100:.1f}%)
- **❌ DESFAVORÁVEL:** {desfavoraveis} ({desfavoraveis/total*100:.1f}%)
- **⚠️ REVISÃO NECESSÁRIA:** {revisao} ({revisao/total*100:.1f}%)

### 📋 PLs Encontradas:

{df_resultados[['Nº', 'Ano', 'Casa', 'Fonte', 'Classificação', 'Score', 'Ementa']].to_markdown(index=False)}

### 🔗 Links para PLs Desfavoráveis:
"""
                
                # Adicionar links dos desfavoráveis
                desfav_links = [r for r in resultados if r['Classificação'] == 'DESFAVORÁVEL']
                if desfav_links:
                    for r in desfav_links[:10]:  # Primeiros 10
                        relatorio += f"\n- [{r['Nº']}]({r['Link']}) - {r['Score']}"
                
                relatorio += f"\n\n---\n\n**Logs da busca:**\n```\n{logs}\n```\n\n**Última busca:** {datetime.now().strftime('%d/%m/%Y %H:%M')}"
                
                return relatorio
            
            except Exception as e:
                sys.stdout = old_stdout if 'old_stdout' in locals() else sys.stdout
                logs = output_buffer.getvalue() if 'output_buffer' in locals() else ""
                return f"""❌ Erro ao buscar e analisar: {str(e)}

**Logs antes do erro:**
```
{logs}
```

**Tipo de erro:** {type(e).__name__}

**Dica:** Verifique sua conexão com a internet e tente novamente."""
        
        btn_buscar.click(
            fn=buscar_e_analisar,
            inputs=[ano_inicio, ano_fim, limite_resultados, checkbox_camara, checkbox_senado],
            outputs=output_busca
        )
        
        gr.Markdown("""
        ---
        
        ### 💡 Como funciona:
        
        1. **Selecione o período:** Escolha o ano inicial e final (2010-2025)
        2. **Escolha as fontes:** Marque Câmara e/ou Senado
        3. **Defina o limite:** Quantas PLs você quer encontrar (máximo recomendado: 50-100)
        4. **Clique em "Buscar e Analisar PLs"** para iniciar
        5. O sistema busca PLs nas APIs usando termos relacionados a LGBTQIA+
        6. Filtra PLs que contêm termos relevantes na ementa
        7. Analisa automaticamente cada PL encontrado com o Ensemble Híbrido
        8. Exibe resultados com classificação (Favorável/Desfavorável/Revisão)
        
        ### 📋 Recomendações:
        - **Período pequeno (1-2 anos):** Rápido, poucos resultados
        - **Período médio (3-5 anos):** Balanceado, mais resultados
        - **Período grande (2010-2025):** Pode levar alguns minutos, muitos resultados
        
        ### ⚠️ Limitações:
        - A busca pode levar alguns segundos (até minutos para períodos longos)
        - A API da Câmara permite até 100 itens por página (buscamos múltiplas páginas)
        - A API do Senado ainda está em desenvolvimento básico
        - Depende da disponibilidade das APIs públicas
        """)
    
    gr.Markdown("""
    ---
    
    ### 📚 Sobre
    - **Sistema:** Ensemble Híbrido (Radar Social + AzMina/QuiterIA + Keywords + Padrões)
    - **Modelos:** 
      - Radar Social LGBTQIA+ V2.1 por [Veronyka](https://huggingface.co/Veronyka/radar-social-lgbtqia-v2.1)
      - IA Feminista AzMina/QuiterIA por [AzMina](https://huggingface.co/azmina/ia-feminista-bert-posicao)
    - **Dataset base:** 39 PLs anotadas manualmente
    
    ### ⚖️ Limitações
    - Requer validação humana para contexto legislativo completo
    - Thresholds: ≥50% = DESFAVORÁVEL | 30-50% = REVISÃO | <30% = FAVORÁVEL
    """)

if __name__ == "__main__":
    # Para Hugging Face Spaces, usar launch sem parâmetros
    # Para local, pode usar os parâmetros abaixo
    try:
        import os
        if os.getenv("SPACE_ID") or os.getenv("SYSTEM"):
            # Rodando no Hugging Face Space
            app.launch()
        else:
            # Rodando localmente
            app.launch(
                share=False,
                server_name="0.0.0.0",
                server_port=7860,
                inbrowser=False,
                show_error=True
            )
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        # Fallback: tentar sem parâmetros
        app.launch()
