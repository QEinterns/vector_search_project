import os
import markdown

def extract_text_from_md(md_file):
    with open(md_file, 'r', encoding='utf-8') as file:
        text = file.read()
    html = markdown.markdown(text)
    return html

def main():
    directory = '/Users/spatra/Desktop/Movie/Internal_docs/kv_engine'
    output_file = '/Users/spatra/Desktop/Movie/Architect_Chat/Dataset/raw/temp.txt'

    with open(output_file, 'w', encoding='utf-8') as output:
        for filename in os.listdir(directory):
            if filename.endswith('.md'):
                print(filename)
                md_path = os.path.join(directory, filename)
                text = extract_text_from_md(md_path)
                output.write(text + '\n\n')  # Add a couple of newlines between texts for clarity

    print("Text extracted from Markdown files and written to", output_file)

if __name__ == "__main__":
    main()
