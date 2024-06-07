# Email Assistant

Author: Gsteiger Dominik (gsteidom@students.zhaw.ch)<br>
Module: Machine Learning 2<br>
Semester: FS24<br>

## Table of Contents

1. Setup
2. Project Goal / Motivation
3. Data Collection or Generation
4. Modeling
5. Interpretation and Validation
6. Future work & expansions

## 1. Setup

1. Clone Git Repository
2. Setup local python environment (venv) with python version 3.10.0
3. Install requirements <br/>
   ``` pip install -r requirements.txt```
4. Create .env file with the following variable <br/>
   Email Assistant uses GPT-3.5-Turbo. Use your own OPENAI_API_KEY or request a OPENAI_API_KEY per mail. <br/>
   ```OPENAI_API_KEY='REPLACEME'```
5. Run app with ```python app.py``` or with ```flask run```
6. Go to url printed in console or  http://127.0.0.1:5000 and have fun :)
7. Testdata: Use your own Emails to test the assistant or generate Email with the ```test/create_emails.py```

## 2. Project Goal / Motivation

Reading and deciding what to do with emails consumes a significant amount of our time daily.
The volume of spam emails is continuously increasing, requiring users to identify and manage them.
There are also numerous emails that simply require scheduling an appointment in Outlook and nothing more.

Additionally, the sheer volume of emails can be overwhelming, leading to important messages being overlooked or delayed
in response.
Users often struggle to prioritize emails based on urgency and importance, causing inefficiencies in communication and
task management.
Furthermore, manually sorting, categorizing, and responding to emails can lead to errors and inconsistencies.

An AI that first classifies emails and then takes appropriate action could be very helpful,
especially if it operates fully autonomously within the inbox.
However, achieving full autonomy for the AI is still a long way off.

As a first step and proof of concept, a chat interface should be developed where an email can be uploaded.
This email should then be classified, and the user should provide consent that the action chosen by the AI is correct.
Subsequently, the email should be further processed with follow-up questions to the user.

### 2.1 Scope and context

This project serves as a proof of concept for an AI-based email assistant.
The goal is to evaluate the feasibility of using a large language model (LLM) like GPT-3.5 Turbo to build such an
assistant. <br/>
During the concept phase, the project scope was defined as follows:

- <b>Classifier Implementation and Testing:</b> <br>A classifier will be developed and automatically tested with test
  data, aiming for an accuracy of over 75%.
- <b>Action Agents Implementation and Testing:</b> <br>The following action agents will be implemented and manually
  tested.
    - <b>Create Meeting Agent:</b><br> This agent will extract meeting details and offer them as a downloadable file.
    - <b>Answer Mail Agent:</b><br> This agent will generate an initial response to emails and adapt based on user
      feedback.
    - <b>User Action Agent:</b><br> This agent will advise the user on necessary actions.
    - <b>Read Mail Agent:</b><br> This agent will extract relevant information from emails and present it to the user.
    - <b>Delete Mail Agent:</b><br> This agent will inform the user that the email has been deleted without taking
      direct action.
- The User should always have the option to interfeer.
  ![Concept](img/concept.png)

## 3. Data Collection or Generation

In the use case of the email assistant, there are essentially two types of input data.
First, there is the .msg file, which serves as the initial input to start the process.
This file is then classified by the classifier.
Second, there are various ways the user can interact with the assistant.

1. <b>.msg Files/Emails for the Classifier:</b><br>
   To test the classifier, emails are needed.
   On one hand, personal or private emails can be used.
   On the other hand, dummy emails are generated in the test folder to ensure there is enough test data to fairly assess
   the accuracy. ```Generation in test/create_emails.py``` On default this python file creates 25 .msg files. But it can
   easily be
   scaled to a bigger amount. For this proof of concept 25 emails should be enough.
2. <b>User Interaction:</b><br>
   User interaction is tested manually, and therefore, no data is generated or collected.

## 4. Modeling

This chapter is all about how the projects modeling / code / prompt engineering works. Its divided into this 3
subchapters:
Agent concept, Conversation handler & State machine and varia

### 4.1 Agent concept

Working with the full prompt in a python file was quite unsatisfying. Therefore, I created the "agent"-concept i will
describe in this chapter.
<br>
Every agent consists out of 3 files. A system_prompt.txt file
(containing the system prompt), a wrapper_prompt.txt file
(containing the wrapper_prompt) and a python file.
The system prompt is the prompt which defines the task and the behaviour of the model. The wrapper prompt is where the
user input gets inserted.
While engineering this solution, i firstly had some issues that the model not always would give me the answer as a json,
when only mentioned in the
system prompt. When I added the json a second time at the end of the prompt (Ref: wrapper_prompts), i never had this
issue again. Variables marked with { } (Example {feedback}) are used to insert conversation data into the prompt.
<br>
So to conclude the "agent"-concept has the following advantages:

