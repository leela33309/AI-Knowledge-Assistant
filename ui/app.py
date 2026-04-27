import streamlit as st
import sys
import os

# ✅ Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.embed_search import search
from core.rag import generate_answer
from core.file_loader import load_uploaded_file  # ✅ returns chunks now
from core.vector_store import create_index, search_index

# ✅ Fix Streamlit watcher issue (Python 3.13+)
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

st.set_page_config(page_title="AI Assistant", layout="wide")

st.title("🤖 AI Knowledge Assistant")

# =========================
# ✅ SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# 🔥 store chunks instead of full text
if "file_chunks" not in st.session_state:
    st.session_state.file_chunks = []

# =========================
# 📄 FILE UPLOAD
# =========================
uploaded_file = st.file_uploader(
    "📄 Upload a document (TXT or PDF)",
    type=["txt", "pdf"]
)

if uploaded_file:
    file_chunks = load_uploaded_file(uploaded_file)  # ✅ already chunked

    if file_chunks:
        st.session_state.file_chunks = file_chunks
        st.success("✅ File uploaded & processed successfully!")
    else:
        st.warning("⚠️ Could not read file")

# =========================
# 🤝 SMALL TALK
# =========================
def is_small_talk(query):
    greetings = ["hi", "hello", "hey", "how are you", "good morning"]
    return query.lower().strip() in greetings

# =========================
# 🔍 SIMPLE CHUNK RETRIEVAL
# =========================
def get_relevant_chunks(query, chunks):
    query = query.lower()

    matched = [
        chunk for chunk in chunks
        if query in chunk.lower()
    ]

    # fallback if no match
    if not matched:
        return chunks[:3]

    return matched[:3]

# =========================
# 🧠 HANDLE QUERY
# =========================
def handle_query():
    query = st.session_state.input_text.strip()

    if not query:
        return

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    # 🔍 Retrieve from base knowledge
    results = search(query, k=3)

    context_chunks = [
        r["content"] if isinstance(r, dict) else str(r)
        for r in results
    ]

    # 🔥 Add uploaded file chunks (SMART)
    if st.session_state.file_chunks:
        relevant_chunks = get_relevant_chunks(
            query,
            st.session_state.file_chunks
        )
        context_chunks.extend(relevant_chunks)

    # 🔥 Hybrid logic
    if is_small_talk(query):
        answer = "Hi 😊 How can I help you today?"

    elif any(context_chunks):
        answer = generate_answer(query, context_chunks)

    else:
        answer = generate_answer(query, [])

    # Save bot response
    st.session_state.messages.append({
        "role": "bot",
        "content": answer
    })

    # Clear input
    st.session_state.input_text = ""

# =========================
# 💬 CHAT DISPLAY
# =========================
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"🧑 **{msg['content']}**")
    else:
        st.markdown(f"🤖 {msg['content']}")

# =========================
# ⌨️ INPUT BOX
# =========================
st.text_input(
    "Type your question:",
    key="input_text",
    placeholder="Ask anything...",
    on_change=handle_query
)

# =========================
# 🎨 UI CLEANUP
# =========================
st.markdown("""
<style>
div[data-baseweb="input"] input {
    border: 1px solid #ccc !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)