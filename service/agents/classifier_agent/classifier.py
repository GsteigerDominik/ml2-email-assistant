import json

from service.model.enums import Action


class ClassifierAgent:
    def __init__(self, file_helper, gpt_helper):
        self.system_prompt = file_helper.load_txt_file('./service/agents/classifier_agent/system_prompt.txt')
        self.wrapper_prompt = file_helper.load_txt_file('./service/agents/classifier_agent/wrapper_prompt.txt')
        self.gpt_helper = gpt_helper

    def classify_email(self, email):
        updated_content = self.wrapper_prompt.replace('{email_text}', email)
        json_response = self.gpt_helper.send_prompt(self.system_prompt, updated_content)
        print(json_response)
        json_response = json_response.content.replace('\'', '\"')
        action_string = json.loads(json_response)
        return Action(action_string['ACTION'])
