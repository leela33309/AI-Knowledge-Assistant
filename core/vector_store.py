import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# =========================
# LAZY LOAD MODEL (FAST STARTUP)
# =========================
model = None

index = None
stored_chunks = []
stored_embeddings = None


# =========================
# LOAD MODEL ONLY WHEN NEEDED
# =========================
def get_model():
    global model

    if model is None:
        model = SentenceTransformer("all-MiniLM-L6-v2")

    return model


# =========================
# CREATE INDEX
# =========================
def create_index(chunks):
    global index, stored_chunks, stored_embeddings

    stored_chunks = chunks

    texts = []

    for chunk in chunks:
        if isinstance(chunk, dict):
            texts.append(chunk["content"])
        else:
            texts.append(str(chunk))

    # Load model here only
    embed_model = get_model()

    embeddings = embed_model.encode(texts)
    embeddings = np.array(embeddings).astype("float32")

    stored_embeddings = embeddings

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)


# =========================
# SEARCH INDEX
# =========================
def search_index(
    query,
    top_k=5,
    file_type=None,
    source_name=None
):
    global index, stored_chunks

    if index is None:
        return []

    # Load model here only
    embed_model = get_model()

    query_embedding = embed_model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(
        query_embedding,
        top_k * 3
    )

    results = []

    for rank, idx in enumerate(indices[0]):

        if idx >= len(stored_chunks):
            continue

        chunk = stored_chunks[idx]

        if isinstance(chunk, dict):

            # =========================
            # METADATA FILTERING
            # =========================
            if file_type:
                if chunk.get(
                    "file_type",
                    ""
                ).lower() != file_type.lower():
                    continue

            if source_name:
                if chunk.get(
                    "source",
                    ""
                ).lower() != source_name.lower():
                    continue

            # Distance score
            chunk["score"] = float(
                distances[0][rank]
            )

            results.append(chunk)

        else:

            results.append({
                "content": str(chunk),
                "score": float(
                    distances[0][rank]
                )
            })

        if len(results) >= top_k:
            break

    return results