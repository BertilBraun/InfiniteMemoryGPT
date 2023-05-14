from util.gpt import chat_completion, count_tokens_in_messages, remove_messages_until_token_count_available
from util.database import search_top_k
from util.settings import config
from util.types import Message, Role
from util.util import fetch_input, prompt_add_to_db

while True:
    user_question = fetch_input("User: ")
    top_k_results = search_top_k(user_question, 15)
    starter_messages = [
        Message(role=Role.SYSTEM, content=config['system_prompt']),
    ]

    info_messages = top_k_results
    info_messages.append(Message(role=Role.USER, content=user_question))

    info_messages = remove_messages_until_token_count_available(info_messages, config['max_tokens'] + count_tokens_in_messages(starter_messages))

    gpt_response = chat_completion(starter_messages + info_messages)
    print("GPT-4:", gpt_response)

    prompt_add_to_db(user_question, gpt_response)
    