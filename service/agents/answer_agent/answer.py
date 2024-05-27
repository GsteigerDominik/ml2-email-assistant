import json


class AnswerAgent:

    def __init__(self, file_helper, gpt_helper):
        self.system_prompt = file_helper.load_txt_file('./service/agents/answer_agent/system_prompt3.txt')
        self.wrapper_prompt = file_helper.load_txt_file('./service/agents/answer_agent/wrapper_prompt.txt')
        self.gpt_helper = gpt_helper

    def answer_email(self, email):
        updated_content = self.wrapper_prompt.replace('{email_text}', email)
        response = self.gpt_helper.send_prompt(self.system_prompt, updated_content)
        response_json = json.loads(response.content.replace('\'', '\"'))
        return response.content

    def answer_email_context(self, email,context,feedback):
        updated_content = self.wrapper_prompt.replace('{email_text}', email)
        updated_content = updated_content.replace('{context}', context)
        updated_content = updated_content.replace('{feedback}', feedback)
        response = self.gpt_helper.send_prompt(self.system_prompt, updated_content)
        response_json = json.loads(response.content.replace('\'', '\"'))
        return response.content