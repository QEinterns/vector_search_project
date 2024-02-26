from dependencies import *

def chunk_text(text, Chunk_size = 1000, Overlap = 50, Length_function = len, debug_mode = 0):

    chunks  = RecursiveCharacterTextSplitter(
        chunk_size = Chunk_size,
        chunk_overlap = Overlap,
        length_function = Length_function
    ).create_documents([text])

    if(debug_mode):
        k=0
        for i in chunks:
            print("Chunk {k+1} : i\n")
            k+=1
        
        print('\n')
    
    return chunks
