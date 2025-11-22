import streamlit as st
st.set_page_config(page_title="Juron - Consulta Jurídica", page_icon="⚖️", layout="centered")

from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI

# Verifica premium
model = "gpt-4o" if st.session_state.get("premium", False) else "gpt-4o-mini"
llm = ChatOpenAI(model=model, temperature=0.2)

# ========================= ESTILO GLOBAL =========================
st.markdown("""
<style>
    .stApp {background:#000; color:white; padding:20px;}
    .main-title {font-size:82px; font-weight:900; text-align:center; color:white; margin:10px 0;}
    .subtitle {font-size:34px; text-align:center; color:#ccc; margin-top:-20px;}
    .pix-box {background:#111; padding:35px; border-radius:20px; border:2px solid #00ff41; text-align:center;}
    .stButton>button {
        background:#111;
        color:white;
        border:2px solid #555;
        border-radius:15px;
        height:65px;
        font-size:22px;
        font-weight:bold;
    }
    .stButton>button:hover {border-color:white; background:#222;}
    .stTextArea textarea {
        background:#0a0a0a;
        color:white;
        border:2px solid #333;
        border-radius:15px;
    }
</style>
""", unsafe_allow_html=True)

# ========================= LOGO =========================
st.image("juron logo.png", width=240)

# ========================= TÍTULOS =========================
st.markdown('<h1 class="main-title">JURON</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">CONSULTA JURÍDICA</p>', unsafe_allow_html=True)
st.markdown("—"*40)

# ========================= PREMIUM =========================
if st.session_state.get("premium"):
    st.success("PREMIUM ATIVO – GPT-4o completo")
else:
    st.info("Versão gratuita • Libere o Premium por apenas R$ 47/mês")

if not st.session_state.get("premium"):
    if st.button("LIBERAR ACESSO PREMIUM – R$ 47/mês", use_container_width=True):
        st.session_state.show_pix = True

    if st.session_state.get("show_pix"):
        st.markdown("<div class='pix-box'>", unsafe_allow_html=True)
        st.markdown("### Pague via PIX – R$ 47,00 (mensal)")

        # QR CODE salvo na pasta juron
        st.image("qrcode47.png", width=300)

        # Chave PIX
        st.markdown("### Chave PIX (copia e cola):")
        st.code("43999324592", language=None)

        st.markdown("Após o pagamento clique abaixo:")

        if st.button("Já paguei – Ativar Premium"):
            st.session_state.premium = True
            st.session_state.show_pix = False
            st.balloons()
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

# ========================= CONSULTA =========================
pergunta = st.text_area(
    "",
    placeholder="Descreva seu caso completo (golpe cripto, divórcio, contrato...)",
    height=200,
    label_visibility="collapsed"
)

if st.button("CONSULTAR JURON ⚖️", use_container_width=True):
    if pergunta.strip():
        with st.spinner("Juron analisando..."):
            prompt = f"""
            Você é o JURON, IA jurídica brasileira especialista.
            Pergunta: {pergunta}
            Responda em português perfeito, com passo a passo e aviso ético.
            """
            resp = llm.invoke(prompt)
        st.success("Resposta completa")
        st.markdown(resp.content)
        st.info("Esta é apenas uma orientação geral. Consulte um advogado.")
    else:
        st.warning("Descreva seu caso")

# ========================= RODAPÉ =========================
st.markdown(
    "<div style='text-align:center; margin-top:80px; color:#666; font-size:16px;'>"
    "<strong>JURON</strong> • 2025 • www.juron.com</div>",
    unsafe_allow_html=True
)
