from util.gpt import chat_completion, create_embedding
from util.milvus import insert_data, search_top_k
from util.settings import config

SYSTEM_PROMPT = config['system_prompt']

while True:
    user_question = input("User: ")
    top_k_results = search_top_k(user_question)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]

    for result in top_k_results:
        messages.append({"role": "user", "content": result.entity.question})
        messages.append({"role": "assistant", "content": result.entity.answer})

    messages.append({"role": "user", "content": user_question})
    print("Calling GPT-4 with the following messages: ", messages)
    gpt_response = chat_completion(messages)
    print("GPT-4:", gpt_response)

    add_to_db = input("Should this message be added to the database? (yes/no): ")
    if add_to_db.lower() in ["yes", "y"]:
        question_embedding = create_embedding(user_question)
        insert_data(user_question, gpt_response, question_embedding)
       
