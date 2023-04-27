
def chunk_text(raw_text: str, chunk_size=1000, chunk_overlap=200) -> list[str]:
    # Split text into overlapping blocks

    blocks = []
    for i in range(0, len(raw_text), chunk_size - chunk_overlap):
        block = raw_text[i:i + chunk_size]
        blocks.append(block)
    
    return blocks
