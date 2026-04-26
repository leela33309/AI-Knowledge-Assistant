import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def generate_answer(query, context_chunks):
    # ✅ context_chunks is already list of strings
    context = "\n\n".join(context_chunks)

    prompt = f"""
You are an AI assistant. Answer using ONLY the given context.

Give a COMPLETE and clear answer.

Context:
{context}

Question:
{query}

Answer:
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            }
        )

        return response.json()["response"]

    except Exception as e:
        return f"❌ Error: {e}"