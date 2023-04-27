from util.gpt import create_embedding
from util.milvus import insert_data


def prompt_add_to_db(question: str, answer: str) -> None:
    add_to_db = input("Should this message be added to the database? (yes/no): ")
    if add_to_db.lower() in ["yes", "y"]:
        question_embedding = create_embedding(question)
        insert_data(question, answer, question_embedding)
    
def chunk_text(raw_text: str, chunk_size=1000, chunk_overlap=200) -> list[str]:
    # Split text into overlapping blocks

    blocks = []
    for i in range(0, len(raw_text), chunk_size - chunk_overlap):
        block = raw_text[i:i + chunk_size]
        blocks.append(block)
    
    return blocks
