import chromadb


client = chromadb.PersistentClient(
    path="database/chroma"
)


def get_collection(document_id):
    return client.get_or_create_collection(
        name=f"doc_{document_id}"
    )


def store_chunks(
    document_id,
    chunks,
    embeddings
):
    collection = get_collection(
        document_id
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


def search_documents(
    document_ids,
    query_embedding,
    n_results=5
):
    all_results = []

    for document_id in document_ids:

        collection = get_collection(
            document_id
        )

        if collection.count() == 0:
            continue

        results = collection.query(
            query_embeddings=[
                query_embedding.tolist()
            ],
            n_results=min(
                n_results,
                collection.count()
            ),
            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):

            all_results.append({
                "document_id": document_id,
                "text": document,
                "page": metadata["page"],
                "distance": distance
            })

    # Lower distance = more relevant
    all_results.sort(
        key=lambda item: item["distance"]
    )

    return all_results[:n_results]


def delete_document_collection(
    document_id
):
    collection_name = f"doc_{document_id}"

    try:
        client.delete_collection(
            name=collection_name
        )

    except Exception:
        pass