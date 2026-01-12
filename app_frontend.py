import streamlit as st
import requests, time

API_URL_BASE = "https://unsneaky-unsegregational-cristy.ngrok-free.dev".strip().strip("/")
st.set_page_config(page_title="Shopee Bot Pro v11.6", page_icon="💎", layout="wide")

if 'url_tentada' not in st.session_state: st.session_state.url_tentada = ""

st.title("💎 Shopee Bot Pro v11.6")

with st.sidebar:
    st.header("⚙️ Configurações")
    modo_debug = st.checkbox("Modo Debug 🛠️", value=True)
    st.info("Status: v11.6 Stable")

nivel_texto = st.select_slider("Fidelidade:", options=["Nada Fiel", "Pouco Fiel", "Fiel (Padrão)", "Bem Fiel", "Muito Fiel"], value="Fiel (Padrão)")
map_fid = {"Nada Fiel": 1, "Pouco Fiel": 2, "Fiel (Padrão)": 3, "Bem Fiel": 4, "Muito Fiel": 5}

url_input = st.text_input("Link original da Shopee:")

if st.button("🚀 BUSCAR MELHOR PREÇO"):
    if url_input:
        st.session_state.url_tentada = url_input
        with st.status("🛰️ Analisando dados da rede Shopee...", expanded=True) as status:
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

                    # --- EXIBIÇÃO SEGURA DO DEBUG v11.6 ---
                    if modo_debug and res.get("dados_debug"):
                        db = res["dados_debug"]
                        with st.expander("🔍 RELATÓRIO TÉCNICO", expanded=True):
                            st.info(f"**Termo usado:** {db.get('termo_usado', 'N/A')}")
                            col1, col2 = st.columns(2)
                            col1.metric("Itens na API", db.get('total_achado', 0))
                            col2.metric("Eliminados", db.get('total_eliminado', 0))
                            
                            st.subheader("🏆 Ranking Final (Itens Aprovados)")
                            st.dataframe(db.get('ranking_validados', []), use_container_width=True)
                else:
                    st.error(f"Erro: {res.get('erro')}")
            except Exception as e:
                st.error(f"Falha de conexão: {e}")