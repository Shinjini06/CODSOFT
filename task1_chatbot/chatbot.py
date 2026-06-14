import streamlit as st
import re
from datetime import datetime

st.set_page_config(page_title="BotX", page_icon="🤖", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
body { background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%); }
.main { background: transparent !important; }
.header { background: linear-gradient(135deg, #1e3a8a 0%, #0f766e 100%); padding: 2rem; border-radius: 12px; color: white; text-align: center; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
.header h1 { font-size: 2rem; margin: 0; }
.header p { margin: 0.5rem 0 0 0; opacity: 0.9; }
.stButton > button { background: linear-gradient(135deg, #1e3a8a 0%, #0f766e 100%); color: white; border: none; border-radius: 8px; font-weight: 600; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.15); }
</style>
""", unsafe_allow_html=True)

RULES = [
    (r'\b(hi|hello|hey|howdy)\b', "Hi! I'm BotX, your AI assistant. How can I help?"),
    (r'\b(how are you|you doing)\b', "Running perfectly! What would you like to know?"),
    (r'\b(your name|who are you)\b', "I'm BotX — an AI chatbot built with Python and Streamlit."),
    (r'\b(what can you do|help|capabilities)\b', "I can chat, solve math, answer questions, and have fun conversations!"),
    (r'\b(artificial intelligence|machine learning|ai)\b', "AI is Artificial Intelligence - machines that think and learn!"),
    (r'\bpython\b', "Python is the best language for AI and Machine Learning!"),
    (r'\bstreamlit\b', "Streamlit builds data apps in pure Python - no frontend needed!"),
    (r'\b(joke|funny|laugh)\b', "Why do programmers prefer dark mode? Because light attracts bugs! 🐛"),
    (r'\btime\b', f"Current time: {datetime.now().strftime('%I:%M %p')}"),
    (r'\b(date|today)\b', f"Today: {datetime.now().strftime('%A, %B %d, %Y')}"),
    (r'\b(bye|goodbye)\b', "Goodbye! Come back anytime!"),
    (r'\b(thanks|thank you)\b', "You're welcome!"),
]

FALLBACK = "Not sure about that. Try asking about AI, Python, math, or general questions!"

def get_response(text):
    try:
        math_expr = re.sub(r'[^0-9+\-*/().% ]', '', text)
        if math_expr and math_expr.strip() and any(c in math_expr for c in '+-*/'):
            result = eval(math_expr)
            return f"The answer is **{result}**"
    except:
        pass
    for pattern, response in RULES:
        if re.search(pattern, text, re.IGNORECASE):
            return response
    return FALLBACK

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown('<div class="header"><h1>🤖 BotX</h1><p>AI-Powered Assistant</p></div>', unsafe_allow_html=True)

if not st.session_state.messages:
    st.info("👋 Welcome! Try asking about AI, doing math, or just chatting.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["text"])

st.divider()

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "text": user_input})
    st.session_state.messages.append({"role": "assistant", "text": get_response(user_input)})
    st.rerun()

st.markdown("**Quick Actions:**")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Calculate 5+5", use_container_width=True):
        st.session_state.messages.append({"role": "user", "text": "5+5"})
        st.session_state.messages.append({"role": "assistant", "text": get_response("5+5")})
        st.rerun()

with col2:
    if st.button("What is AI?", use_container_width=True):
        st.session_state.messages.append({"role": "user", "text": "What is AI?"})
        st.session_state.messages.append({"role": "assistant", "text": get_response("AI")})
        st.rerun()

with col3:
    if st.button("Tell a Joke", use_container_width=True):
        st.session_state.messages.append({"role": "user", "text": "Tell me a joke"})
        st.session_state.messages.append({"role": "assistant", "text": get_response("joke")})
        st.rerun()

st.divider()
col1, col2 = st.columns([3, 1])
with col1:
    st.caption("CodSoft AI Internship • Task 1")
with col2:
    if st.button("Clear", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
