from enum import Enum


class State(Enum):
    INITIAL_STATE = 0
    EMAIL_RECEIVED = 1
    FINE_TUNING = 2
    WRONG_CLASSIFICATION=3


class Action(Enum):
    DELETE_MAIL = "DELETE_MAIL"
    ANSWER_MAIL = "ANSWER_MAIL"
    CREATE_MEETING = "CREATE_MEETING"
    USER_ACTION_NEEDED = "USER_ACTION_NEEDED"
    READ_MAIL = "READ_MAIL"

    def to_user_readable(self):
        readable_mapping = {
            self.DELETE_MAIL: "Mail loeschen",
            self.ANSWER_MAIL: "Mail beantworten",
            self.CREATE_MEETING: "Termin erstellen",
            self.USER_ACTION_NEEDED: "Benutzer Aktion erforderlich",
            self.READ_MAIL: "Email lesen"
        }
        return readable_mapping[self]
