
from util.gpt import create_embedding
from util.database import insert_data
from unidecode import unidecode


def chunk_text(raw_text: str, chunk_size=1000, chunk_overlap=200) -> list[str]:
    # Split text into overlapping blocks

    blocks = []
    for i in range(0, len(raw_text), chunk_size - chunk_overlap):
        block = raw_text[i:i + chunk_size]
        blocks.append(block)
    
    return blocks

def replace_newlines(text: str) -> str:
    while "\n\n" in text:
        text = text.replace("\n\n", "\n")
    return text

def cleanup_text(text: str) -> str:
    # Purge/asciify the raw_text
    text = unidecode(text)
    text = replace_newlines(text)
    # TODO: Add more cleanup steps
    return text

def upload_text(text: str, origin: str) -> None:
    text = cleanup_text(text)
    blocks = chunk_text(text)

    # Embed and insert blocks into the database
    for i, block in enumerate(blocks):
        title = f"Data Source: '{origin}' Block {i+1}"
        print(f"Inserting block {i+1} with title {title}")
        block_embedding = create_embedding(block)
        insert_data(title, block, block_embedding)