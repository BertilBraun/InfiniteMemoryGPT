import openai

from milvus import insert_data, search_top_k
from settings import config

SYSTEM_PROMPT = config['system_prompt']
openai.api_key = config['openai_api_key']

def chat_completion(messages):
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.5,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return completion["choices"][0]["message"]["content"]

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
        response = openai.Embedding.create(
            input=user_question,
            model="text-embedding-ada-002"
        )
        question_embeddings = response['data'][0]['embedding']
        insert_data(user_question, gpt_response, question_embeddings)
       
