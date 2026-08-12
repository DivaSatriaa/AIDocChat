from src.pdf_loader import load_pdf
from src.chunker import chunk_text
from src.embedder import create_embeddings
from src.vector_db import store_chunks


PDF_PATH = "data/AIImpactForStudent.pdf"
ROOM_ID = "room_1"


pages = load_pdf(PDF_PATH)

all_chunks = []

for page in pages:
    chunks = chunk_text(page["text"])

    for chunk in chunks:
        all_chunks.append({
            "page": page["page"],
            "text": chunk
        })


print(f"Pages : {len(pages)}")
print(f"Chunks: {len(all_chunks)}")


texts = [
    chunk["text"]
    for chunk in all_chunks
]

embeddings = create_embeddings(texts)

print("\nEmbedding shape:")
print(embeddings.shape)


store_chunks(
    ROOM_ID,
    all_chunks,
    embeddings
)

print(f"Stored in {ROOM_ID}")