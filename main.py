from src.retriever import search
from src.llm import ask_llm


while True:
    question = input("\nYou: ")

    if question.lower() in ["exit", "quit", "q"]:
        print("Goodbye!")
        break

    results = search(question)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    print("\n================ RETRIEVAL ================\n")

    for i, document in enumerate(documents):
        print(f"Result {i + 1}")
        print(f"Page     : {metadatas[i]['page']}")
        print(f"Distance : {distances[i]}")
        print(f"Content  : {document[:300]}")
        print("-" * 60)

    context_parts = []

    for i, document in enumerate(documents):
        page = metadatas[i]["page"]

        context_parts.append(
            f"[Source {i + 1} - Page {page}]\n{document}"
        )

    context = "\n\n".join(context_parts)

    answer = ask_llm(
        question,
        context
    )

    print("\n================ ANSWER ================\n")
    print(answer)

    print("\n================ SOURCES ================\n")

    for i, metadata in enumerate(metadatas):
        print(
            f"[Source {i + 1}] "
            f"AIImpactForStudent.pdf - Page {metadata['page']}"
        )