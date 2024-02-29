import os
from PyPDF2 import PdfReader
from m2s_converter import multiline_to_single_conv

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ''
    page = reader.pages[0]
    print(page.extract_text())
    text += multiline_to_single_conv(page.extract_text())
    return text

def main():
    directory = '/Users/spatra/Desktop/Movie/Architect_Chat/Data_Collection/data'
    output_file = '/Users/spatra/Desktop/Movie/Architect_Chat/Dataset/raw_data.txt'

    with open(output_file, 'w', encoding='utf-8') as output:
        for filename in os.listdir(directory):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(directory, filename)
                text = extract_text_from_pdf(pdf_path)
                output.write(text + ' ')  # Add a couple of newlines between texts for clarity

    print("Text extracted from PDFs and written to", output_file)

if __name__ == "__main__":
    main()
