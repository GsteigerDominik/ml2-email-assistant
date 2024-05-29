from service.agents.answer_agent.answer import AnswerAgent
from service.agents.classifier_agent.classifier import ClassifierAgent
from service.agents.meeting_agent.meeting import MeetingAgent
from service.model.enums import *
from service.utils.file_helper import FileHelper
from service.utils.gpt_helper import GptHelper


class ConversationHandler:

    def __init__(self):
        self.file_helper = FileHelper()
        self.gpt_helper = GptHelper()
        self.classifier_agent = ClassifierAgent(self.file_helper, self.gpt_helper)
        self.meeting_agent = MeetingAgent(self.file_helper, self.gpt_helper)
        self.answer_agent = AnswerAgent(self.file_helper, self.gpt_helper)
        self.state = State.INITIAL_STATE
        self.action = ""
        self.email_content = ""
        self.context = ""

    def parse_email(self,file):
        return self.file_helper.load_email_json(file)

    def handle_email(self, file):
        email_content = self.file_helper.load_email(file)
        self.email_content = email_content
        action = self.classifier_agent.classify_email(email_content)
        self.action = action
        self.state = State.EMAIL_RECEIVED
        return f"Vorgeschlagene Aktion: {action.to_user_readable()}. Bist du mit der Aktion einverstanden? (ja/nein)"

    def handle_user_input(self, message):
        if self.state == State.EMAIL_RECEIVED:
            if message.lower() != 'ja':
                return "User doesnt want this action"

            if self.action == Action.CREATE_MEETING:
                return {'ACTION': Action.CREATE_MEETING.name,
                        'CONTENT': self.meeting_agent.create_meeting_suggestion(self.email_content)}
            elif self.action == Action.ANSWER_MAIL:
                response= self.answer_agent.answer_email(self.email_content)
                self.context += str(response)
                self.state = State.FINE_TUNING

                return {'ACTION': Action.ANSWER_MAIL.name,
                        'CONTENT': str(response)}
            elif self.action == Action.DELETE_MAIL:
                return "Das Mail wird gelöscht."

        if self.state == State.FINE_TUNING:
            if self.action == Action.ANSWER_MAIL:
                response=  self.answer_agent.answer_email_context(self.email_content, self.context, message)
                self.context += str(response)
                return {'ACTION': Action.ANSWER_MAIL.name,
                               'CONTENT': str(response)}
