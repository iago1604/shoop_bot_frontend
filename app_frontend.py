import streamlit as st
import requests
import time

# --- EXPLICAÇÃO PARA LEIGOS ---
# Configura o nome do site e o ícone que aparece na aba do navegador.
st.set_page_config(page_title="Shopee Bot Pro v5.5", page_icon="💎", layout="centered")

# --- EXPLICAÇÃO PARA LEIGOS ---
# IMPORTANTE: Toda vez que você ligar o Ngrok na VM B, você deve colar o novo link aqui.
# O link PRECISA terminar com /processar e estar entre aspas.
API_URL = "https://unsneaky-unsegregational-cristy.ngrok-free.dev/processar"

# Estilização básica para o botão ficar grande e laranja (cor da Shopee)
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; background-color: #ff4b2b; color: white; height: 3em; font-weight: bold; }
    .stButton>button:hover { background-color: #ff5722; border: 1px solid #ff4b2b; }
    </style>
    """, unsafe_allow_html=True)

st.title("💎 Shopee Bot Pro v5.5")
st.caption("Sistema de Busca e Afiliação com Bypass de Segurança")

# --- EXPLICAÇÃO PARA LEIGOS ---
# Painel de busca avançada: Permite ao usuário escolher o nível de "rigor" do robô.
with st.expander("🛠️ Busca Avançada", expanded=False):
    st.write("Configurações de precisão do robô:")
    modo_precisao = st.radio(
        "Quantidade de palavras âncora para validar o item:",
        options=[3, 5],
        index=0,
        help="3 palavras: Mais flexível. 5 palavras: Busca exata pelo modelo."
    )

# Entrada do link do produto
url_input = st.text_input("Cole o link do produto original da Shopee:", placeholder="https://shopee.com.br/produto-exemplo...")

if st.button("🚀 BUSCAR MELHOR OFERTA"):
    if not url_input:
        st.warning("⚠️ Por favor, cole um link da Shopee primeiro.")
    elif "shopee.com.br" not in url_input:
        st.error("❌ O link inserido não parece ser um link válido da Shopee.")
    else:
        # --- EXPLICAÇÃO PARA LEIGOS ---
        # Iniciamos a barra de status dinâmica para mostrar o progresso ao usuário.
        with st.status("🛰️ Conectando ao Cérebro via Túnel Seguro...", expanded=True) as status:
            try:
                # --- EXPLICAÇÃO PARA LEIGOS (O CORAÇÃO DA v5.5) ---
                # Estes 'headers' são a "Chave VIP" que pula aquela tela de aviso do Ngrok que você viu.
                # Sem isso, o robô trava na porta e o site dá erro 404 ou 403.
                headers = {
                    "ngrok-skip-browser-warning": "true",
                    "User-Agent": "ShopeeBotPro_Agent_5.5"
                }
                
                # Dados que enviamos para o Cérebro (VM B)
                payload = {
                    "url": url_input,
                    "num_ancoras": modo_precisao
                }
                
                st.write("Buscando preços e convertendo links... (Isso pode levar até 1 minuto)")
                
                # Faz a chamada para a API (Worker)
                response = requests.post(
                    API_URL, 
                    json=payload, 
                    headers=headers, 
                    timeout=180 # Esperamos o robô trabalhar com calma
                )
                
                if response.status_code == 200:
                    res = response.json()
                    
                    if res.get("sucesso"):
                        status.update(label="✅ Processamento concluído com sucesso!", state="complete", expanded=False)
                        st.balloons()
                        
                        # Exibição dos resultados encontrados
                        st.success(f"### {res['titulo']}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Melhor Preço", f"R$ {res['preco']:.2f}")
                        with col2:
                            # Caso o robô tenha retornado a economia (v4.3 em diante)
                            if 'economia' in res:
                                st.metric("Economia Gerada", f"R$ {res['economia']:.2f}", delta_color="normal")

                        st.markdown("---")
                        st.subheader("🔗 Seu Link de Afiliado:")
                        st.info("Copie e divulgue o link abaixo:")
                        st.code(res['link_afiliado'], language="text")
                        
                        # Botão extra para testar o link gerado
                        st.link_button("🌍 Abrir Link de Afiliado", res['link_afiliado'], use_container_width=True)
                    
                    else:
                        status.update(label="❌ Falha no Processamento", state="error")
                        st.error(f"Motivo: {res.get('erro')}")
                
                elif response.status_code == 404:
                    status.update(label="📡 Erro de Endereço", state="error")
                    st.error("O endereço do Cérebro não foi encontrado (Erro 404). Verifique se você esqueceu o '/processar' no final do link.")
                
                else:
                    status.update(label="📡 Falha na Rede", state="error")
                    st.error(f"Erro de conexão com o Ngrok. Código HTTP: {response.status_code}")
                    st.info("Dica: Verifique se o Ngrok está aberto na VM B e se o link no código está atualizado.")

            except Exception as e:
                status.update(label="🚨 Erro Crítico", state="error")
                st.error(f"Não foi possível alcançar o servidor: {str(e)}")

# Rodapé técnico
st.markdown("---")
st.caption("Engenharia Sênior | Shopee Bot Pro v5.5 Distributed Architecture")