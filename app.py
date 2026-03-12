import streamlit as st
import requests
import base64

st.set_page_config(page_title="JURON ⚖️", page_icon="⚖️", layout="wide")

# Tema 100% preto - apenas nome JURON
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
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .stChatMessage.user { border-left: 5px solid #555555; }
    .stChatMessage.assistant { border-left: 5px solid #777777; }
    .stChatInput textarea {
        background: #111111 !important;
        color: var(--text) !important;
        border: 1px solid #333333 !important;
    }
    .logo-container { text-align: center; margin: 120px 0 60px; }
    .title {
        font-size: 5.5rem;
        font-weight: 900;
        color: #ffffff;
        text-align: center;
        letter-spacing: 8px;
        text-transform: uppercase;
    }
    hr { border-color: #222222; margin: 40px 0; }
    .crypto-logo {
        width: 40px;
        height: 40px;
        vertical-align: middle;
        margin-right: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Logo: APENAS JURON (totalmente preto e branco)
st.markdown("""
<div class="logo-container">
  <h1 class="title">JURON</h1>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr>', unsafe_allow_html=True)

# Seção de doações com logos reais de BTC e USDT
st.subheader("💰 Apoie o JURON")
st.markdown("Doações voluntárias ajudam a manter o projeto ativo e gratuito para todos.")

donations = st.container()

with donations:
    col_pix, col_btc, col_bsc = st.columns(3)

    with col_pix:
        st.markdown("**PIX**")
        st.image("qrcode47.png", width=180)
        st.code("43999324592", language=None)

    with col_btc:
        st.markdown('<img src="https://upload.wikimedia.org/wikipedia/commons/4/46/Bitcoin.svg" class="crypto-logo">**Bitcoin (BTC)**', unsafe_allow_html=True)
        st.code("1PDgV1zEGKd2oDefucF7fmjTiaLNLKLZqg", language=None)

    with col_bsc:
        st.markdown('<img src="https://upload.wikimedia.org/wikipedia/commons/0/05/Tether_logo.svg" class="crypto-logo">**USDT - Rede BSC**', unsafe_allow_html=True)
        st.code("0x4c20c6d93797b4d4707879354ed8ed9900fbbb98", language=None)

st.markdown("---")

# ======================= RESTO DO CÓDIGO =======================

OPENROUTER_API_KEY = "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"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

uploaded_file = st.file_uploader("Envie imagem (opcional)", type=["png", "jpg", "jpeg"])

image_base64 = None
if uploaded_file is not None:
    if uploaded_file.type.startswith("image/"):
        image_bytes = uploaded_file.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        st.image(image_bytes, caption="Imagem enviada", use_column_width=True)

def chamar_juron(image_b64=None):
    system_prompt = """Você é JURON, IA jurídica útil e direta.
Especialista em Direito Brasileiro.

Seja conversacional, siga o fluxo do usuário.
Quando for análise de caso use estrutura simples:
1. Resumo dos fatos
2. Base legal
3. Riscos e próximos passos

Responda em português brasileiro.
Finalize sempre com: "Esta é uma análise geral de IA. Não substitui advogado habilitado. Consulte um profissional." """

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
    except requests.exceptions.HTTPError as e:
        return f"Erro {resp.status_code}: {resp.text}\n\nVerifique a chave no dashboard: https://openrouter.ai/keys"
    except Exception as e:
        return f"Erro geral: {str(e)}"

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Oi! Sou o JURON. Pode mandar sua dúvida jurídica ou enviar imagem.\n\nLembrete: sou IA, não substituo advogado."
    }]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Sua dúvida ou caso..."):
    full_content = prompt
    if image_base64:
        full_content += "\n\n[Imagem enviada]"
    st.session_state.messages.append({"role": "user", "content": full_content})
    with st.chat_message("user"):
        st.markdown(prompt)
        if image_base64:
            st.image(uploaded_file, width=400)
    with st.chat_message("assistant"):
        resposta = chamar_juron(image_base64)
        st.markdown(resposta)
    st.session_state.messages.append({"role": "assistant", "content": resposta})

with st.sidebar:
    if st.button("Limpar conversa", use_container_width=True):
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()
