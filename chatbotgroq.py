import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
 
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
# PAGE CONFIG
# --------------------------------------------------
 
st.set_page_config(
    page_title="IndiGo Support Assistant",
    page_icon="✈️",
    layout="centered"
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
# UI
# --------------------------------------------------
 
st.title("✈️ IndiGo Customer Support")
st.caption("Powered by Groq + LangChain")
 
# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
 
# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
 
with st.sidebar:
    st.header("Quick Questions")
 
    quick_questions = [
        "What is IndiGo baggage allowance?",
        "How do I check in online?",
        "How can I change my flight?",
        "What is the cancellation policy?"
    ]
 
    for question in quick_questions:
        if st.button(question, use_container_width=True):
            st.session_state.selected_question = question
            st.rerun()
 
    st.divider()
 
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_history = [
            SystemMessage(content=SYSTEM_PROMPT)
        ]
        st.rerun()
 
# --------------------------------------------------
# INPUT
# --------------------------------------------------
 
prompt = st.chat_input("Ask your question...")
 
# Handle sidebar question click
if "selected_question" in st.session_state:
    prompt = st.session_state.selected_question
    del st.session_state.selected_question
 
# --------------------------------------------------
# CHAT
# --------------------------------------------------
 
if prompt:
 
    # User message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
 
    st.session_state.chat_history.append(
        HumanMessage(content=prompt)
    )
 
    with st.chat_message("user"):
        st.markdown(prompt)
 
    # Assistant response
    with st.chat_message("assistant"):
 
        with st.spinner("Thinking..."):
 
            try:
                llm = get_llm()
 
                response = llm.invoke(
                    st.session_state.chat_history
                )
 
                reply = response.content
 
            except Exception as e:
                reply = f"⚠️ Error: {str(e)}"
 
            st.markdown(reply)
 
            st.session_state.chat_history.append(
                AIMessage(content=reply)
            )
 
            st.session_state.messages.append(
                {"role": "assistant", "content": reply}
            )