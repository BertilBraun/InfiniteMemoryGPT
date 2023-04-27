import sys

from pypdf import PdfReader
from unidecode import unidecode

from util.upload import upload_text

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

upload_text(extract_text_from_pdf(pdf_filename), pdf_filename)