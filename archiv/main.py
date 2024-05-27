import json

from zz_email_assistant.agents.classifier_agent.classifier import classify_email
from zz_email_assistant.agents.answer_agent.answer import answer_email
from zz_email_assistant.util.file_helper import load_email
from zz_email_assistant.agents.meeting_agent.meeting import create_meeting_suggestion

def main():
    email_content = load_email("information_mail.msg.msg")

    # Schritt 2: Entscheidung über den ActionType
    action_string = classify_email(email_content)
    action_string=action_string.replace('\'', '\"')
    print(action_string)
    action = json.loads(action_string)
    print(f"Vorgeschlagene Aktion: {action['ACTION']}")

    confirmation = input("Bist du mit der Entscheidung einverstanden? (ja/nein): ")
    if confirmation.lower() != 'ja':
        print("Aktion abgebrochen.")
        return

    if action['ACTION'] == 'CREATE_MEETING':
        meeting_suggestion = create_meeting_suggestion(email_content)
        print(meeting_suggestion)
    if action['ACTION'] == 'ANSWER_MAIL':
        answer = answer_email(email_content)
        print(answer)


if __name__ == "__main__":
    main()
