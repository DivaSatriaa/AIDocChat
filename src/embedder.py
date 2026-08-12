from sentence_transformers import SentenceTransformer


model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)


def create_embeddings(texts):
    return model.encode(
        texts,
        batch_size=32,
        show_progress_bar=False
    )