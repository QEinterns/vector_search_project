
import numpy as np
import logging
# from FlagEmbedding import BGEM3FlagModel
# embed_model = BGEM3FlagModel('BAAI/bge-m3',  use_fp16=True)

def user_query(model,sentence):
    emb = model.encode(sentence)
    emb = emb['dense_vecs']
    print("before: \n")
    print(emb.tolist())

    return emb.tolist()



# user_query(embed_model,"this is good")

