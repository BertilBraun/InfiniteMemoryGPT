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
    return soup.get_text(separator="\n")

upload_text(extract_text_from_html(url), url)
