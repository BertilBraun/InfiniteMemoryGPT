
from util.gpt import create_embedding
from util.milvus import insert_data


def chunk_text(raw_text: str, chunk_size=1000, chunk_overlap=200) -> list[str]:
    # Split text into overlapping blocks

    blocks = []
    for i in range(0, len(raw_text), chunk_size - chunk_overlap):
        block = raw_text[i:i + chunk_size]
        blocks.append(block)
    
    return blocks

def upload_text(text: str) -> None:
    blocks = chunk_text(text)

    # Embed and insert blocks into the database
    for i, block in enumerate(blocks):
        title = f"Text Block {i+1}"
        print(f"Inserting block {i+1} with title {title}")
        block_embedding = create_embedding(block)
        insert_data(title, block, block_embedding)