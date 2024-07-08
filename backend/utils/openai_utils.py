from openai import OpenAI

client = OpenAI()

def generate_response(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "학생과 책과 관련된 모르는 부분에 대한 질문에 답하는 역할"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error in processing text with OpenAI: {e}"
