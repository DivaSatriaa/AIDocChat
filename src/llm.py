from ollama import chat


def ask_llm(question, context, history):
    history_text = ""

    for message in history:
        history_text += (
            f"{message['role']}: "
            f"{message['content']}\n"
        )

    prompt = f"""
You are a helpful assistant answering questions based on a document.

Use ONLY the information provided in the context.

If the answer cannot be found in the context, say:
"I couldn't find the answer in the document."

Conversation history:
{history_text}

Context:
{context}

Question:
{question}

Answer:
"""

    response = chat(
        model="qwen3:4b-instruct",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.message.content