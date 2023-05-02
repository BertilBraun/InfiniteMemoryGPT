import datetime
import os

import openai
import tiktoken

from .settings import config

MAX_TOKENS = 8000

openai.api_key = config['openai_api_key']
encoding = tiktoken.get_encoding("cl100k_base")


def count_tokens_in_messages(messages: list[dict]) -> int:
    return sum(count_tokens(message['content']) for message in messages)

def count_tokens(text: str) -> int:
    return len(encoding.encode(text))

def chat_completion(messages: list[dict]) -> str:
    # write request and response to file at config['log_folder'] + '/' + (current_date in YYYY-MM-DD) + '/' + (current_time in HH-MM-SS format) + '.txt'
    folder_path = f"{config['log_folder']}/{datetime.datetime.now().strftime('%Y-%m-%d')}"
    
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    
    file_path = f"{folder_path}/{datetime.datetime.now().strftime('%H-%M-%S')}.txt"
    
    with open(file_path, "w", encoding="utf8") as f:
        f.write("Request:\n")
        for message in messages:
            f.write(message['role'] + ": " + message['content'] + "\n\n")
        
    print("Fetching response...")
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=config['temperature'],
        max_tokens=config['max_tokens'],
        top_p=config['top_p'],
        frequency_penalty=config['frequency_penalty'],
        presence_penalty=config['presence_penalty']
    )
    
    with open(file_path, "a", encoding="utf8") as f:
        f.write("\n\nResponse:\n")
        f.write(str(completion["choices"][0]["message"]["content"])) 

    return completion["choices"][0]["message"]["content"]

def create_embedding(input: str) -> list[float]:
    response = openai.Embedding.create(
        input=input,
        model="text-embedding-ada-002"
    )
    
    return response['data'][0]['embedding']