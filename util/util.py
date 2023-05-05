import sys
from util.gpt import create_embedding
from util.milvus import insert_data


def prompt_add_to_db(question: str, answer: str) -> None:
    try:
        add_to_db = input("Should this message be added to the database? (yes/no): ")
    except KeyboardInterrupt:
        sys.exit(0)
    if add_to_db.lower() in ["yes", "y"]:
        print("Adding to database...")
        question_embedding = create_embedding(question)
        insert_data(question, answer, question_embedding)
    

def fetch_input(prompt: str) -> str:
    try:
        start = input("(SUMBIT to commit) " + prompt) + "\n"
        while "SUBMIT" not in start:
            start += input() + "\n"
        return start.replace("SUBMIT", "").strip()
    except KeyboardInterrupt:
        sys.exit(0)
