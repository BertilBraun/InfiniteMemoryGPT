from util.gpt import chat_completion
from util.milvus import search_top_k
from util.settings import config
from util.util import prompt_add_to_db

while True:
    user_question = input("User: ")
    top_k_results = search_top_k(user_question)
    messages = [
        {"role": "system", "content": config['system_prompt']},
    ]

    for result in top_k_results:
        messages.append({"role": "user", "content": result.entity.question})
        messages.append({"role": "assistant", "content": result.entity.answer})

    messages.append({"role": "user", "content": user_question})
    gpt_response = chat_completion(messages)
    print("GPT-4:", gpt_response)

    prompt_add_to_db(user_question, gpt_response)
    