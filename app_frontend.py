import streamlit as st
import requests
import time

# --- EXPLICAÇÃO PARA LEIGOS ---
# Este bloco configura a aparência do site (Título e Ícone).
st.set_page_config(page_title="Shopee Bot Pro", page_icon="💎", layout="centered")

# --- EXPLICAÇÃO PARA LEIGOS ---
# Aqui colocamos o endereço "mágico" que o Ngrok nos deu. É por aqui que o site conversa com o robô.
API_URL = "https://unsneaky-unsegregational-cristy.ngrok-free.dev/processar"

st.title("💎 Shopee Bot Pro v3.0")
st.caption("Interface de Busca Inteligente")

# --- EXPLICAÇÃO PARA LEIGOS ---
# Criamos uma caixa de texto para o usuário colar o link do produto.
url_input = st.text_input("Cole o link da Shopee aqui:")

if st.button("🚀 BUSCAR MELHOR PREÇO"):
    if url_input:
        # --- EXPLICAÇÃO PARA LEIGOS ---
        # st.status cria aquela caixinha animada que mostra o que está acontecendo agora.
        with st.status("🛰️ Enviando comando para o Cérebro...", expanded=True) as status:
            try:
                # --- EXPLICAÇÃO PARA LEIGOS ---
                # Enviamos o link para a outra máquina e pedimos para ela ignorar avisos do Ngrok.
                headers = {"ngrok-skip-browser-warning": "true"}
                payload = {"url": url_input}
                
                response = requests.post(API_URL, json=payload, headers=headers, timeout=180)
                
                if response.status_code == 200:
                    res = response.json()
                    if res.get("sucesso"):
                        status.update(label="✅ Sucesso!", state="complete", expanded=False)
                        st.balloons() # Solta balões na tela para comemorar
                        
                        # --- EXPLICAÇÃO PARA LEIGOS ---
                        # Mostra os resultados bonitos na tela para o usuário.
                        st.success(f"### Encontrado: {res['titulo']}")
                        st.metric("Melhor Preço", f"R$ {res['preco']:.2f}")
                        st.subheader("🔗 Link de Afiliado Gerado:")
                        st.code(res['link_afiliado'])
                    else:
                        status.update(label="❌ Erro no Processamento", state="error")
                        st.error(res.get("erro"))
                else:
                    st.error("Falha na rede externa.")
            except Exception as e:
                st.error(f"Erro de conexão: {e}")