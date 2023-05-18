from util.gpt import chat_completion_system_prompt
from util.settings import config
from util.types import Message, Role
from util.util import fetch_input

mail = input("Mail: ")
name = input("Name: ")
content = fetch_input("Content: ")

PROMPT = f"""
I need to write a mail to {mail}. Write a formal, polite but not too polite mail. The content of the mail is the following. Use this for content information, but not as wording.

{content}

Now write this mail for me {name}.
"""

messages = [Message(role=Role.USER, content=PROMPT)]

while True:
    gpt_response = chat_completion_system_prompt(messages, config['system_prompt'])
    messages.append(Message(role=Role.ASSISTANT, content=gpt_response))
    messages.append(Message(role=Role.USER, content=fetch_input("User: ")))
    