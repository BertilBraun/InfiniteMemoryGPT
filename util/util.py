import os
import subprocess
import sys

from util.types import Message, Messages, Role

from .settings import config


def prompt_add_to_db(question: str, answer: str) -> None:
    from util.database import insert_data
    from util.gpt import create_embedding

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

def split_into_paragraphs(text: str) -> list[str]:
    return [p if p.startswith('#') else '##' + p for p in text.split("##")]

def run_runner(inputs: list[str], script: str) -> None:
    runner_folder = config['runner_folder']
    print("Running GPT-4 on each input...")
    os.makedirs(runner_folder, exist_ok=True)
    script = script if script.endswith(".py") else script + ".py"

    for i, input in enumerate(inputs):
        with open(f"{runner_folder}/data_{i}.txt", "w", encoding="utf-8") as f:
            f.write(input)
            
        print(f"Running {script} on input {i}...")
        cmd = f"start cmd.exe /k python {script} {i}".split(" ")
        subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print("Done!")
    
def get_runner_input(promp_continue=True) -> str:
    runner_folder = config['runner_folder']
    if len(sys.argv) < 2:
        print("Usage: python <script> <input number>")
        sys.exit(1)
        
    input_number = sys.argv[1]
    print("Input number:", input_number)
    
    if not os.path.exists(f"{runner_folder}/data_{input_number}.txt"):
        print("Input file does not exist!")
        sys.exit(1)

    with open(f"{runner_folder}/data_{input_number}.txt", "r", encoding="utf-8") as f:
        input_data = f.read()
    print("Input data:", input_data)
    
    os.remove(f"{runner_folder}/data_{input_number}.txt")
    
    if promp_continue:
        input("\n\nPress enter to start the writing process...\n\n")
    
    return input_data

def simple_chat(prompt: str) -> None:    
    starter_messages = [Message(role=Role.SYSTEM, content=config['system_prompt'])]
    messages = [Message(role=Role.USER, content=prompt)]

    chat(messages, starter_messages)
        
def query_chat(prompt: str, query: str, top_k = 15) -> None:
    from util.database import search_top_k
    
    starter_messages = [
        Message(role=Role.SYSTEM, content=config['system_prompt']),
        Message(role=Role.USER, content="The following are information that I have gathered for you:"),
    ]
    
    messages = search_top_k(query, top_k)
    messages.append(Message(role=Role.USER, content=prompt))
    
    chat(messages, starter_messages)
    
        
def chat(messages: Messages, starter_messages: Messages) -> None:
    from util.gpt import chat_completion
    
    while True:
        gpt_response = chat_completion(messages, starter_messages)
        messages.append(Message(role=Role.ASSISTANT, content=gpt_response))
        messages.append(Message(role=Role.USER, content=fetch_input("User: ")))