from email_assistant.util.file_helper import load_txt_file
from email_assistant.util.gpt_helper import send_prompt

system_prompt = load_txt_file('./system_prompt.txt')
wrapper_prompt = load_txt_file('./wrapper_prompt.txt')


def classify_email(email):
    updated_content = wrapper_prompt.replace('{email_text}', email)
    response = send_prompt(system_prompt, updated_content)
    return response.content
