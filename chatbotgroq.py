import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import base64
from pathlib import Path
from PIL import Image
 
# --------------------------------------------------
# CONFIG
# --------------------------------------------------
 
MODEL = "llama-3.1-8b-instant"
 
SYSTEM_PROMPT = """
You are IndiGo Airlines' AI customer support assistant.
 
Guidelines:
- Answer politely and professionally.
- If you are unsure, say so instead of making up information.
- Keep responses concise and helpful.
"""
# --------------------------------------------------
# LOGO CONFIG
# --------------------------------------------------
 
LOGO_PATH = r"C:\Users\rouna\Pictures\final project\download.jpg"
 
def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()
 
logo_base64 = get_base64_image(LOGO_PATH)
logo_icon = Image.open(LOGO_PATH)
# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
 
st.set_page_config(
    page_title="IndiGo Support Assistant",
    page_icon=logo_icon,
    layout="centered"
)
 
# --------------------------------------------------
# INDIGO BRAND STYLES
# IndiGo brand blue: #001B94  |  Orange accent: #FF6600
# White: #FFFFFF               |  Light bg: #F0F4FF
# --------------------------------------------------
 
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
 
  /* Apply font globally without breaking anything */
  html, body { font-family: 'Inter', sans-serif !important; }
 
  /* ── Custom header card ── */
  .indigo-header {
    background: linear-gradient(135deg, #001B94 0%, #0025C8 100%);
    padding: 20px 24px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 0;
    box-shadow: 0 6px 24px rgba(0,27,148,0.30);
  }
  .indigo-header-text h2 {
    color: #FFFFFF;
    font-size: 1.4rem;
    font-weight: 700;
    margin: 0 0 2px 0;
  }
  .indigo-header-text p {
    color: rgba(255,255,255,0.72);
    font-size: 0.78rem;
    margin: 0;
  }
  .indigo-logo-box {
    background: rgba(255,255,255,0.15);
    border-radius: 10px;
    padding: 8px 10px;
    font-size: 1.8rem;
    line-height: 1;
  }
 
  /* ── Orange accent stripe ── */
  .orange-stripe {
    height: 4px;
    background: linear-gradient(90deg, #FF6600 0%, #FF9933 100%);
    border-radius: 0 0 4px 4px;
    margin-bottom: 20px;
  }
 
  /* ── Sidebar header ── */
  .sidebar-heading {
    color: #001B94 !important;
    font-weight: 700;
    font-size: 1rem;
    margin-bottom: 4px;
  }
  .sidebar-footer {
    font-size: 0.72rem;
    color: #888;
    text-align: center;
    margin-top: 24px;
    line-height: 1.6;
  }
 
  /* ── User chat bubble: blue bg, white text ── */
  [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background-color: #001B94 !important;
    border-radius: 12px !important;
    padding: 4px 8px !important;
  }
  [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) p,
  [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) span {
    color: #FFFFFF !important;
  }
 
  /* ── Assistant bubble: white card ── */
  [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    background-color: #FFFFFF !important;
    border: 1.5px solid #D0DCFF !important;
    border-radius: 12px !important;
    padding: 4px 8px !important;
  }
  [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) p,
  [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) span {
    color: #1A1A2E !important;
  }
 
  /* ── Chat input box — only border, background stays Streamlit's own ── */
  [data-testid="stChatInput"] {
    border: 2px solid #001B94 !important;
    border-radius: 12px !important;
  }
  [data-testid="stChatInput"]:focus-within {
    border-color: #FF6600 !important;
    box-shadow: 0 0 0 3px rgba(255,102,0,0.12) !important;
  }
 
  /* ── Sidebar blue background ── */
  [data-testid="stSidebar"] > div:first-child {
    background-color: #001B94 !important;
  }
  /* Sidebar text white */
  [data-testid="stSidebar"] p,
  [data-testid="stSidebar"] span,
  [data-testid="stSidebar"] label,
  [data-testid="stSidebar"] h1,
  [data-testid="stSidebar"] h2,
  [data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
  }
  /* Sidebar buttons */
  [data-testid="stSidebar"] .stButton > button {
    background-color: rgba(255,255,255,0.12) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255,255,255,0.28) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
  }
  [data-testid="stSidebar"] .stButton > button:hover {
    background-color: #FF6600 !important;
    border-color: #FF6600 !important;
    color: #FFFFFF !important;
  }
  [data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.2) !important;
  }
</style>
""", unsafe_allow_html=True)
# --------------------------------------------------
# HEADER
# --------------------------------------------------
 
st.markdown(
    f"""
    <div class="indigo-header">
        <img
            src="data:image/jpeg;base64,{logo_base64}"
            style="
                width:70px;
                height:70px;
                object-fit:contain;
                background:white;
                padding:4px;
                border-radius:10px;
            "
        />
        <div>
            <h1>IndiGo Customer Support</h1>
            <p>India's largest airline · Available 24/7 · IATA: 6E</p>
        </div>
    </div>
    <div class="orange-bar"></div>
    """,
    unsafe_allow_html=True
)
 
# --------------------------------------------------
# LLM
# --------------------------------------------------
 
@st.cache_resource
def get_llm():
    return ChatGroq(
        api_key=st.secrets["GROQ_API_KEY"],
        model_name=MODEL,
        temperature=0.7,
        max_tokens=1024
    )
 
# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
 
if "messages" not in st.session_state:
    st.session_state.messages = []
 
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        SystemMessage(content=SYSTEM_PROMPT)
    ]
 
# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------
 
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
 
# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
 
with st.sidebar:
    st.markdown("### ✈️ Quick Questions")
    st.markdown("---")
 
    quick_questions = [
        "🧳 Baggage allowance?",
        "📱 How to check in online?",
        "🔄 How to change my flight?",
        "❌ Cancellation policy?",
        "💺 Seat selection options?",
        "🌐 International routes?",
    ]
 
    for question in quick_questions:
        if st.button(question, use_container_width=True):
            st.session_state.selected_question = question
            st.rerun()
 
    st.markdown("---")
 
    with st.container():
        st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.chat_history = [
                SystemMessage(content=SYSTEM_PROMPT)
            ]
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
 
    st.markdown("""
    <div style='margin-top: 32px; font-size: 0.75rem; opacity: 0.6; text-align: center;'>
        Powered by Groq + LangChain<br/>
        IndiGo Airlines · 6E
    </div>
    """, unsafe_allow_html=True)
 
# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------
 
prompt = st.chat_input("Ask about flights, baggage, check-in...")
 
# Handle sidebar question click
if "selected_question" in st.session_state:
    prompt = st.session_state.selected_question
    del st.session_state.selected_question
 
# --------------------------------------------------
# CHAT LOGIC
# --------------------------------------------------
 
if prompt:
 
    # Show welcome tip only on first message
    if len(st.session_state.messages) == 0:
        pass
 
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.chat_history.append(HumanMessage(content=prompt))
 
    with st.chat_message("user"):
        st.markdown(prompt)
 
    # Assistant response
    with st.chat_message("assistant"):
        with st.spinner("IndiGo is looking into that..."):
            try:
                llm = get_llm()
                response = llm.invoke(st.session_state.chat_history)
                reply = response.content
            except Exception as e:
                reply = f"⚠️ Error: {str(e)}"
 
        st.markdown(reply)
 
        st.session_state.chat_history.append(AIMessage(content=reply))
        st.session_state.messages.append({"role": "assistant", "content": reply})
