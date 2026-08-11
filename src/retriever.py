from src.embedder import model
from src.vector_db import collection


def search(query, top_k=5):
    query_embedding = model.encode([query])

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k
    )

    return results