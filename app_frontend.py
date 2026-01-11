import streamlit as st
import requests, time

API_URL_BASE = "https://unsneaky-unsegregational-cristy.ngrok-free.dev".strip().strip("/")
st.set_page_config(page_title="Shopee Bot Pro v11.0", page_icon="💎", layout="wide")

st.markdown("""<style>.stButton>button { width: 100%; border-radius: 10px; background-color: #ff4b2b; color: white; font-weight: bold; }
.stMetric { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #eee; }</style>""", unsafe_allow_html=True)

if 'url_tentada' not in st.session_state: st.session_state.url_tentada = ""

@st.dialog("🚩 Reportar Erro")
def modal_reporte():
    url_bug = st.text_input("Link falho:", value=st.session_state.url_tentada)
    motivos = st.multiselect("Motivo:", ["Produto errado", "Preço maior", "Link quebrado", "Acessório/Capa"])
    if st.button("Enviar"):
        requests.post(f"{API_URL_BASE}/reportar_erro", json={"url_falha": url_bug, "categorias": motivos, "descricao": ""}, headers={"ngrok-skip-browser-warning": "true"})
        st.success("Enviado!"); time.sleep(2); st.rerun()

st.title("💎 Shopee Bot Pro v11.0")

with st.sidebar:
    if st.button("🚩 Reportar Erro"): modal_reporte()
    st.markdown("---")
    modo_debug = st.checkbox("Modo Debug 🛠️", value=False)

with st.expander("🎯 Configuração de Precisão", expanded=True):
    nivel_texto = st.select_slider("Fidelidade:", options=["Nada Fiel", "Pouco Fiel", "Fiel (Padrão)", "Bem Fiel", "Muito Fiel"], value="Fiel (Padrão)")
    map_fid = {"Nada Fiel": 1, "Pouco Fiel": 2, "Fiel (Padrão)": 3, "Bem Fiel": 4, "Muito Fiel": 5}

url_input = st.text_input("Cole o link original da Shopee:")

if st.button("🚀 EXECUTAR BUSCA INTELIGENTE"):
    if url_input:
        st.session_state.url_tentada = url_input
        with st.status("🛰️ Analisando dados da rede Shopee...", expanded=True) as status:
            try:
                headers = {"ngrok-skip-browser-warning": "true"}
                payload = {"url": url_input, "nivel_fidelidade": map_fid[nivel_texto], "debug": modo_debug}
                response = requests.post(f"{API_URL_BASE}/processar", json=payload, headers=headers, timeout=180)
                res = response.json()
                
                if res.get("sucesso"):
                    status.update(label="✅ Busca Concluída!", state="complete", expanded=False)
                    st.success(f"### {res['titulo']}")
                    c1, c2 = st.columns(2); c1.metric("Preço Achado", f"R$ {res['preco']:.2f}")
                    if 'preco_original' in res: c2.metric("Referência Original", f"R$ {res['preco_original']:.2f}")
                    st.code(res['link_afiliado'])
                    st.link_button("🌍 Abrir Link", res['link_afiliado'], use_container_width=True)

                    if modo_debug and res.get("dados_debug"):
                        db = res["dados_debug"]
                        with st.expander("🔍 RELATÓRIO TÉCNICO (Ghost Engine Analítica)", expanded=True):
                            st.info(f"**Termo usado na API:** {db['termo_usado']}")
                            col1, col2 = st.columns(2)
                            col1.metric("Itens na API", db['total_achado'])
                            col2.metric("Eliminados", db['total_eliminado'])
                            st.subheader("🔝 Top 3 Crus (Sem Validação)")
                            st.table(db['top_3_crus'])
                            st.subheader("🏆 Ranking Final (Aprovados)")
                            st.dataframe(db['ranking_validados'], use_container_width=True)
                else: st.error(f"Erro: {res.get('erro')}")
            except Exception as e: st.error(f"Falha de conexão: {e}")