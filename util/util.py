from util.gpt import create_embedding
from util.milvus import insert_data


def prompt_add_to_db(question: str, answer: str) -> None:
    add_to_db = input("Should this message be added to the database? (yes/no): ")
    if add_to_db.lower() in ["yes", "y"]:
        question_embedding = create_embedding(question)
        insert_data(question, answer, question_embedding)
    

def fetch_input(prompt: str) -> str:
    start = input(prompt)
    while "SUBMIT" not in start:
        start += input()
    return start.replace("SUBMIT", "").strip()
