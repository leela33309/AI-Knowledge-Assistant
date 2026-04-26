import os
import json

DATA_PATH = r"C:\AI-Knowledge-Assistant\data\raw"

CHUNK_SIZE = 300  # ✅ better chunking

def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("content", "")

def chunk_text(text, size):
    return [text[i:i+size] for i in range(0, len(text), size)]

def process_files():
    all_chunks = []

    print("Reading from:", DATA_PATH)

    for file in os.listdir(DATA_PATH):
        path = os.path.join(DATA_PATH, file)

        if file.endswith(".txt"):
            text = read_txt(path)
        elif file.endswith(".json"):
            text = read_json(path)
        else:
            continue

        chunks = chunk_text(text, CHUNK_SIZE)

        for chunk in chunks:
            all_chunks.append({
                "source": file,
                "content": chunk
            })

    return all_chunks


if __name__ == "__main__":
    chunks = process_files()

    print("\n✅ Total chunks:", len(chunks))

    for i, chunk in enumerate(chunks[:5]):
        print(f"\nChunk {i+1}:")
        print(chunk["content"])