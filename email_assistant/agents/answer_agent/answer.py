import json

from email_assistant.util.file_helper import load_txt_file
from email_assistant.util.gpt_helper import send_prompt

system_prompt = load_txt_file('./system_prompt3.txt')
wrapper_prompt = load_txt_file('./wrapper_prompt.txt')


def answer_email(email):
    updated_content = wrapper_prompt.replace('{email_text}', email)
    response = send_prompt(system_prompt, updated_content)
    response_json = json.loads(response.content.replace('\'', '\"'))
    print('Meine Vorgeschlagene Antwort auf die Email:'+response_json['email_response'])
    #for question in response_json['questions']:
    #    user_answer = input(question)
    #    updated_content += '\n Antwort auf deine Frage: ' + question + ' : ' + user_answer
    user_improvments = input('Verbesserungsvorschläge: ')
    updated_content += '\n Verbesserungsvorschläge vom User: ' + user_improvments
    response = send_prompt(system_prompt, updated_content)
    return response.content
