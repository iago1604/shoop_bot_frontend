import streamlit as st
import requests

# --- EXPLICAÇÃO PARA LEIGOS ---
# Verifique se este link termina exatamente com '/processar'
# E se não há espaços antes ou depois das aspas.
API_URL = "https://unsneaky-unsegregational-cristy.ngrok-free.dev/processar"

st.set_page_config(page_title="Shopee Bot Pro", page_icon="💎")
st.title("💎 Shopee Bot Pro v3.7")

url_input = st.text_input("Cole o link do produto aqui:")

if st.button("🚀 BUSCAR MELHOR PREÇO"):
    if url_input:
        with st.status("🛰️ Tentando conexão com o Cérebro...", expanded=True) as status:
            try:
                # --- EXPLICAÇÃO PARA LEIGOS (MELHORIA v3.7) ---
                # O Ngrok às vezes pergunta: "Você tem certeza que quer entrar neste site?"
                # Este comando 'headers' abaixo responde "SIM" automaticamente para o robô não travar.
                headers = {
                    "ngrok-skip-browser-warning": "69420",
                    "User-Agent": "Mozilla/5.0"
                }
                
                payload = {"url": url_input}
                
                # Fazemos a chamada para o Cérebro
                response = requests.post(
                    API_URL, 
                    json=payload, 
                    headers=headers, 
                    timeout=180 # Esperamos até 3 minutos pelo robô
                )
                
                if response.status_code == 200:
                    res = response.json()
                    if res.get("sucesso"):
                        status.update(label="✅ Conectado!", state="complete", expanded=False)
                        st.success(f"### Encontrado: {res['titulo']}")
                        st.metric("Preço", f"R$ {res['preco']:.2f}")
                        st.code(res['link_afiliado'])
                    else:
                        st.error(f"Erro no Cérebro: {res.get('erro')}")
                else:
                    # --- EXPLICAÇÃO PARA LEIGOS ---
                    # Se o código não for 200, algo bloqueou o caminho (Firewall ou Ngrok offline).
                    st.error(f"Falha na rede externa. Código de erro: {response.status_code}")
                    st.info("Verifique se o link do Ngrok no código é o mesmo que está aparecendo no terminal da VM B.")

            except Exception as e:
                st.error(f"Não foi possível alcançar o Cérebro: {e}")