import streamlit as st
import requests
import base64

st.set_page_config(page_title="JURON ⚖️", page_icon="⚖️", layout="wide")

# Tema 100% preto - limpo e estiloso
st.markdown("""
<style>
    :root {
        --bg: #000000;
        --text: #e0e0e0;
        --accent: #ffffff;
        --border: #222222;
    }
    .stApp { background: var(--bg); color: var(--text); }
    .stChatMessage {
        background: #0a0a0a;
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 14px;
    }
    .stChatMessage.user { border-left: 5px solid #444444; }
    .stChatMessage.assistant { border-left: 5px solid #777777; }
    .stChatInput textarea {
        background: #111111 !important;
        color: var(--text) !important;
        border: 1px solid #333333 !important;
        border-radius: 8px;
    }
    .logo-container {
        text-align: center;
        margin: 100px 0 50px;
    }
    .title {
        font-size: 5.5rem;
        font-weight: 900;
        color: #ffffff;
        text-align: center;
        letter-spacing: 10px;
        text-transform: uppercase;
        text-shadow: 0 0 20px rgba(255,255,255,0.1);
    }
    hr { border-color: #222222; margin: 40px 0; }
    /* Doações fixas no canto inferior direito - discreto */
    .donation-fixed {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: rgba(10,10,10,0.9);
        border: 1px solid #333333;
        border-radius: 12px;
        padding: 16px;
        width: 300px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.8);
        z-index: 999;
        font-size: 0.95rem;
        backdrop-filter: blur(8px);
    }
    .donation-title {
        font-size: 1.2rem;
        margin-bottom: 12px;
        text-align: center;
        color: #dddddd;
    }
    .crypto-item {
        margin: 10px 0;
        display: flex;
        align-items: center;
        font-size: 0.9rem;
    }
    .crypto-code {
        font-family: monospace;
        background: #111111;
        padding: 8px;
        border-radius: 6px;
        word-break: break-all;
        flex: 1;
    }
</style>
""", unsafe_allow_html=True)

# Logo principal: APENAS "JURON" grande e branco
st.markdown("""
<div class="logo-container">
  <h1 class="title">JURON</h1>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr>', unsafe_allow_html=True)

# Chat principal
uploaded_file = st.file_uploader("Envie imagem (opcional - print, contrato, email...)", type=["png", "jpg", "jpeg"])

image_base64 = None
if uploaded_file is not None:
    if uploaded_file.type.startswith("image/"):
        image_bytes = uploaded_file.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        st.image(image_bytes, caption="Imagem enviada", use_column_width=True)
    else:
        st.warning("Apenas imagens (png/jpg).")

def chamar_juron(image_b64=None):
    system_prompt = """Você é JURON, uma IA jurídica útil, direta e inteligente.
Especialista em Direito Brasileiro (todas as áreas).
Seja natural e conversacional: responda de forma livre, siga o fluxo da conversa, faça perguntas para esclarecer se necessário, dê continuidade às dúvidas.
Quando for análise de caso, mantenha estrutura simples:
1. Resumo dos fatos
2. Base legal (leis/artigos)
3. Riscos e próximos passos práticos
Responda sempre em português brasileiro fluente.
Seja ético: nunca incentive nada ilegal.
Finalize toda resposta com: "Esta é uma análise geral de IA. Não substitui advogado habilitado. Consulte um profissional." """
    messages = [{"role": "system", "content": system_prompt}]
    for m in st.session_state.messages:
        messages.append({"role": m["role"], "content": m["content"]})
    if image_b64:
        messages[-1]["content"] += "\n\n[Descreva esta imagem no contexto jurídico se possível]"
    payload = {
        "model": "anthropic/claude-3-haiku",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1500,
        "stream": False
    }
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "JURON"
    }
    try:
        resp = requests.post(OPENROUTER_URL, json=payload, headers=headers, timeout=45)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Erro na API: {str(e)}\n\nDetalhes: {resp.text if 'resp' in locals() else 'sem resposta do servidor'}"

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Oi! Sou o JURON. Pode mandar sua dúvida jurídica, caso ou enviar uma imagem relacionada.\n\nLembrete: sou IA, não substituo advogado."
    }]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Sua dúvida ou caso..."):
    full_content = prompt
    if image_base64:
        full_content += "\n\n[Imagem enviada para análise]"
    st.session_state.messages.append({"role": "user", "content": full_content})
    with st.chat_message("user"):
        st.markdown(prompt)
        if image_base64:
            st.image(uploaded_file, width=400)
    with st.chat_message("assistant"):
        resposta = chamar_juron(image_base64)
        st.markdown(resposta)
    st.session_state.messages.append({"role": "assistant", "content": resposta})

# Doações fixas no canto inferior direito (discretas e elegantes)
st.markdown("""
<div class="donation-fixed">
  <div class="donation-title">Apoie o JURON</div>
  <div class="crypto-item">
    <strong>PIX</strong><br>
    <div class="crypto-code">43999324592</div>
  </div>
  <div class="crypto-item">
    <strong>BTC</strong><br>
    <div class="crypto-code">1PDgV1zEGKd2oDefucF7fmjTiaLNLKLZqg</div>
  </div>
  <div class="crypto-item">
    <strong>USDT - BSC</strong><br>
    <div class="crypto-code">0x4c20c6d93797b4d4707879354ed8ed9900fbbb98</div>
  </div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    if st.button("Limpar conversa", use_container_width=True):
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()
