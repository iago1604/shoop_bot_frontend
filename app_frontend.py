import streamlit as st
import requests, time

# --- EXPLICAÇÃO: Sanitização automática do link ---
API_URL_BASE = "https://unsneaky-unsegregational-cristy.ngrok-free.dev".strip().strip("/")

st.set_page_config(page_title="Shopee Bot Pro v9.0", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; background-color: #ff4b2b; color: white; font-weight: bold; }
    .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

def send_telemetry(level, msg, ctx={}):
    try:
        headers = {"ngrok-skip-browser-warning": "true"}
        requests.post(f"{API_URL_BASE}/log", json={"level": level, "message": msg, "context": ctx}, headers=headers, timeout=1.5)
    except: pass

if 'url_tentada' not in st.session_state: st.session_state.url_tentada = ""

@st.dialog("🚩 Reportar Erro")
def modal_reporte():
    url_bug = st.text_input("Link falho:", value=st.session_state.url_tentada)
    motivos = st.multiselect("O que houve?", ["Produto diferente", "Preço maior", "Link quebrado", "Acessório/Capa"])
    detalhes = st.text_area("Detalhes:")
    if st.button("Enviar"):
        headers = {"ngrok-skip-browser-warning": "true"}
        requests.post(f"{API_URL_BASE}/reportar_erro", json={"url_falha": url_bug, "categorias": motivos, "descricao": detalhes}, headers=headers)
        st.success("Relatório enviado!"); time.sleep(2); st.rerun()

st.title("💎 Shopee Bot Pro v9.0")
st.caption("Fidelity Matrix Edition | Ghost API Engine")

with st.sidebar:
    st.header("⚙️ Suporte")
    if st.button("🚩 Reportar Erro"): modal_reporte()

# --- EXPLICAÇÃO: O Slider de Fidelidade ---
with st.expander("🎯 Configuração de Precisão (Matriz v9.0)", expanded=True):
    nivel_texto = st.select_slider(
        "Nível de Fidelidade:",
        options=["Nada Fiel", "Pouco Fiel", "Fiel (Padrão)", "Bem Fiel", "Muito Fiel"],
        value="Fiel (Padrão)"
    )
    map_fid = {"Nada Fiel": 1, "Pouco Fiel": 2, "Fiel (Padrão)": 3, "Bem Fiel": 4, "Muito Fiel": 5}
    nivel_fidelidade = map_fid[nivel_texto]

url_input = st.text_input("Cole o link original da Shopee:")

if st.button("🚀 EXECUTAR BUSCA INTELIGENTE"):
    if url_input:
        st.session_state.url_tentada = url_input
        send_telemetry("info", "busca_iniciada", {"nivel": nivel_fidelidade})
        with st.status("🛰️ Interceptando dados da Shopee...", expanded=True) as status:
            try:
                headers = {"ngrok-skip-browser-warning": "true"}
                payload = {"url": url_input, "nivel_fidelidade": nivel_fidelidade}
                response = requests.post(f"{API_URL_BASE}/processar", json=payload, headers=headers, timeout=180)
                res = response.json()
                
                if res.get("sucesso"):
                    status.update(label="✅ Sucesso!", state="complete")
                    st.balloons()
                    st.success(f"### {res['titulo']}")
                    c1, c2 = st.columns(2)
                    c1.metric("Preço Achado", f"R$ {res['preco']:.2f}")
                    if 'preco_original' in res:
                        c2.metric("Preço Original", f"R$ {res['preco_original']:.2f}", delta="BUSCA ATIVA")
                    st.subheader("🔗 Link de Afiliado:")
                    st.code(res['link_afiliado'])
                    st.link_button("🌍 Abrir Link", res['link_afiliado'], use_container_width=True)
                else: st.error(f"Erro: {res.get('erro')}")
            except Exception as e: st.error(f"Falha de conexão: {e}")