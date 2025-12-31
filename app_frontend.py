import streamlit as st
import requests

# --- EXPLICAÇÃO PARA LEIGOS ---
# Endereço do seu Cérebro (Ngrok). Lembre-se de atualizar se o Ngrok reiniciar!
API_URL = "https://SEU-LINK-AQUI.ngrok-free.app/processar"

st.set_page_config(page_title="Shopee Bot Pro v4.0", page_icon="💎")
st.title("💎 Shopee Bot Pro v4.0")

# --- EXPLICAÇÃO PARA LEIGOS ---
# Criamos um botão que "abre" opções escondidas de busca.
with st.expander("🛠️ Busca Avançada", expanded=False):
    st.info("Escolha o nível de precisão para validar o produto:")
    modo_precisao = st.radio(
        "Quantidade de palavras para conferência (Âncora):",
        options=[3, 5],
        index=0,
        help="3 palavras: Mais chance de achar. 5 palavras: Só aceita se for exatamente igual."
    )

url_input = st.text_input("Link do produto:")

if st.button("🚀 EXECUTAR BUSCA"):
    if url_input:
        with st.status("🛰️ Processando com Busca Avançada...", expanded=True) as status:
            try:
                headers = {"ngrok-skip-browser-warning": "true"}
                # --- EXPLICAÇÃO PARA LEIGOS ---
                # Agora enviamos para o robô não só o link, mas também o nível de precisão escolhido.
                payload = {
                    "url": url_input,
                    "num_ancoras": modo_precisao
                }
                
                response = requests.post(API_URL, json=payload, headers=headers, timeout=180)
                
                if response.status_code == 200:
                    res = response.json()
                    if res.get("sucesso"):
                        status.update(label="✅ Produto Identificado!", state="complete", expanded=False)
                        st.success(f"### {res['titulo']}")
                        st.metric("Melhor Preço", f"R$ {res['preco']:.2f}")
                        st.code(res['link_afiliado'])
                    else:
                        st.error(f"Erro: {res.get('erro')}")
                else:
                    st.error(f"Falha na rede (Status {response.status_code})")
            except Exception as e:
                st.error(f"Erro de conexão: {e}")