- Structure: it gives a nice structure to the code, as you have a package with 3 files for every agent.
- Prompt management: the prompts can easily be managed in txt files.

### 4.2 Conversation handler & State machine

The conversation handler is the heart of the application. It's the interface between the api-handler (app.py) and all
the agents.
It decides at which time which agent is needed.
To handle the state of the conversation a small but effective state machine was implemented.
![State Machine](img/state_machine.png)

#### Further Development:

Right now the conversation handler is only able to handle one conversation.
Enabling a multi-user / multi-conversation management would be a next big step.

## 5. Validation and Interpretation

To ensure a fair validation each component / agent is getting tested/validated separately in this chapter.
The validation focuses on the classifier agent because it's the main focus of this project. The validation
of the other agents depends mostly on the opinion of the author.

### 5.1 Classifier-Agent

The primary testing of the classifier-agent ist automated in ```/test/classifier_test.py```.
Of 25 emails 22 get classified correctly, so we got an accuracy of 88%. For further usage this should be tested with
much more testdata.
But it's already a quite a good result this also resembles in the manual tests.
<br>
Manual Testcases:

1. eBill Rechnung: Es ist eine neue Rechnung verfügbar.
2. Einladung zur GV vom Handball
3. Ergotherapie: Anfrage ob ein Termin auch 3 Stunden früher gehen würde.
4. Booking Answer: Antwort auf eine Frage die ich gestellt habe.
5. Google Sicherheitswarnung: Auf einem Geräte wurde sich eingeloggt.
6. Digitec: Bewerte unseren Service

| Testcase |      Expected      |       Actual       |
|:--------:|:------------------:|:------------------:|
|    1     | USER_ACTION_NEEDED | USER_ACTION_NEEDED |
|    2     |   CREATE_MEETING   |   CREATE_MEETING   |
|    3     |    ANSWER_MAIL     |    ANSWER_MAIL     |
|    4     |     READ_MAIL      |    ANSWER_MAIL     |
|    5     | USER_ACTION_NEEDED |     READ_MAIL      |
|    6     |    DELETE_MAIL     |   ERROR Code 400   |

The manual test results seem quite bad, but sometimes, especially in complex email histories,
its even hard for me to decide what the right action would be for this case (Testcase 4,5,6).
I got two possible solution for this problem in mind:

1. Reduce the number of actions (classes), so it gets easier to decide which is the right one.
2. Implement a user based feedback loop, where every user can individualize the actions taken:<br>
   For me the testcase 6 Digitec Feedback would classify as spam (DELETE_MAIL). Other users maybe want it to classify as
   UserActionNeeded

### 5.2 Answer-Agent

The idea of the answer agent was to interpret the mail received and generate an accurate answer to it.
If there are some open / unclear points that the model cant decide, the model should ask the user to clarify this open
points.

#### Example

- Input Mail: <br>
  Hallo Hans<br>
  Ich wollte dich nur kurz fragen, ob es morgen für dich auch um 14:00 passen würde?<br>
  Liebe Grüsse Max
- Expected Model Output should be something like: <br>
  Hallo Max<br>
  Ja 14:00 passt für mich auch!<br>
  Liebe Grüsse Hans<br>
  Open Questions: Passt ihnen der Termin um 14:00 ?
- Actual Model Output:
  Lieber Hans, vielen Dank für deine E-Mail. Ja, morgen um 14:00 Uhr passt mir für die Therapie. Danke für die
  Erinnerung. Liebe Grüße, Hans<br>
  <br>
  In general it works really well. But sometimes these problems occur:
- Mixing up forms of politeness (Even after giving feedback)
- Mixing up which email should be answered (Especially if there is an email history as an input)
- Identifying open questions (The model is not good at identifying open questions/points)

### 5.3 Delete-Agent

Is not implemented so it will not be tested.

### 5.4 Meeting-Agent

The extraction of an meeting / appointment out of a email overall works really well.
But the model starts to struggle if the date is given relative (not absolute, example next friday).
I tried to fix this by giving the date of today as an input. It got better but is still not optimal.
It also struggles to handle incomplete data.

### 5.5 Reader-Agent

Extracting the relevant information out of an email works really well.

### 5.6 UserAction-Agent

Extracting the relevant action out of an email works quite well.

### 5.7 Conclusion

To sum it up the project was an success. The author is really happy with the results especially with the
classifier-agent.
But also the other agents (Part of proof of concept) work quite good. To improve better results with the prompt
engineering
in the other agents it would need a huge amount of time (That i didn't have anymore). Overall its a solid proof of
concept that would enable further improvements easily.

## 6. Possible future work & expansions

- Integration in Outlook or other email clients
- Improve performance of agents by improving prompt engineering and overthinking actions (classes)
- Improve feedback loops from users
- Implement multi-user/multi-conversation ability
- Enable agents to execute actions (Example: Delete Mail, Answer mail)