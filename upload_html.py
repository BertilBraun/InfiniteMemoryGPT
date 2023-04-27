import sys

import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

from util.gpt import create_embedding
from util.milvus import insert_data
from util.util import chunk_text

if len(sys.argv) < 2:
    print("Usage: python upload_html.py <url>")
    sys.exit(1)

url = sys.argv[1]

def extract_text_from_html(url: str) -> str:
    # Download the HTML content
    response = requests.get(url)
    response.raise_for_status()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract text from the parsed HTML
    raw_text = soup.get_text(separator="\n")

    # Purge/asciify the raw_text
    return unidecode(raw_text)

def replace_triple_newlines(text: str) -> str:
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n")
    return text

blocks = chunk_text(replace_triple_newlines(extract_text_from_html(url)))

# Embed and insert blocks into the database
for i, block in enumerate(blocks):
    title = f"{url} Block {i+1}"
    print(f"Inserting block {i+1} with title {title}")
    block_embedding = create_embedding(block)
    insert_data(title, block, block_embedding)
