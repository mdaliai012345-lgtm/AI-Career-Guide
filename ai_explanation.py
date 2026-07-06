from openai import OpenAI
client = OpenAI(
api_key = "YOUR_API_KEY"
)
def get_ai_advice(career):
    prompt = f"""The recommended career is {career}.
    Explain:
    1. Why this career is suitable.
    2. What skills are required for this career.
    3. What skills the user needs to devlop.
    4. Future scope of this career.
    5. motivation for this career.
    keep the answers short.
    """
    response = client.responses.create(
        model = "gpt-5.5",
        input = prompt,
    )
    return response.output_texts