import streamlit as st
import sys
import os

# ✅ Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.embed_search import search
from core.rag import generate_answer

st.set_page_config(page_title="AI Assistant", layout="wide")

st.title("🤖 AI Knowledge Assistant")

# ✅ Initialize session
if "messages" not in st.session_state:
    st.session_state.messages = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# ✅ Function to handle input submission
def handle_query():
    query = st.session_state.input_text.strip()

    if not query:
        return

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    # 🔍 Retrieve
    results = search(query, k=3)

    # ✅ Safe conversion (prevents earlier errors)
    context_chunks = [
        r["content"] if isinstance(r, dict) else str(r)
        for r in results
    ]

    # 🧠 Generate answer
    answer = generate_answer(query, context_chunks)

    # Save bot response
    st.session_state.messages.append({
        "role": "bot",
        "content": answer
    })

    # ✅ Clear input safely (ONLY inside callback)
    st.session_state.input_text = ""

# ✅ Display chat
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"🧑 **{msg['content']}**")
    else:
        st.markdown(f"🤖 {msg['content']}")

# ✅ Input box (Enter triggers automatically)
st.text_input(
    "Type your question:",
    key="input_text",
    placeholder="Ask something...",
    on_change=handle_query
)

# ✅ OPTIONAL: remove red border styling completely
st.markdown("""
<style>
div[data-baseweb="input"] input {
    border: 1px solid #ccc !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)