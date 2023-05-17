from util.database import search_top_k
from util.gpt import (chat_completion, count_tokens_in_messages,
                      remove_messages_until_token_count_available)
from util.settings import config
from util.types import Message, Role
from util.util import fetch_input, prompt_add_to_db

PROMPT = """
I want you to become my prompt engineer. Your goal is to help me craft the best possible prompt for my needs. This prompt will be used by you, ChatGPT. You will follow the following processes.

1. Your first response will ask me what the prompt should be about. I will provide my answer, but we will need to improve it through continual iterations by going through the next steps.

2. Based on my input, you will generate 2 sections. a) Revised prompt (provide your rewritten prompt. it should be clear, concise, and easily understood by you), b) Questions (ask any relevant questions pertaining to what additional information is needed from me to improve the prompt).

3. We will continue this iterative process with me providing additional information to you and you updating the prompt in the Revised prompt section until I say we are done.
"""

RESPONSE = """
I'm here to help you craft an effective prompt!

So, let's start with the first step. What should the prompt be about?
"""

user_question = fetch_input(RESPONSE + "User: ")

starter_messages = [
    Message(role=Role.SYSTEM, content=config['system_prompt']),
]

starter_tokens = count_tokens_in_messages(starter_messages)

info_messages = [
    Message(role=Role.USER, content=PROMPT),
    Message(role=Role.ASSISTANT, content=RESPONSE),
    Message(role=Role.USER, content=user_question)
]

while True:
    # purge messages if they get too long
    info_messages = remove_messages_until_token_count_available(info_messages, config['max_tokens'] + starter_tokens)

    gpt_response = chat_completion(starter_messages + info_messages)
    info_messages.append(Message(role=Role.ASSISTANT, content=gpt_response))    
    info_messages.append(Message(role=Role.USER, content=fetch_input("User: ")))
    
