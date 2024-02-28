from dependencies import *

def chunk_text(text, title, Chunk_size = 2000, Overlap = 50, Length_function = len, debug_mode = 0):
    global global_unique_hashes
    
    # print(title)
    chunks  = RecursiveCharacterTextSplitter(
        chunk_size = Chunk_size,
        chunk_overlap = Overlap,
        length_function = Length_function
    ).create_documents([text])

    if debug_mode:
        for idx, chunk in enumerate(chunks):
            print(f"Chunk {idx+1}: {chunk}\n")
        
        print('\n')

    for sentence in chunks:
        sentence.page_content = title + " " + sentence.page_content

    # print(chunks)
    return chunks
