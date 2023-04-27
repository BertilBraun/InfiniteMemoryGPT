import datetime

import openai

from .settings import config

openai.api_key = config['openai_api_key']


def chat_completion(messages: list[dict]) -> str:
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=config['temperature'],
        max_tokens=config['max_tokens'],
        top_p=config['top_p'],
        frequency_penalty=config['frequency_penalty'],
        presence_penalty=config['presence_penalty']
    )
    
    # write request and response to file at config['log_folder'] + '/' + (current_time in HH-MM-SS format) + '.txt'
    file_path = f"{config['log_folder']}/{datetime.datetime.now().strftime('%H-%M-%S')}.txt"
    with open(file_path, "w", encoding="utf8") as f:
        f.write("Request:\n")
        f.write(str(messages))
        f.write("\n\nResponse:\n")
        f.write(str(completion["choices"][0]["message"]["content"])) 

    return completion["choices"][0]["message"]["content"]

def create_embedding(input: str) -> list[float]:
    response = openai.Embedding.create(
        input=input,
        model="text-embedding-ada-002"
    )
    
    return response['data'][0]['embedding']