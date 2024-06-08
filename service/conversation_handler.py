from service.agents.answer_agent.answer import AnswerAgent
from service.agents.classifier_agent.classifier import ClassifierAgent
from service.agents.delete_agent.deleter import DeleteAgent
from service.agents.meeting_agent.meeting import MeetingAgent
from service.agents.reader_agent.reader import ReaderAgent
from service.agents.useraction_agent.useraction import UserActionAgent
from service.model.enums import *
from service.utils.file_helper import FileHelper
from service.utils.gpt_helper import GptHelper


def create_action_content_json(action, content):
    return {'ACTION': action.name,
            'CONTENT': content}


class ConversationHandler:

    def __init__(self):
        self.file_helper = FileHelper()
        self.gpt_helper = GptHelper()
        self.classifier_agent = ClassifierAgent(self.file_helper, self.gpt_helper)
        self.meeting_agent = MeetingAgent(self.file_helper, self.gpt_helper)
        self.answer_agent = AnswerAgent(self.file_helper, self.gpt_helper)
        self.reader_agent = ReaderAgent(self.file_helper, self.gpt_helper)
        self.useraction_agent = UserActionAgent(self.file_helper, self.gpt_helper)
        self.delete_agent = DeleteAgent()
        self.state = State.INITIAL_STATE
        self.action = ""
        self.email_content = ""
        self.context = ""

    def parse_email(self, file):
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
            return self.handle_state_received(message)
        if self.state == State.FINE_TUNING:
            if self.action == Action.ANSWER_MAIL:
                response = self.answer_agent.answer_email_context(self.email_content, self.context, message)
                self.context += str(response)
                return {'ACTION': Action.ANSWER_MAIL.name,
                        'CONTENT': response}

        if self.state == State.WRONG_CLASSIFICATION:
            print(message)

    def handle_state_received(self, message):
        if message.lower() != 'ja':
            self.state = State.WRONG_CLASSIFICATION
            return "Es tut mir leid dass ich das Email falsch klassifiziert habe. Bitte gib mir Feedback dass ich daraus lernen kann. (Not implemented yet!)"

        if self.action == Action.CREATE_MEETING:
            content = self.meeting_agent.create_meeting_suggestion(self.email_content)
            return create_action_content_json(Action.CREATE_MEETING, content)
        elif self.action == Action.ANSWER_MAIL:
            content = self.answer_agent.answer_email(self.email_content)
            self.context += str(content)
            self.state = State.FINE_TUNING
            return create_action_content_json(Action.ANSWER_MAIL, content)
        elif self.action == Action.READ_MAIL:
            content = self.reader_agent.read_email(self.email_content)
            return create_action_content_json(Action.READ_MAIL, content)
        elif self.action == Action.DELETE_MAIL:
            content = self.delete_agent.delete_email()
            return content
        elif self.action == Action.USER_ACTION_NEEDED:
            content = self.useraction_agent.extract_user_action(self.email_content)
            return create_action_content_json(Action.USER_ACTION_NEEDED, content)
