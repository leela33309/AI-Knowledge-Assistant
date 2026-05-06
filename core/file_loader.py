import os
import re
import pandas as pd
import docx

# Safe PDF import
try:
    import fitz
except:
    fitz = None


# =========================
# KNOWLEDGE GRAPH STORAGE
# =========================
knowledge_graph = {}


# =========================
# CLEAN TEXT
# =========================
def clean_text(text):
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s.,:/()-]', '', text)
    return text.strip()


# =========================
# BUILD KNOWLEDGE GRAPH
# =========================
def build_knowledge_graph(text):

    global knowledge_graph

    lines = text.split(".")

    for line in lines:

        line = line.strip()

        if ":" in line:

            parts = line.split(":", 1)

            key = parts[0].strip().lower()
            value = parts[1].strip()

            if key and value:
                knowledge_graph[key] = value

        elif "-" in line:

            parts = line.split("-", 1)

            key = parts[0].strip().lower()
            value = parts[1].strip()

            if key and value:
                knowledge_graph[key] = value


# =========================
# GET GRAPH ANSWER
# =========================
def search_knowledge_graph(query):

    query = query.lower()

    for key, value in knowledge_graph.items():

        if key in query:
            return f"{key.title()}: {value}"

    return None


# =========================
# SMART CHUNKING WITH META
# =========================
def chunk_text(
    text,
    chunk_size=220,
    overlap=40,
    source="File",
    page=1,
    file_type="unknown"
):

    words = text.split()
    chunks = []
    chunk_id = 1

    step = chunk_size - overlap

    for i in range(0, len(words), step):

        chunk_words = words[i:i + chunk_size]

        if not chunk_words:
            continue

        chunk = " ".join(chunk_words)

        chunks.append({
            "content": chunk,
            "source": source,
            "page": page,
            "chunk": chunk_id,
            "file_type": file_type,
            "word_count": len(chunk_words)
        })

        chunk_id += 1

    return chunks


# =========================
# TXT
# =========================
def read_txt(file):

    text = file.read().decode(
        "utf-8",
        errors="ignore"
    )

    text = clean_text(text)

    build_knowledge_graph(text)

    return chunk_text(
        text=text,
        source=file.name,
        page=1,
        file_type="txt"
    )


# =========================
# PDF
# =========================
def read_pdf(file):

    if fitz is None:
        return []

    pdf = fitz.open(
        stream=file.read(),
        filetype="pdf"
    )

    all_chunks = []

    for page_num, page in enumerate(pdf, start=1):

        text = page.get_text()

        text = clean_text(text)

        build_knowledge_graph(text)

        page_chunks = chunk_text(
            text=text,
            source=file.name,
            page=page_num,
            file_type="pdf"
        )

        all_chunks.extend(page_chunks)

    return all_chunks


# =========================
# DOCX
# =========================
def read_docx(file):

    doc = docx.Document(file)

    text = "\n".join(
        [
            p.text for p in doc.paragraphs
            if p.text.strip()
        ]
    )

    text = clean_text(text)

    build_knowledge_graph(text)

    return chunk_text(
        text=text,
        source=file.name,
        page=1,
        file_type="docx"
    )


# =========================
# CSV
# =========================
def read_csv(file):

    df = pd.read_csv(file)

    text = df.to_string(index=False)

    text = clean_text(text)

    build_knowledge_graph(text)

    return chunk_text(
        text=text,
        source=file.name,
        page=1,
        file_type="csv"
    )


# =========================
# MAIN LOADER
# =========================
def load_uploaded_file(uploaded_file):

    ext = os.path.splitext(
        uploaded_file.name
    )[1].lower()

    try:

        if ext == ".txt":
            return read_txt(uploaded_file)

        elif ext == ".pdf":
            return read_pdf(uploaded_file)

        elif ext == ".docx":
            return read_docx(uploaded_file)

        elif ext == ".csv":
            return read_csv(uploaded_file)

        else:
            return []

    except Exception as e:

        return [{
            "content": f"Error reading file: {str(e)}",
            "source": uploaded_file.name,
            "page": 1,
            "chunk": 1,
            "file_type": ext.replace(".", "")
        }]