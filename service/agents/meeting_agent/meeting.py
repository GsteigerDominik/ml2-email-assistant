from datetime import datetime


class MeetingAgent:
    def __init__(self, file_helper, gpt_helper):
        self.system_prompt = file_helper.load_txt_file('./service/agents/meeting_agent/system_prompt.txt')
        dt = datetime.now()
        self.system_prompt = self.system_prompt.replace('{today}', str(dt) + " " + dt.strftime('%A'))
        self.wrapper_prompt = file_helper.load_txt_file('./service/agents/meeting_agent/wrapper_prompt.txt')
        self.gpt_helper = gpt_helper

    def create_meeting_suggestion(self, email):
        updated_content = self.wrapper_prompt.replace('{email_text}', email)
        response = self.gpt_helper.send_prompt(self.system_prompt, updated_content)
        return response.content
