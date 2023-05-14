import datetime
import os
import sys

import openai
import tiktoken
from util.types import Messages, messagesToMap

from .settings import config

MAX_TOKENS = 8000

openai.api_key = config['openai_api_key']
encoding = tiktoken.get_encoding("cl100k_base")


def count_tokens_in_messages(messages: Messages) -> int:
    return sum(count_tokens(message.content) for message in messages)

def count_tokens(text: str) -> int:
    return len(encoding.encode(text))

def remove_messages_until_token_count_available(messages: Messages, token_count: int) -> Messages:
    while count_tokens_in_messages(messages) > MAX_TOKENS - token_count:
        messages.pop(0)
    
    if len(messages) == 0:
        raise ValueError("No messages left after removing messages until token count available.")
    
    return messages

def chat_completion(messages: Messages) -> str:
    # write request and response to file at config['log_folder'] + '/' + (current_date in YYYY-MM-DD) + '/' + (current_time in HH-MM-SS format) + '.txt'
    folder_path = f"{config['log_folder']}/{datetime.datetime.now().strftime('%Y-%m-%d')}"
    
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    
    file_path = f"{folder_path}/{datetime.datetime.now().strftime('%H-%M-%S')}.txt"
    
    with open(file_path, "w", encoding="utf8") as f:
        f.write("Request:\n")
        for message in messages:
            f.write(message.role.value + ": " + message.content + "\n\n")
        
    print("Fetching response... (" + str(count_tokens_in_messages(messages)) + " tokens in messages)")
    for _ in range(3):
        try:
            text = ""
            for res in openai.ChatCompletion.create(
                model="gpt-4",
                messages=messagesToMap(messages),
                temperature=config['temperature'],
                max_tokens=config['max_tokens'],
                top_p=config['top_p'],
                frequency_penalty=config['frequency_penalty'],
                presence_penalty=config['presence_penalty'],
                stream=True
            ):
                sys.stdout.write(res["choices"][0]["delta"].get("content", ""))
                sys.stdout.flush()
                text += str(res["choices"][0]["delta"].get("content", ""))
            break
        except openai.error.RateLimitError:
            print("Rate limit exceeded, retrying...")
    else:
        raise openai.error.RateLimitError("Rate limit exceeded, please try again later.")            
            
    with open(file_path, "a", encoding="utf8") as f:
        f.write("\n\nResponse:\n")
        f.write(text) 

    return text

def create_embedding(input: str) -> list[float]:
    response = openai.Embedding.create(
        input=input,
        model="text-embedding-ada-002"
    )
    
    return response['data'][0]['embedding']