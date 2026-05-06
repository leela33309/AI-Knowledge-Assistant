# AI Knowledge Assistant

## Overview
AI Knowledge Assistant is a local Retrieval-Augmented Generation (RAG) system that reads internal knowledge documents and answers user questions using semantic search + local LLM.

## Features

- Upload TXT / PDF / DOCX / CSV files
- Automatic chunking and indexing
- Semantic search using FAISS
- AI Answers using Ollama (phi3)
- Citations / Sources
- Export answers to Word / CSV
- Secure Login with .env key
- Query logging and latency tracking
- Privacy masking for emails / phone numbers
- Synthetic data generator

## Tech Stack

- Python
- Streamlit
- Sentence Transformers
- FAISS
- Ollama
- Pandas
- python-docx

## Run Project

```bash
streamlit run ui/app.py