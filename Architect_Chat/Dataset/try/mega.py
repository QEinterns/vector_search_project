import os
from PyPDF2 import PdfReader
from m2s_converter_d import multiline_to_single_conv
import json
import nltk
import requests
import sys
from pathlib import Path

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ''
    # print(page.extract_text())
    for page in reader.pages:
        text += multiline_to_single_conv(page.extract_text())
    return text

def load_domain_knowledge(domain_file):
    with open(domain_file, 'r') as file:
        domain_knowledge = file.read().strip()
    return domain_knowledge

def generate_instructions(domain_knowledge, context):
    instructions = []

    # Tokenize domain knowledge into sentences
    sentences = nltk.sent_tokenize(domain_knowledge)

    # Generate logical questions based on sentences
    for sentence in sentences:
        # Tokenize each sentence into words
        words = nltk.word_tokenize(sentence)
        # Tag parts of speech for each word
        tagged_words = nltk.pos_tag(words)
        # Filter out proper nouns (NNP) and gerunds (VBG)
        proper_nouns = [word for word, tag in tagged_words if tag == 'NNP']
        gerunds = [word for word, tag in tagged_words if tag == 'VBG']
        # If there are proper nouns or gerunds in the sentence, generate questions
        if proper_nouns or gerunds:
            question = f"What is the significance of {' and '.join(proper_nouns + gerunds)} in the context of {context}?"
            instructions.append(question)

    return instructions

def save_instructions(instructions, filename):
    with open(filename, 'w') as file:
        json.dump(instructions, file, indent=4)

def query_ollama(prompt, domain, context='', model='llama2'):
    url = 'http://localhost:11434/api/generate'
    data = {"model": model, "stream": False, "prompt": f"[DOMAIN] {domain} [/DOMAIN] [CONTEXT] {context} [/CONTEXT] {prompt}"}
    response = requests.post(url, json=data)
    response.raise_for_status()
    followup_data = {"model": model, "stream": False, "prompt": response.json()['response'].strip() + "What is a likely follow-up question or request? Return just the text of one question or request."}
    followup_response = requests.post(url, json=followup_data)
    followup_response.raise_for_status()
    return response.json()['response'].strip(), followup_response.json()['response'].replace("\"", "").strip()

def create_validation_file(temp_file, train_file, valid_file, test_file):
    with open(temp_file, 'r') as file:
        lines = file.readlines()
    train_lines = lines[:int(len(lines) * 0.8)]
    test_lines = lines[int(len(lines) * 0.8):int(len(lines) * 0.9)]
    valid_lines = lines[int(len(lines) * 0.9):]
    with open(train_file, 'a') as file:
        file.writelines(train_lines)
    with open(valid_file, 'a') as file:
        file.writelines(valid_lines)
    with open(test_file, 'a') as file:
        file.writelines(test_lines)

def main(context, train_file, valid_file, test_file, temp_file):
    directory = "/Users/spatra/Desktop/Movie/Internal_docs/magma"
    output_file = "/Users/spatra/Desktop/Movie/Architect_Chat/Dataset/try/chunks/magma.txt"

    with open(output_file, 'w', encoding='utf-8') as output:
        for filename in os.listdir(directory):
            if filename.endswith('.pdf'):
                print(filename)
                pdf_path = os.path.join(directory, filename)
                text = extract_text_from_pdf(pdf_path)
                output.write(text)  # Add a couple of newlines between texts for clarity

                print("Text extracted from PDF", filename, "and written to", output_file)

                # Specify the directory path
                dir = "/Users/spatra/Desktop/Movie/Architect_Chat/Dataset/try/"

                # Load domain knowledge from file
                domain_knowledge = load_domain_knowledge(output_file)

                # Generate instructions
                instructions = generate_instructions(domain_knowledge, context)

                # Save instructions to JSON file
                save_instructions(instructions, dir + "instructions.json")
                instructions_file = dir + "instructions.json"
                with open(instructions_file, 'r') as file:
                    instructions = json.load(file)
                for i, instruction in enumerate(instructions, start=1):
                    print(f"Processing ({i}/{len(instructions)}): {instruction}")
                    answer, followup_question = query_ollama(instruction, domain_knowledge, context)
                    result = json.dumps({
                        'text': f'<s>[INST] {instruction}[/INST] {answer}</s>[INST]{followup_question}[/INST]'
                    }) + "\n"
                    with open(temp_file, 'a') as file:
                        file.write(result)
                create_validation_file(temp_file, train_file, valid_file, test_file)
                print("Done! Training, testing and validation JSONL files created.")
                print()
                os.remove(instructions_file)
                os.remove(temp_file)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.exit("Usage: python script.py <context> <train.jsonl> <valid.jsonl> <test_file>")
    nltk.download('punkt')  # Download the punkt tokenizer
    nltk.download('averaged_perceptron_tagger')  # Download the POS tagger model
    path = "/Users/spatra/Desktop/Movie/Architect_Chat/Dataset/try/"
    # main(context, train_file, valid_file, test_file)
    main(sys.argv[1], path + sys.argv[2], path + sys.argv[3], path + sys.argv[4], path + "temp.jsonl")