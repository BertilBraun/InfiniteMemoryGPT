from util.gpt import chat_completion, count_tokens_in_messages, MAX_TOKENS, remove_messages_until_token_count_available
from util.milvus import search_top_k
from util.settings import config
from util.util import fetch_input, prompt_add_to_db

user_question = fetch_input("User: ")

top_k_results = search_top_k(user_question, 15)
starter_messages = [
    {"role": "system", "content": config['system_prompt']},
]

starter_tokens = count_tokens_in_messages(starter_messages)

info_messages = []
for result in reversed(top_k_results):
    info_messages.append({"role": "user", "content": result.entity.question})
    info_messages.append({"role": "assistant", "content": result.entity.answer})

info_messages.append({"role": "user", "content": user_question})

while True:
    # purge messages if they get too long
    info_messages = remove_messages_until_token_count_available(info_messages, config['max_tokens'] + starter_tokens)

    gpt_response = chat_completion(starter_messages + info_messages)
    info_messages.append({"role": "assistant", "content": gpt_response})
    print("GPT-4:", gpt_response)
    
    prompt_add_to_db(user_question, gpt_response)
    
    info_messages.append({"role": "user", "content": fetch_input("User: ")})
    
