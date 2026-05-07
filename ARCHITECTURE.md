# AI Knowledge Assistant Architecture

## System Flow

```text
                 ┌──────────────────┐
                 │  Knowledge Docs  │
                 │ TXT / PDF / CSV  │
                 │ DOCX / JSON      │
                 └────────┬─────────┘
                          │
                          ▼
               ┌────────────────────┐
               │  Ingestion Layer   │
               │ file_loader.py     │
               │ ingest.py          │
               └────────┬───────────┘
                        │
                        ▼
               ┌────────────────────┐
               │ Text Chunking      │
               │ Metadata Creation  │
               └────────┬───────────┘
                        │
                        ▼
               ┌────────────────────┐
               │ Embedding Model    │
               │ all-MiniLM-L6-v2   │
               └────────┬───────────┘
                        │
                        ▼
               ┌────────────────────┐
               │ Vector Database    │
               │ FAISS Index        │
               └────────┬───────────┘
                        │
                        ▼
               ┌────────────────────┐
               │ Retriever          │
               │ Similarity Search  │
               └────────┬───────────┘
                        │
                        ▼
               ┌────────────────────┐
               │ RAG Pipeline       │
               │ Prompt Building    │
               │ Context Injection  │
               └────────┬───────────┘
                        │
                        ▼
               ┌────────────────────┐
               │ Ollama LLM         │
               │ Phi3 / Llama       │
               └────────┬───────────┘
                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼
┌──────────────────┐         ┌──────────────────┐
│ FastAPI Backend  │         │ Streamlit UI     │
│ /ask endpoint    │         │ Chat Interface   │
└────────┬─────────┘         └────────┬─────────┘
         │                              │
         ▼                              ▼
┌──────────────────┐         ┌──────────────────┐
│ Evaluation       │         │ Export Features  │
│ Recall@K         │         │ Word / CSV       │
│ Latency Metrics  │         └──────────────────┘
└──────────────────┘
```

---

## Components

### 1. Ingestion Layer
Handles loading and preprocessing of:
- TXT
- PDF
- DOCX
- CSV

### 2. Embedding Layer
Uses Sentence Transformers:
- all-MiniLM-L6-v2

to convert text chunks into vector embeddings.

### 3. Vector Store
FAISS stores embeddings for fast similarity search.

### 4. Retrieval Layer
Retrieves top-k relevant chunks using semantic similarity.

### 5. RAG Pipeline
Builds prompts using:
- retrieved context
- user question
- system instructions

### 6. LLM Layer
Uses Ollama local models:
- Phi3
- Llama3
- Mistral

for grounded answer generation.

### 7. API Layer
FastAPI exposes:
- POST /ask

endpoint for querying.

### 8. Frontend
Streamlit provides:
- chat interface
- file upload
- export options
- citation display

### 9. Evaluation
Measures:
- Recall@K
- latency
- retrieval quality

### 10. Security
Includes:
- password protection
- regex-based data masking
- environment variable secrets