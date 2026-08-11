from src.pdf_loader import load_pdf
from src.chunker import chunk_text
from src.embedder import create_embeddings
from src.vector_db import store_chunks
from src.retriever import search
from src.llm import ask_llm


# =========================
# 1. LOAD PDF
# =========================

pages = load_pdf("data/AIImpactForStudent.pdf")

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


# =========================
# 2. CREATE EMBEDDINGS
# =========================

texts = [chunk["text"] for chunk in all_chunks]

embeddings = create_embeddings(texts)

print("\nEmbedding shape:")
print(embeddings.shape)


# =========================
# 3. STORE TO VECTOR DB
# =========================

store_chunks(
    all_chunks,
    embeddings
)

print("Chunks successfully stored.")


# =========================
# 4. ASK QUESTION
# =========================

question = input("\nAsk something about the document: ")

results = search(question)

documents = results["documents"][0]

context = "\n\n".join(documents)


# =========================
# 5. ASK LLM
# =========================

answer = ask_llm(
    question,
    context
)

print("\n================ ANSWER ================\n")
print(answer)