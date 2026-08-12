from ollama import chat


def rewrite_query(question, history):
    history_text = ""

    for message in history:
        history_text += (
            f"{message['role']}: {message['content']}\n"
        )

    prompt = f"""
Rewrite the user's latest question into a standalone search query.

Use the conversation history to resolve references such as:
- it
- they
- them
- this
- that
- tersebut
- itu
- mereka

Do not answer the question.

Return ONLY the rewritten search query.

Conversation history:
{history_text}

Latest question:
{question}
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

    return response.message.content.strip()