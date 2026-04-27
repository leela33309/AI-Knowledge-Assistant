import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def call_ollama(prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]


def generate_answer(query, context_chunks):
    context = "\n\n".join(context_chunks)

    # ✅ If context exists → RAG mode
    if context.strip():
        prompt = f"""
You are an AI assistant. Answer ONLY from the context below.

Context:
{context}

Question:
{query}

Answer clearly:
"""
    else:
        # ✅ No context → normal AI (ChatGPT-like)
        prompt = f"""
You are a helpful AI assistant.

User Question:
{query}

Answer:
"""

    return call_ollama(prompt)