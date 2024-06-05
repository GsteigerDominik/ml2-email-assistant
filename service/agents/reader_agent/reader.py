class ReaderAgent:
    def __init__(self, file_helper, gpt_helper):
        self.system_prompt = file_helper.load_txt_file('./service/agents/reader_agent/system_prompt.txt')
        self.wrapper_prompt = file_helper.load_txt_file('./service/agents/reader_agent/wrapper_prompt.txt')
        self.gpt_helper = gpt_helper

    def read_email(self, email):
        updated_content = self.wrapper_prompt.replace('{email_text}', email)
        response = self.gpt_helper.send_prompt(self.system_prompt, updated_content)
        return response
