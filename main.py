import json
from uuid import uuid4

import numpy as np
import openai
from pymilvus import (Collection, CollectionSchema, DataType, FieldSchema,
                      connections, utility)

SYSTEM_PROMPT = "You are a helpful AI assistant"
CONFIG_FILE = "config.json"

config = json.load(open(CONFIG_FILE, 'r'))
openai.api_key = config['openai_api_key']

# Connect to Milvus
connections.connect(
    "default", 
    uri=config['milvus_uri'], 
    user="db_admin", 
    password=config['milvus_password'], 
    secure=True
)

# Create collection
fields = [
    FieldSchema(name="pk", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=100),
    FieldSchema(name="question", dtype=DataType.VARCHAR, max_length=2024),
    FieldSchema(name="answer", dtype=DataType.VARCHAR, max_length=2024),
    FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=1536),
]

schema = CollectionSchema(fields, "Infinite memory chatbot using GPT-4 and Milvus")
collection_name = "gpt4_milvus_chatbot"

# Check if the collection exists
has = utility.has_collection(collection_name, using="default")

if not has:
    chatbot_collection = Collection(collection_name, schema, using="default", consistency_level="Strong")

    # Create index
    index = {
        "index_type": "AUTOINDEX",
        "metric_type": "L2",
        "params": {"nlist": 1536},
    }

    chatbot_collection.create_index("embeddings", index)

else:
    # If the collection exists, load it
    chatbot_collection = Collection(collection_name, using="default")

def insert_data(question, answer, embeddings):
    entities = [
        [str(uuid4())],  # Primary key
        [question],
        [answer],
        [embeddings],
    ]

    chatbot_collection.insert(entities)
    chatbot_collection.flush()

def search_top_k(question, k=5):
    response = openai.Embedding.create(
        input=question,
        model="text-embedding-ada-002"
    )
    embeddings = response['data'][0]['embedding']

    chatbot_collection.load()
    search_params = {
        "metric_type": "L2",
        "params": {"nprobe": 10},
    }

    results = chatbot_collection.search(
        [embeddings],
        "embeddings",
        search_params,
        limit=k,
        output_fields=["question", "answer"]
    )

    return results[0]

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
       
