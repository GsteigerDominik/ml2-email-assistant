import os
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from service.agents.classifier_agent.classifier import ClassifierAgent
from service.model.enums import Action
from service.utils.file_helper import FileHelper
from service.utils.gpt_helper import GptHelper


# Helper Method

def test_classification(directory, expected, total, correct):
    files = os.listdir(directory)
    for file in files:
        total += 1
        email = file_helper.load_email(directory + file)
        actual = classifier_agent.classify_email(email)
        if expected == actual:
            correct += 1
    return total, correct


# SETUP
total = 0
correct = 0
file_helper = FileHelper()
classifier_agent = ClassifierAgent(
    file_helper,
    GptHelper(),
    system_prompt_path='../service/agents/classifier_agent/system_prompt.txt',
    wrapper_prompt_path='../service/agents/classifier_agent/wrapper_prompt.txt')

print("Running ANSWER_MAIL Test")
total, correct = test_classification('./ANSWER_MAIL/', Action.ANSWER_MAIL, total, correct)
print(f"Results after ANSWER_MAIL Total: {total}, Correct {correct}")
print("Running CREATE_MEETING Test")
total, correct = test_classification('./CREATE_MEETING/', Action.CREATE_MEETING, total, correct)
print(f"Results after CREATE_MEETING Total: {total}, Correct {correct}")
print("Running DELETE_MAIL Test")
total, correct = test_classification('./DELETE_MAIL/', Action.DELETE_MAIL, total, correct)
print(f"Results after DELETE_MAIL Total: {total}, Correct {correct}")
print("Running READ_MAIL Test")
total, correct = test_classification('./READ_MAIL/', Action.READ_MAIL, total, correct)
print(f"Results after READ_MAIL Total: {total}, Correct {correct}")
print("Running USER_ACTION_NEEDED Test")
total, correct = test_classification('./USER_ACTION_NEEDED/', Action.USER_ACTION_NEEDED, total, correct)
print(f"Results after USER_ACTION_NEEDED Total: {total}, Correct {correct}")
overall_accuracy = (correct / total * 100)
print(f"Overall classification accuracy: {overall_accuracy:.2f}%")
