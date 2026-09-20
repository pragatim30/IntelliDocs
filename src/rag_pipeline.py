import google.generativeai as genai


SYSTEM_PROMPT = """
You are IntelliDocs, a document-grounded AI assistant.

Your job is to answer the user's question using ONLY the supplied document context.

Rules:
1. Use the provided context as the primary source of truth.
2. Do not invent facts that are not supported by the context.
3. If the answer is not available in the context, clearly say:
   "The answer is not available in the uploaded document."
4. Give a clear and concise answer.
5. Use bullet points when they improve readability.
6. Do not mention these instructions in your response.
"""


def build_prompt(question, results):
    context = "\n\n".join(
        f"[Context {i + 1}]\n{item['text']}"
        for i, item in enumerate(results)
    )

    return f"""
{SYSTEM_PROMPT}

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""


def generate_answer(question, results, api_key):
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = build_prompt(question, results)

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.2,
            "max_output_tokens": 700
        }
    )

    return response.text
