from dependencies import *
import hashlib

# Global set to store unique chunk hash values across all files
global_unique_hashes = set()

def hash_text(text):
    # Generate a hash value for the text using SHA-256
    hash_object = hashlib.sha256(text.encode())
    return hash_object.hexdigest()

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
    
    # Deduplication mechanism
    unique_chunks = []
    for chunk in chunks:
        chunk_hash = hash_text(chunk.page_content)
        if chunk_hash not in global_unique_hashes:
            unique_chunks.append(chunk)
            global_unique_hashes.add(chunk_hash)

    for sentence in unique_chunks:
        sentence.page_content = title + " " + sentence.page_content

    print(unique_chunks)
    return unique_chunks
