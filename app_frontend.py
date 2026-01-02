import streamlit as st
import requests
import time

# --- EXPLICAÇÃO PARA LEIGOS (v6.6) ---
# 1. Cole seu link do Ngrok aqui. 
# 2. O comando '.strip("/")' no final remove qualquer barra extra que você colocar sem querer.
# 3. NUNCA coloque '/processar' aqui. Apenas o link puro.
API_URL_BASE = "https://unsneaky-unsegregational-cristy.ngrok-free.dev".strip().strip("/")

# Configuração visual da página
st.set_page_config(page_title="Shopee Bot Pro v6.6", page_icon="💎", layout="wide")

# Estilização para deixar os botões com a cara da Shopee (Laranja)
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; background-color: #ff4b2b; color: white; font-weight: bold; }
    .stButton>button:hover { background-color: #ff5722; border: 1px solid #ff4b2b; }
    </style>
    """, unsafe_allow_html=True)

# --- EXPLICAÇÃO PARA LEIGOS ---
# Usamos a memória do navegador (Session State) para o site não esquecer o link que deu erro.
if 'url_tentada' not in st.session_state:
    st.session_state.url_tentada = ""

# --- EXPLICAÇÃO PARA LEIGOS ---
# Esta é a janelinha (Modal) que abre quando você clica em "Reportar Erro".
@st.dialog("🚩 Reportar Erro ou Incoerência")
def modal_reporte():
    st.write("Diga-nos o que aconteceu para que o Engenheiro possa consertar.")
    
    # Ele já sugere o link que você tentou usar antes
    url_bug = st.text_input("Link do produto que falhou:", value=st.session_state.url_tentada)
    
    motivos = st.multiselect(
        "Qual foi o problema?",
        ["Produto diferente/errado", "Preço maior que o original", "Link de afiliado quebrado", "Apareceu acessório/capa"]
    )
    
    detalhes = st.text_area("Explique melhor o erro (opcional):")
    
    if st.button("Enviar para o Cérebro"):
        if not motivos:
            st.error("Por favor, selecione pelo menos um motivo.")
        else:
            with st.spinner("Enviando relatório..."):
                try:
                    # O "Crachá VIP" para o Ngrok deixar a mensagem passar
                    headers = {"ngrok-skip-browser-warning": "true"}
                    payload = {
                        "url_falha": url_bug if url_bug else "Não informado",
                        "categorias": motivos,
                        "descricao": detalhes if detalhes else "Sem descrição"
                    }
                    
                    # Envia para a "sala de erros" no Cérebro (VM B)
                    endpoint_erro = f"{API_URL_BASE}/reportar_erro"
                    resp = requests.post(endpoint_erro, json=payload, headers=headers, timeout=30)
                    
                    if resp.status_code == 200:
                        st.success("Relatório salvo! O desenvolvedor irá analisar o log na VM B.")
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error(f"O Cérebro recusou o reporte (Erro {resp.status_code})")
                except Exception as e:
                    st.error(f"Falha ao conectar com o Cérebro: {e}")

# --- INTERFACE PRINCIPAL ---
st.title("💎 Shopee Bot Pro v6.6")
st.caption("Sistema Distribuído | Alta Precisão | Monitoramento de Erros")

# Menu Lateral
with st.sidebar:
    st.header("⚙️ Central de Suporte")
    st.write("Use o botão abaixo se o robô falhar ou trouxer o produto errado.")
    if st.button("🚩 Reportar Erro"):
        modal_reporte()
    st.markdown("---")
    st.info("Versão do Sistema: 6.6 Stable")

# Área de Busca
with st.expander("🛠️ Ajustes de Busca Avançada", expanded=False):
    st.write("Quantas palavras o robô deve usar para validar a identidade do produto?")
    modo_precisao = st.radio("Nível de Rigor:", [3, 5], index=0, help="3: Recomendado. 5: Para modelos muito específicos.")

url_input = st.text_input("Insira o link original da Shopee:", placeholder="https://shopee.com.br/...")

if st.button("🚀 EXECUTAR BUSCA INTELIGENTE"):
    if url_input:
        # Salva na memória caso precisemos reportar erro depois
        st.session_state.url_tentada = url_input
        
        with st.status("🛰️ Comunicando com o Cérebro...", expanded=True) as status:
            try:
                headers = {"ngrok-skip-browser-warning": "true"}
                payload = {"url": url_input, "num_ancoras": modo_precisao}
                
                # Monta a URL da "sala de processamento"
                endpoint_busca = f"{API_URL_BASE}/processar"
                response = requests.post(endpoint_busca, json=payload, headers=headers, timeout=180)
                
                if response.status_code == 200:
                    res = response.json()
                    if res.get("sucesso"):
                        status.update(label="✅ Concluído!", state="complete", expanded=False)
                        st.balloons()
                        st.success(f"### {res['titulo']}")
                        
                        col1, col2 = st.columns(2)
                        col1.metric("Melhor Preço", f"R$ {res['preco']:.2f}")
                        if 'preco_original' in res:
                            col2.metric("Preço Original", f"R$ {res['preco_original']:.2f}", delta="-ECONOMIA", delta_color="normal")
                        
                        st.subheader("🔗 Link de Afiliado:")
                        st.code(res['link_afiliado'], language="text")
                        st.link_button("🌍 Abrir Link Convertido", res['link_afiliado'], use_container_width=True)
                    else:
                        status.update(label="❌ O Cérebro falhou", state="error")
                        st.error(f"Motivo: {res.get('erro')}")
                else:
                    status.update(label="📡 Erro de Rede", state="error")
                    st.error(f"Falha na comunicação (Status {response.status_code})")
                    st.info("Dica: Verifique se o link do Ngrok no código está igual ao do terminal.")
            
            except Exception as e:
                status.update(label="🚨 Erro de Conexão", state="error")
                st.error(f"Não foi possível alcançar o Worker: {e}")

# Rodapé
st.markdown("---")
st.caption("Desenvolvido por Engenharia Sênior | Logs ativos na VM B")