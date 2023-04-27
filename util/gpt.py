import openai

from .settings import config

openai.api_key = config['openai_api_key']


def chat_completion(messages: list[dict]) -> str:
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

def create_embedding(input: str) -> list[float]:
    response = openai.Embedding.create(
        input=input,
        model="text-embedding-ada-002"
    )
    
    return response['data'][0]['embedding']