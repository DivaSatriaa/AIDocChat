import chromadb


client = chromadb.PersistentClient(
    path="database/chroma"
)


def get_collection(room_id):
    return client.get_or_create_collection(
        name=f"room_{room_id}"
    )


def store_chunks(room_id, chunks, embeddings):
    collection = get_collection(room_id)

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