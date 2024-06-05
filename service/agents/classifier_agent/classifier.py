import json

from service.model.enums import Action


class ClassifierAgent:

    def __init__(self,
                 file_helper,
                 gpt_helper,
                 system_prompt_path='./service/agents/classifier_agent/system_prompt.txt',
                 wrapper_prompt_path='./service/agents/classifier_agent/wrapper_prompt.txt'
                 ):
        self.system_prompt = file_helper.load_txt_file(system_prompt_path)
        self.wrapper_prompt = file_helper.load_txt_file(wrapper_prompt_path)
        self.gpt_helper = gpt_helper

    def classify_email(self, email):
        updated_content = self.wrapper_prompt.replace('{email_text}', email)
        response = self.gpt_helper.send_prompt(self.system_prompt, updated_content)
        return Action(response['ACTION'])
