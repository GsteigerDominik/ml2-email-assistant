from openai import OpenAI

client = OpenAI(api_key="REPLACE ME")
model = "gpt-3.5-turbo"


def send_prompt(system_content, user_content):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]
    )
    return response.choices[0].message
