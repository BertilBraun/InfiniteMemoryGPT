import os
import subprocess
import sys


def prompt_add_to_db(question: str, answer: str) -> None:
    from util.gpt import create_embedding
    from util.database import insert_data

    try:
        add_to_db = input("Should this message be added to the database? (yes/no): ")
    except KeyboardInterrupt:
        sys.exit(0)
    if add_to_db.lower() in ["yes", "y"]:
        print("Adding to database...")
        question_embedding = create_embedding(question)
        insert_data(question, answer, question_embedding)
    

def fetch_input(prompt: str) -> str:
    try:
        start = input("(SUMBIT to commit) " + prompt) + "\n"
        while "SUBMIT" not in start:
            start += input() + "\n"
        return start.replace("SUBMIT", "").strip()
    except KeyboardInterrupt:
        sys.exit(0)

def markdownify(text: str) -> str:
    while "  " in text:
        text = text.replace("  ", " ")
        
    while " \n" in text:
        text = text.replace(" \n", " ")
        
    while " \r\n" in text:
        text = text.replace(" \r\n", " ")
        
    if text[-1] != "\n":
        text += "\n"
        
    return text

def run_runner(inputs: list[str], script: str) -> None:
    print("Running GPT-4 on each input...")
    os.makedirs("runner", exist_ok=True)
    script = script.strip(".py")

    processes = []
    for i, input in enumerate(inputs):
        with open(f"runner/data_{i}.txt", "w") as f:
            f.write(input)
            
        cmd = f"start cmd.exe /k python {script}.py {i}".split(" ")
        proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        processes.append(proc)
        
    print("Waiting for GPT-4 to finish...")
    for proc in processes:
        proc.wait()
    print("Done!")
    
def get_runner_input() -> str:
    if len(sys.argv) < 2:
        print("Usage: python <script> <input number>")
        sys.exit(1)
        
    input_number = sys.argv[1]
    print("Input number:", input_number)

    with open(f"runner/data_{input_number}.txt", "r") as f:
        input = f.read()
    return input