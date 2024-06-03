# Email Assistant
Author: Gsteiger Dominik (gsteidom@students.zhaw.ch)
Module: Machine Learning 2
Semester: FS24
## Table of Contents
1. Setup
2. Project Goal / Motivation 
3. Data Collection or Generation
4. Modeling
5. Interpretation and Validation

## 1. Setup
1. Clone Git Repository 
2. Setup local python environment (venv) with python version 3.10.0
3. Install requirements <br/>
``` pip install -r requirements.txt```
4. Create .env file with the following variable <br/>
Email Assistant uses GPT-3.5-Turbo. Use your own KEY or request a key per mail. <br/>
```OPENAI_API_KEY='REPLACEME'```
5. Run app with ```python app.py```
6. Go to url printed in console or  http://127.0.0.1:5000 and have fun :)

## 2. Project Goal / Motivation
Reading and deciding what to do with emails consumes a significant amount of our time daily. 
The volume of spam emails is continuously increasing, requiring users to identify and manage them. 
There are also numerous emails that simply require scheduling an appointment in Outlook and nothing more.

Additionally, the sheer volume of emails can be overwhelming, leading to important messages being overlooked or delayed in response. 
Users often struggle to prioritize emails based on urgency and importance, causing inefficiencies in communication and task management. 
Furthermore, manually sorting, categorizing, and responding to emails can lead to errors and inconsistencies.

An AI that first classifies emails and then takes appropriate action could be very helpful,
especially if it operates fully autonomously within the inbox. 
However, achieving full autonomy for the AI is still a long way off.

As a first step and proof of concept, a chat interface should be developed where an email can be uploaded. 
This email should then be classified, and the user should provide consent that the action chosen by the AI is correct. 
Subsequently, the email should be further processed with follow-up questions to the user.

