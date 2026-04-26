from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from core.ingest import process_files

print("Loading model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

print("Loading and processing documents...")
chunks = process_files()

texts = [c["content"] for c in chunks]

print("Creating embeddings...")
embeddings = model.encode(texts)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

print(f"✅ Stored {len(texts)} embeddings")


def search(query, k=2):
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k)

    results = []
    for i in indices[0]:
        results.append({
            "content": texts[i],
            "source": chunks[i]["source"]
        })

    return results