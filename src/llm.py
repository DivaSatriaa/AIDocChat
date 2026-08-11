import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def ask_llm(question, context):
    prompt = f"""
You are a helpful assistant answering questions based on the provided documents.

Use ONLY the information from the context.

If the answer cannot be found in the context, say:
"I couldn't find the answer in the document."

Context:
{context}

Question:
{question}
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text