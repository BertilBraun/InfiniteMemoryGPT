import sys

from util.upload import upload_text

if len(sys.argv) < 2:
    print("Usage: python upload_file.py <file path>")
    sys.exit(1)

file_path = sys.argv[1]

upload_text(open(file_path, 'r', encoding='utf8').read(), file_path)
