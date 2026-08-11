import chromadb

client = chromadb.PersistentClient(
    path="database/chroma"
)

collection = client.get_or_create_collection(
    name="documents"
)


def store_chunks(chunks, embeddings):

    # Hapus data lama
    collection.delete(
        ids=collection.get()["ids"]
    )

    ids = [
        f"chunk_{i}"
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        embeddings=embeddings.tolist(),
        documents=[
            chunk["text"]
            for chunk in chunks
        ],
        metadatas=[
            {
                "page": chunk["page"]
            }
            for chunk in chunks
        ]
    )