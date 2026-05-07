from fastapi import FastAPI
from pydantic import BaseModel
import time

from core.rag import generate_answer
from core.embed_search import search

app = FastAPI()


# =========================
# REQUEST MODEL
# =========================
class QueryRequest(BaseModel):
    question: str


# =========================
# RESPONSE MODEL
# =========================
class QueryResponse(BaseModel):
    answer: str
    sources: list
    latency: float


# =========================
# ASK ENDPOINT
# =========================
@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):

    start_time = time.time()

    # Retrieve relevant chunks
    retrieved_results = search(
        request.question
    )

    retrieved_chunks = [
        item["content"]
        for item in retrieved_results
    ]

    # Generate answer
    answer = generate_answer(
        request.question,
        retrieved_chunks
    )

    latency = time.time() - start_time

    return {
        "answer": answer,
        "sources": retrieved_results,
        "latency": round(latency, 2)
    }