from util.gpt import chat_completion_system_prompt
from util.settings import config
from util.types import Message, Role
from util.util import fetch_input

mail = input("Mail: ")
name = input("Name: ")
content = fetch_input("Content: ")

PROMPT = f"""
Ich muss eine Mail an {mail} schreiben. Schreibe eine formale, höfliche aber nicht zu höfliche mail. Der Inhalt der mail ist der folgende. Nutze diesen für inhaltliche information, allerdings nicht als Formulierung.

{content}

Schreibe nun diese Mail für mich {name}.
"""

messages = [Message(role=Role.USER, content=PROMPT)]

while True:
    gpt_response = chat_completion_system_prompt(messages, config['system_prompt'])
    messages.append(Message(role=Role.ASSISTANT, content=gpt_response))
    messages.append(Message(role=Role.USER, content=fetch_input("User: ")))
    