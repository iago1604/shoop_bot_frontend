# 🖥️ Shopee Bot Pro - Documentação da Interface (Frontend)

Este módulo é o portal de comando do usuário. Ele gerencia a entrada de links, exibe a economia gerada e monitora a saúde do sistema via telemetria.

## 🛠️ Stack Tecnológica
- **Linguagem:** Python 3.12
- **Framework UI:** Streamlit (Hospedado no Streamlit Cloud)
- **Comunicação:** Requests (com Bypass Ngrok)

## 📋 Lista de Funções por Versão

### [v14.0] - Sentinel UI
- **Cascade Status Tracker**: Barra de progresso que avisa visualmente em qual etapa da cascata o robô está.
- **NLP Feedback**: Exibe o termo "limpo" que o robô usou para pesquisar.

### [v11.0] - Analytics & Ranking
- **Ranking de Candidatos**: Tabela dinâmica com os melhores substitutos encontrados.
- **Near Misses Table**: Exibe os itens que o robô viu, mas rejeitou (e o motivo técnico).
- **Metric Dashboard**: Mostra Preço Original, Preço Achado e Economia Real.

### [v9.0] - Fidelity Controller
- **Precision Slider**: Seletor de 5 níveis (Nada Fiel até Muito Fiel) para controle do usuário.

### [v7.0] - Invisible Telemetry
- **Telemetry Engine**: Envio silencioso de logs de performance e cliques para a VM B.
- **Log Bridge**: Canal de comunicação para centralizar erros do site no log do Cérebro.

### [v6.5] - Suporte Avançado
- **Modal de Reporte**: Janela de diálogo (`st.dialog`) para coletar falhas estruturadas.
- **Categorização de Erros**: Multiselect para o usuário definir o problema (ex: "Produto Errado").

### [v5.5] - Segurança de Rede
- **Ngrok VIP Header**: Injeção automática do bypass para pular o aviso do túnel.
- **Auto-Clean URL**: Sanitização de espaços e barras extras no link do servidor.