import sys

from pypdf import PdfReader
from unidecode import unidecode

from gpt import create_embedding
from milvus import insert_data
from util import chunk_text

if len(sys.argv) < 2:
    print("Usage: python upload_pdf.py <pdf_filename>")
    sys.exit(1)

pdf_filename = sys.argv[1]

def extract_text_from_pdf(pdf_filename: str) -> str:
    # Read PDF file using PyPDF2
    reader = PdfReader(pdf_filename)
    raw_text = "\n\n".join([page.extract_text() for page in reader.pages])

    # Purge/asciify the raw_text
    return unidecode(raw_text)

blocks = chunk_text(extract_text_from_pdf(pdf_filename))

# Embed and insert blocks into the database
for i, block in enumerate(blocks):
    title = f"{pdf_filename} Block {i+1}"
    print(f"Inserting block {i+1} with title {title}")
    block_embedding = create_embedding(block)
    insert_data(title, block, block_embedding)
