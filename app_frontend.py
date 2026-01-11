import streamlit as st
import requests, time

# --- CONFIGURAÇÃO ---
API_URL_BASE = "https://SEU-LINK-NGROK-AQUI.ngrok-free.app".strip().strip("/")

st.set_page_config(page_title="Shopee Bot Pro v10.0", page_icon="💎", layout="wide")

# --- ESTILIZAÇÃO ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; background-color: #ff4b2b; color: white; font-weight: bold; }
    .stMetric { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# --- TELEMETRIA ---
def send_telemetry(level, msg, ctx={}):
    try:
        headers = {"ngrok-skip-browser-warning": "true"}
        requests.post(f"{API_URL_BASE}/log", json={"level": level, "message": msg, "context": ctx}, headers=headers, timeout=1.5)
    except: pass

# --- MODAL DE REPORTE ---
@st.dialog("🚩 Reportar Erro")
def modal_reporte():
    url_bug = st.text_input("Link que falhou:", value=st.session_state.get('url_tentada', ''))
    motivos = st.multiselect("O que houve?", ["Produto errado", "Preço maior", "Link quebrado", "Acessório/Capa"])
    detalhes = st.text_area("Detalhes:")
    if st.button("Enviar"):
        headers = {"ngrok-skip-browser-warning": "true"}
        payload = {"url_falha": url_bug, "categorias": motivos, "descricao": detalhes}
        requests.post(f"{API_URL_BASE}/reportar_erro", json=payload, headers=headers)
        st.success("Enviado!"); time.sleep(2); st.rerun()

# --- INTERFACE ---
st.title("💎 Shopee Bot Pro v10.0")

with st.sidebar:
    st.header("⚙️ Configurações")
    if st.button("🚩 Reportar Erro"): modal_reporte()
    st.markdown("---")
    # --- EXPLICAÇÃO: Botão para ativar inspeção técnica ---
    modo_debug = st.checkbox("Modo Debug 🛠️", value=False, help="Mostra o JSON bruto interceptado da API Shopee.")
    st.info("Versão: 10.0 Diagnostics")

# Slider de Fidelidade
with st.expander("🎯 Ajuste de Precisão", expanded=True):
    nivel_texto = st.select_slider("Fidelidade da Busca:", 
        options=["Nada Fiel", "Pouco Fiel", "Fiel (Padrão)", "Bem Fiel", "Muito Fiel"], 
        value="Fiel (Padrão)")
    map_fid = {"Nada Fiel": 1, "Pouco Fiel": 2, "Fiel (Padrão)": 3, "Bem Fiel": 4, "Muito Fiel": 5}
    nivel_fidelidade = map_fid[nivel_texto]

url_input = st.text_input("Cole o link original da Shopee:")

if st.button("🚀 EXECUTAR BUSCA INTELIGENTE"):
    if url_input:
        st.session_state.url_tentada = url_input
        send_telemetry("info", "busca_iniciada", {"nivel": nivel_fidelidade, "debug": modo_debug})
        
        with st.status("🛰️ Interceptando tráfego de rede...", expanded=True) as status:
            try:
                headers = {"ngrok-skip-browser-warning": "true"}
                payload = {
                    "url": url_input, 
                    "nivel_fidelidade": nivel_fidelidade,
                    "debug": modo_debug
                }
                
                response = requests.post(f"{API_URL_BASE}/processar", json=payload, headers=headers, timeout=180)
                
                if response.status_code == 200:
                    res = response.json()
                    if res.get("sucesso"):
                        status.update(label="✅ Concluído!", state="complete", expanded=False)
                        st.balloons()
                        
                        # Resultados Principais
                        st.success(f"### {res['titulo']}")
                        c1, c2 = st.columns(2)
                        c1.metric("Preço Encontrado", f"R$ {res['preco']:.2f}")
                        if 'preco_original' in res:
                            c2.metric("Preço de Referência", f"R$ {res['preco_original']:.2f}", delta="ALVO")
                        
                        st.subheader("🔗 Link de Afiliado:")
                        st.code(res['link_afiliado'], language="text")
                        st.link_button("🌍 Abrir no Navegador", res['link_afiliado'], use_container_width=True)

                        # --- EXPLICAÇÃO: Renderiza o Debug se ativo e disponível ---
                        if modo_debug and res.get("dados_debug"):
                            with st.expander("🔍 INSPEÇÃO TÉCNICA: JSON Bruto da API", expanded=False):
                                st.warning("Amostra dos 5 primeiros itens interceptados (Ghost Engine):")
                                st.json(res["dados_debug"])
                    else:
                        st.error(f"Erro no Cérebro: {res.get('erro')}")
                else:
                    st.error(f"Falha na rede (Status {response.status_code})")
            except Exception as e:
                st.error(f"Erro de conexão: {e}")