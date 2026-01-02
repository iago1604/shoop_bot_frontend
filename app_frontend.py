import streamlit as st
import requests
import time

# --- EXPLICAÇÃO PARA LEIGOS ---
# Atualize este link sempre que o Ngrok mudar (a menos que use link fixo).
API_URL_BASE = "https://unsneaky-unsegregational-cristy.ngrok-free.dev"

st.set_page_config(page_title="Shopee Bot Pro v6.5", page_icon="💎", layout="wide")

# --- EXPLICAÇÃO PARA LEIGOS ---
# Esta função cria a janelinha de reportar erro (Modal).
@st.dialog("🚩 Reportar Erro ou Incoerência")
def modal_reporte():
    st.write("Diga-nos o que aconteceu para melhorarmos o robô.")
    url_bug = st.text_input("URL do link que falhou:", value=st.session_state.get('url_tentada', ''))
    motivos = st.multiselect("O que houve?", ["Produto errado", "Preço maior", "Link quebrado", "Acessório no lugar do item"])
    detalhes = st.text_area("Mais detalhes:")
    
    if st.button("Enviar Relatório"):
        if motivos:
            try:
                headers = {"ngrok-skip-browser-warning": "true"}
                payload = {"url_falha": url_bug, "categorias": motivos, "descricao": detalhes}
                requests.post(f"{API_URL_BASE}/reportar_erro", json=payload, headers=headers)
                st.success("Enviado! Obrigado.")
                time.sleep(1)
                st.rerun()
            except: st.error("Erro ao conectar ao servidor.")
        else: st.error("Selecione um motivo.")

# Interface
st.title("💎 Shopee Bot Pro v6.5")

with st.sidebar:
    st.header("⚙️ Suporte")
    if st.button("🚩 Reportar um Erro"):
        modal_reporte()

# Campo de Busca
with st.expander("🛠️ Ajustes de Busca", expanded=False):
    ancoras = st.radio("Precisão (Palavras):", [3, 5], index=0)

url_input = st.text_input("Link do Produto Shopee:")
if st.button("🚀 EXECUTAR"):
    if url_input:
        st.session_state.url_tentada = url_input
        with st.status("🛰️ Processando...", expanded=True) as status:
            try:
                headers = {"ngrok-skip-browser-warning": "true"}
                payload = {"url": url_input, "num_ancoras": ancoras}
                response = requests.post(f"{API_URL_BASE}/processar", json=payload, headers=headers, timeout=180)
                res = response.json()
                
                if res.get("sucesso"):
                    status.update(label="✅ Concluído!", state="complete", expanded=False)
                    st.success(f"### {res['titulo']}")
                    st.metric("Preço", f"R$ {res['preco']:.2f}")
                    st.code(res['link_afiliado'])
                else:
                    st.error(f"Erro: {res.get('erro')}")
            except Exception as e:
                st.error(f"Falha de rede: {e}")