import streamlit as st
import requests, time

API_URL_BASE = "https://unsneaky-unsegregational-cristy.ngrok-free.dev".strip().strip("/")
st.set_page_config(page_title="Shopee Bot Pro v13.0 Stealth", page_icon="💎", layout="wide")

st.markdown("""<style>.stButton>button { width: 100%; border-radius: 10px; background-color: #ff4b2b; color: white; font-weight: bold; }
.stMetric { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #eee; }</style>""", unsafe_allow_html=True)

if 'url_tentada' not in st.session_state: st.session_state.url_tentada = ""

st.title("💎 Shopee Bot Pro v13.0")
st.caption("Anti-Detection Stealth Engine Ativo")

with st.sidebar:
    st.header("⚙️ Suporte")
    if st.button("🚩 Reportar Erro"): st.toast("Use o modal de erro (v6.6)")
    modo_debug = st.checkbox("Modo Debug 🛠️", value=True)

nivel_texto = st.select_slider("Fidelidade da Busca:", options=["Nada Fiel", "Pouco Fiel", "Fiel (Padrão)", "Bem Fiel", "Muito Fiel"], value="Fiel (Padrão)")
map_fid = {"Nada Fiel": 1, "Pouco Fiel": 2, "Fiel (Padrão)": 3, "Bem Fiel": 4, "Muito Fiel": 5}

url_input = st.text_input("Link do produto:")

if st.button("🚀 EXECUTAR"):
    if url_input:
        st.session_state.url_tentada = url_input
        with st.status("🛰️ Interceptando dados via Stealth Mode...", expanded=True) as status:
            try:
                headers = {"ngrok-skip-browser-warning": "true"}
                payload = {"url": url_input, "nivel_fidelidade": map_fid[nivel_texto], "debug": modo_debug}
                response = requests.post(f"{API_URL_BASE}/processar", json=payload, headers=headers, timeout=180)
                res = response.json()
                
                if res.get("sucesso"):
                    status.update(label="✅ Sucesso!", state="complete", expanded=False)
                    st.success(f"### {res['titulo']}")
                    c1, c2 = st.columns(2)
                    c1.metric("Preço Achado", f"R$ {res['preco']:.2f}")
                    if 'preco_original' in res: c2.metric("Original", f"R$ {res['preco_original']:.2f}")
                    
                    st.code(res['link_afiliado'])
                    st.link_button("🌍 Abrir Link", res['link_afiliado'], use_container_width=True)

                    if modo_debug and res.get("dados_debug"):
                        db = res["dados_debug"]
                        with st.expander("🔍 RELATÓRIO TÉCNICO (Anti-Stall)", expanded=True):
                            st.info(f"**Termo usado:** {db.get('termo', 'N/A')}")
                            col1, col2 = st.columns(2)
                            st.metric("Itens na API", db.get('capturados', 0))
                            st.metric("Aprovados", db.get('aprovados', 0))
                            if db.get('ranking'):
                                st.subheader("🏆 Melhores Candidatos")
                                st.dataframe(db['ranking'])
                            if not db.get('aprovados'):
                                st.error("🚨 Nenhum item passou! Veja os eliminados:")
                                st.table(db.get('near_misses', []))
                else: st.error(f"Erro: {res.get('erro')}")
            except Exception as e: st.error(f"Falha de conexão: {e}")