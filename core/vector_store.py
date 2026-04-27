from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# ✅ Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 🔥 Create FAISS index
def create_index(chunks):
    embeddings = model.encode(chunks)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    return index, embeddings


# 🔍 Search relevant chunks
def search_index(query, index, chunks, k=3):
    query_embedding = model.encode([query])

    distances, indices = index.search(
        np.array(query_embedding),
        k
    )

    results = [chunks[i] for i in indices[0]]
    return results