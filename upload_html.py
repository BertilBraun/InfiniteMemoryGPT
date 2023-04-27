import sys

import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

from util.upload import upload_text

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

upload_text(replace_triple_newlines(extract_text_from_html(url)))
