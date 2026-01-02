import streamlit as st
import requests
import time

# --- EXPLICAÇÃO PARA LEIGOS (v7.0) ---
# 1. Cole seu link do Ngrok aqui. 
# 2. O robô limpa o link automaticamente para evitar erros de conexão.
API_URL_BASE = "https://SEU-LINK-NGROK-AQUI.ngrok-free.app".strip().strip("/")

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="Shopee Bot Pro v7.0", page_icon="💎", layout="wide")

# Estilização Shopee (Laranja)
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; background-color: #ff4b2b; color: white; font-weight: bold; height: 3em;}
    .stButton>button:hover { background-color: #ff5722; border: 1px solid #ff4b2b; }
    [data-testid="stMetricValue"] { font-size: 1.8rem; color: #ff4b2b; }
    </style>
    """, unsafe_allow_html=True)

# --- TELEMETRIA SILENCIOSA (A CAIXA PRETA v7.0) ---
def send_telemetry(level, message, context={}):
    """Envia dados de uso para o log central na VM B sem travar o site."""
    try:
        headers = {"ngrok-skip-browser-warning": "true"}
        payload = {"level": level, "message": message, "context": context}
        # Timeout ultra-rápido de 1s para o usuário não sentir lentidão
        requests.post(f"{API_URL_BASE}/log", json=payload, headers=headers, timeout=1.5)
    except:
        pass # Se a telemetria falhar, o site continua funcionando normal

# Inicialização de memória do navegador
if 'url_tentada' not in st.session_state:
    st.session_state.url_tentada = ""

# --- MODAL DE REPORTE ESTRUTURADO ---
@st.dialog("🚩 Central de Reporte")
def modal_reporte():
    st.write("Diga-nos o que houve. O Engenheiro analisará os logs na VM B.")
    url_bug = st.text_input("Link que falhou:", value=st.session_state.url_tentada)
    motivos = st.multiselect("Categorias:", ["Produto errado", "Preço maior", "Link quebrado", "Acessório/Capa"])
    detalhes = st.text_area("Detalhes adicionais:")
    
    if st.button("Enviar para Auditoria"):
        if motivos:
            with st.spinner("Enviando..."):
                try:
                    headers = {"ngrok-skip-browser-warning": "true"}
                    payload = {
                        "url_falha": url_bug,
                        "categorias": motivos,
                        "descricao": detalhes
                    }
                    requests.post(f"{API_URL_BASE}/reportar_erro", json=payload, headers=headers, timeout=10)
                    # Telemetria: Avisa que o usuário reportou algo manualmente
                    send_telemetry("warning", "usuario_reportou_erro_manual", {"categorias": motivos})
                    st.success("Relatório salvo no Cérebro!")
                    time.sleep(2)
                    st.rerun()
                except:
                    st.error("Erro ao conectar com a VM B.")
        else:
            st.error("Selecione pelo menos um motivo.")

# --- INTERFACE ---
st.title("💎 Shopee Bot Pro v7.0")
st.caption("Arquitetura Distribuída com Telemetria e Logs Estruturados")

# Sidebar de Suporte
with st.sidebar:
    st.header("⚙️ Painel de Controle")
    if st.button("🚩 Reportar Incoerência"):
        modal_reporte()
    st.markdown("---")
    st.info("Status: Black Box v7.0 Ativo")

# Busca Avançada
with st.expander("🛠️ Ajustes de Inteligência", expanded=False):
    n_ancoras = st.radio("Nível de Rigor (Âncoras):", [3, 5], index=0, help="3: Normal. 5: Identidade Exata.")

url_input = st.text_input("Link do Produto Shopee:", placeholder="https://shopee.com.br/...")

# --- LÓGICA DE EXECUÇÃO ---
if st.button("🚀 EXECUTAR BUSCA INTELIGENTE"):
    if url_input:
        st.session_state.url_tentada = url_input
        # Telemetria: Início da Jornada
        send_telemetry("info", "busca_iniciada", {"url": url_input, "ancoras": n_ancoras})
        
        with st.status("🛰️ Processando via Cérebro Remoto...", expanded=True) as status:
            try:
                headers = {"ngrok-skip-browser-warning": "true"}
                payload = {"url": url_input, "num_ancoras": n_ancoras}
                
                inicio_timer = time.time()
                response = requests.post(f"{API_URL_BASE}/processar", json=payload, headers=headers, timeout=180)
                tempo_total = round(time.time() - inicio_timer, 2)
                
                if response.status_code == 200:
                    res = response.json()
                    if res.get("sucesso"):
                        status.update(label=f"✅ Concluído em {tempo_total}s", state="complete", expanded=False)
                        st.balloons()
                        
                        # Telemetria: Sucesso
                        send_telemetry("info", "busca_sucesso", {"titulo": res['titulo'], "preco": res['preco'], "tempo": tempo_total})
                        
                        st.success(f"### {res['titulo']}")
                        c1, c2 = st.columns(2)
                        c1.metric("Melhor Preço", f"R$ {res['preco']:.2f}")
                        if 'preco_original' in res:
                            c2.metric("Preço Original", f"R$ {res['preco_original']:.2f}", delta="BUSCA ATIVA")
                        
                        st.subheader("🔗 Seu Link de Afiliado:")
                        st.code(res['link_afiliado'], language="text")
                        st.link_button("🌍 Abrir no Navegador", res['link_afiliado'], use_container_width=True)
                    else:
                        status.update(label="❌ O Cérebro encontrou um problema", state="error")
                        st.error(f"Motivo: {res.get('erro')}")
                        # Telemetria: Falha de Regra de Negócio
                        send_telemetry("error", "worker_error", {"msg": res.get("erro"), "url": url_input})
                else:
                    status.update(label="📡 Erro de Comunicação", state="error")
                    st.error(f"Servidor inacessível (Status {response.status_code})")
                    send_telemetry("critical", "rede_externa_falhou", {"http_status": response.status_code})
            
            except Exception as e:
                status.update(label="🚨 Erro de Rede Crítico", state="error")
                st.error(f"Não foi possível conectar à VM B: {e}")
                send_telemetry("critical", "frontend_exception", {"erro": str(e)})

# Rodapé
st.markdown("---")
st.caption("Engenharia Sênior | Monitoramento em Tempo Real habilitado")