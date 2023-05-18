from util.database import search_top_k
from util.gpt import chat_completion_system_prompt
from util.settings import config
from util.types import Message, Role
from util.util import fetch_input, prompt_add_to_db

user_question = fetch_input("User: ")

messages = search_top_k(user_question, 15)
messages.append(Message(role=Role.USER, content=user_question))

while True:
    gpt_response = chat_completion_system_prompt(messages, config['system_prompt'])
    
    prompt_add_to_db(user_question, gpt_response)
    
    messages.append(Message(role=Role.ASSISTANT, content=gpt_response))
    messages.append(Message(role=Role.USER, content=fetch_input("User: ")))
    
