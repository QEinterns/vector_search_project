from sentence_transformers import SentenceTransformer
import numpy as np
import logging

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
def user_query(sentence):
    # print("Enter the query: ")
    # sentence = input()
    # print('\n')
    
    emb = model.encode(sentence)
    embedding = np.array(emb)
    np.set_printoptions(suppress=True)

    # print(embedding.tolist())

    search_vector = embedding.tolist()
    return sentence , search_vector