import os

from openai import OpenAI


class GptHelper:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key)
    model = "gpt-3.5-turbo"

    def send_prompt(self, system_content, user_content):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
            ]
        )
        return response.choices[0].message
