from util.gpt import MAX_TOKENS, chat_completion, count_tokens_in_messages
from util.milvus import search_top_k
from util.settings import config
from util.util import fetch_input, prompt_add_to_db

while True:
    user_question = fetch_input("User: ")
    top_k_results = search_top_k(user_question, 15)
    starter_messages = [
        {"role": "system", "content": config['system_prompt']},
    ]

    info_messages = []
    for result in reversed(top_k_results):
        info_messages.append({"role": "user", "content": result.entity.question})
        info_messages.append({"role": "assistant", "content": result.entity.answer})
        
    info_messages.append({"role": "user", "content": user_question})

    while count_tokens_in_messages(info_messages) + count_tokens_in_messages(starter_messages) > MAX_TOKENS - config['max_tokens']:
        info_messages.pop(0)

    gpt_response = chat_completion(starter_messages + info_messages)
    print("GPT-4:", gpt_response)

    prompt_add_to_db(user_question, gpt_response)
    