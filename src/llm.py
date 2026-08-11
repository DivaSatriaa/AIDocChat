from ollama import chat


def ask_llm(question, context):
    prompt = f"""
You are a helpful assistant answering questions based on a document.

Use ONLY the information provided in the context.

If the answer cannot be found in the context, say:
"I couldn't find the answer in the document."

When answering, cite the relevant source using its source number.
For example: [Source 1]

Context:
{context}

Question:
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

    return response.message.content