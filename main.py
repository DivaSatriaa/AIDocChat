from src.retriever import search
from src.llm import ask_llm
from src.chat import add_message, get_history
from src.query_rewriter import rewrite_query

ROOM_ID = "room_1"

while True:
    question = input("\nYou: ")

    if question.lower() in ["exit", "quit", "q"]:
        print("Goodbye!")
        break

    # =========================
    # 1. GET CHAT HISTORY
    # =========================

    history = get_history()

    # =========================
    # 2. REWRITE QUERY
    # =========================

    search_query = rewrite_query(
        question,
        history,
    )

    print(f"\nSearch query: {search_query}")

    # =========================
    # 3. RETRIEVAL
    # =========================

    results = search(
        ROOM_ID,
        search_query
        )

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

    # =========================
    # 4. BUILD CONTEXT
    # =========================

    context_parts = []

    for i, document in enumerate(documents):
        page = metadatas[i]["page"]

        context_parts.append(
            f"[Source {i + 1} - Page {page}]\n{document}"
        )

    context = "\n\n".join(context_parts)

    # =========================
    # 5. ASK OLLAMA
    # =========================

    answer = ask_llm(
        question,
        context,
        history
    )

    # =========================
    # 6. SAVE CHAT HISTORY
    # =========================

    add_message("user", question)
    add_message("assistant", answer)

    # =========================
    # 7. DISPLAY ANSWER
    # =========================

    print("\n================ ANSWER ================\n")
    print(answer)

    print("\n================ SOURCES ================\n")

    for i, metadata in enumerate(metadatas):
        print(
            f"[Source {i + 1}] "
            f"AIImpactForStudent.pdf - Page {metadata['page']}"
        )