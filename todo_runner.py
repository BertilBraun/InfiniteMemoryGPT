from util.util import fetch_input, run_runner


complete_section = fetch_input("Complete section: ")

print("Now splitting into paragraphs...")
paragraphs = [p if p.startswith('#') else '##'+p for p in complete_section.split("##")]
print("Found", len(paragraphs), "paragraphs.")

run_runner(paragraphs, "todo")