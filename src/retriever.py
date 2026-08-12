from src.embedder import model
from src.vector_db import get_collection


def search(room_id, query, top_k=8):
    collection = get_collection(room_id)

    query_embedding = model.encode([query])

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k
    )

    return results  