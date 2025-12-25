import streamlit as st
import requests

# --- EXPLICAÇÃO PARA LEIGOS ---
# Toda vez que você ligar o Ngrok, você deve vir aqui e colar o link novo.
# Exemplo: API_URL = "https://1234-abcd.ngrok-free.app/processar"
API_URL = "https://unsneaky-unsegregational-cristy.ngrok-free.dev/processar"

st.set_page_config(page_title="Shopee Bot Pro", page_icon="💎")

st.title("💎 Shopee Bot Pro v3.9")
st.caption("Modo de Conexão Dinâmica (Ngrok)")

url_input = st.text_input("Link do produto da Shopee:")

if st.button("🚀 BUSCAR MELHOR PREÇO"):
    if url_input:
        with st.status("🛰️ Conectando ao Cérebro...", expanded=True) as status:
            try:
                # --- EXPLICAÇÃO PARA LEIGOS ---
                # Este cabeçalho "ngrok-skip-browser-warning" é OBRIGATÓRIO.
                # Ele faz o Ngrok deixar o robô passar sem mostrar aquela tela de aviso.
                headers = {
                    "ngrok-skip-browser-warning": "true"
                }
                
                payload = {"url": url_input}
                
                # Chamada para a API (Cérebro)
                response = requests.post(API_URL, json=payload, headers=headers, timeout=180)
                
                if response.status_code == 200:
                    res = response.json()
                    if res.get("sucesso"):
                        status.update(label="✅ Conectado!", state="complete", expanded=False)
                        st.success(f"### {res['titulo']}")
                        st.metric("Preço", f"R$ {res['preco']:.2f}")
                        st.code(res['link_afiliado'])
                    else:
                        st.error(f"Erro: {res.get('erro')}")
                else:
                    st.error(f"Falha na rede (Erro {response.status_code}). Verifique se o link no código é o mesmo do Ngrok.")
            
            except Exception as e:
                st.error(f"Não foi possível conectar: {e}") 