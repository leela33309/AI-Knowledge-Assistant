# AI Knowledge Assistant

## Overview

AI Knowledge Assistant is a Retrieval-Augmented Generation (RAG) based AI system designed to help users query internal organizational knowledge using natural language.

The system supports:
- document ingestion
- semantic search
- vector embeddings
- local LLM response generation
- evaluation metrics
- export features

The project is fully local and built using open-source technologies.

---

# Features

- Upload TXT, PDF, DOCX, CSV files
- Automatic document chunking
- Semantic vector search using FAISS
- Local LLM integration using Ollama
- Retrieval-Augmented Generation (RAG)
- Streamlit chat interface
- FastAPI backend API
- Word and CSV export
- Synthetic enterprise document generation
- Evaluation framework with Recall@K
- Latency tracking and logging
- Sensitive data masking
- Knowledge graph support

---

# Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend API | FastAPI |
| LLM | Ollama (Phi3 / Llama3) |
| Embeddings | Sentence Transformers |
| Vector Database | FAISS |
| Parsing | PyMuPDF, pandas, docx |
| Evaluation | Python |
| Export | python-docx, pandas |

---

# Project Structure

```text
AI-Knowledge-Assistant/
│
├── api/
│   └── app.py
│
├── core/
│   ├── ingest.py
│   ├── rag.py
│   ├── embed_search.py
│   ├── vector_store.py
│   ├── file_loader.py
│   ├── logger.py
│   └── report.py
│
├── ui/
│   └── app.py
│
├── tools/
│   └── synth_data.py
│
├── evaluation/
│   ├── eval.py
│   └── questions.json
│
├── data/
│   ├── raw/
│   └── generated_docs/
│
├── ARCHITECTURE.md
├── requirements.txt
└── README.md
```

---

# System Workflow

```text
Documents
   ↓
Ingestion
   ↓
Chunking
   ↓
Embeddings
   ↓
FAISS Vector Store
   ↓
Retriever
   ↓
RAG Pipeline
   ↓
Ollama LLM
   ↓
FastAPI API
   ↓
Streamlit UI
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <repository-url>
cd AI-Knowledge-Assistant
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Install Ollama

Download Ollama and install locally.

Run model:

```bash
ollama run phi3
```

---

## 4. Generate Synthetic Data

```bash
python tools/synth_data.py
```

---

## 5. Start FastAPI Backend

```bash
uvicorn api.app:app --reload
```

API available at:

```text
http://127.0.0.1:8000/docs
```

---

## 6. Start Streamlit UI

```bash
streamlit run ui/app.py
```

---

# API Endpoint

## POST /ask

### Request

```json
{
  "question": "What is leave policy?"
}
```

### Response

```json
{
  "answer": "Employees are entitled to 20 paid leaves annually.",
  "sources": [],
  "latency": 0.12
}
```

---

# Evaluation

Run evaluation:

```bash
python evaluation/eval.py
```

Metrics:
- Recall@K
- Latency
- Retrieval quality

---

# Security Features

- Password-protected UI
- Regex-based sensitive data masking
- Environment variable support
- Local-only deployment

---

# Future Improvements

- Hybrid search
- Cross-encoder reranking
- Docker deployment
- Cloud deployment (AWS/Azure)
- Advanced analytics dashboard

---

# Learning Outcomes

This project demonstrates:
- Retrieval-Augmented Generation (RAG)
- Embeddings and vector databases
- Semantic search
- LLM integration
- AI system architecture
- Backend API development
- Frontend AI application design

---

# Author

Leela