import requests
import re
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3"

# =========================
# IMPORT KNOWLEDGE GRAPH
# =========================
try:
    from core.knowledge_graph import knowledge_graph
except:
    knowledge_graph = {}

# =========================
# CACHE STORAGE
# =========================
answer_cache = {}

CACHE_EXPIRY = 1800   # 30 mins


# =========================
# PARTIAL MASKING FUNCTION
# =========================
def redact_sensitive(text):

    # Email Masking
    def mask_email(match):
        email = match.group(0)
        username, domain = email.split("@")
        visible = username[:3]
        return visible + "***@" + domain

    text = re.sub(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        mask_email,
        text
    )

    # Phone Masking
    def mask_phone(match):
        number = match.group(0)
        return "******" + number[-4:]

    text = re.sub(
        r'\b\d{10}\b',
        mask_phone,
        text
    )

    # Large Number Masking
    def mask_number(match):
        number = match.group(0)
        hidden = "*" * (len(number) - 4)
        return hidden + number[-4:]

    text = re.sub(
        r'\b\d{5,}\b',
        mask_number,
        text
    )

    return text


# =========================
# CACHE FUNCTIONS
# =========================
def get_cache_key(query, context):
    return query.lower().strip() + "||" + context[:300]


def get_cached_answer(key):

    if key in answer_cache:

        saved = answer_cache[key]

        if time.time() - saved["time"] < CACHE_EXPIRY:
            return saved["answer"]

        else:
            del answer_cache[key]

    return None


def save_cache(key, answer):

    answer_cache[key] = {
        "answer": answer,
        "time": time.time()
    }


# =========================
# KNOWLEDGE GRAPH SEARCH
# =========================
def graph_answer(query):

    q = query.lower()

    for key, values in knowledge_graph.items():

        if key.lower() in q:

            if values:
                return ", ".join(values)

    return None


# =========================
# OLLAMA CALL
# =========================
def call_ollama(prompt):

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "num_predict": 300
                }
            },
            timeout=300
        )

        response.raise_for_status()

        data = response.json()

        answer = data.get(
            "response",
            "No response generated."
        ).strip()

        return redact_sensitive(answer)

    except Exception as e:

        return f"⚠️ Error: {str(e)}"


# =========================
# GENERATE ANSWER
# =========================
def generate_answer(query, context_chunks):

    context = "\n\n".join(
        context_chunks[:2]
    )[:1200]

    context = redact_sensitive(context)

    # =========================
    # GRAPH MODE (FASTEST)
    # =========================
    graph_result = graph_answer(query)

    if graph_result:
        return f"{redact_sensitive(graph_result)}\n\n🧠 Knowledge Graph Response"

    # =========================
    # CACHE MODE
    # =========================
    cache_key = get_cache_key(
        query,
        context
    )

    cached = get_cached_answer(
        cache_key
    )

    if cached:
        return cached + "\n\n⚡ Cached Response"

    # =========================
    # RAG MODE
    # =========================
    if context.strip():

        prompt = f"""
You are an intelligent AI Knowledge Assistant.

Use ONLY the provided context to answer the question.
Do not make up facts.

If answer not found, reply:
Answer not found in uploaded knowledge base.

Context:
{context}

Question:
{query}

Give short professional answer.
"""

    # =========================
    # GENERAL MODE
    # =========================
    else:

        prompt = f"""
You are a smart and professional AI assistant.

Question:
{query}

Answer clearly.
"""

    answer = call_ollama(prompt)

    save_cache(
        cache_key,
        answer
    )

    return answer