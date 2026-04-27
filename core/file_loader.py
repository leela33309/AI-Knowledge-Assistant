import PyPDF2

# 🔥 Split text into chunks
def split_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


# 📄 Load uploaded file
def load_uploaded_file(uploaded_file):
    text = ""

    if uploaded_file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""

    elif uploaded_file.type == "text/plain":
        text = uploaded_file.read().decode("utf-8")

    # 🔥 IMPORTANT: return chunks instead of full text
    return split_text(text)