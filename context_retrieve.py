from PyPDF2 import PdfReader
import nltk
nltk.download('punkt')
from langchain.text_splitter import RecursiveCharacterTextSplitter
from datetime import timedelta
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import (ClusterOptions, ClusterTimeoutOptions,QueryOptions)
import ast
from sentence_transformers import SentenceTransformer
import numpy as np
import json
from json import JSONEncoder




model = SentenceTransformer('paraphrase-MiniLM-L6-v2')


username = "Administrator"
password = "nish123"
bucket_name = "bucket"

auth = PasswordAuthenticator(
    username,
    password,
)

cluster = Cluster('couchbase://172.23.108.107', ClusterOptions(auth))
cluster.wait_until_ready(timedelta(seconds=5))
cb = cluster.bucket(bucket_name)
cb_coll = cb.scope("scope").collection("collection")


def get_document(key):
    print("\nGet Result: ")
    try:
        result = cb_coll.get(key)
        # print(result.value)
        dd = dict(result.value)
        print(dd['data'])
        
        return dd['data']
    except Exception as e:
        print(e)





context_string =""

docids = [109,128,97,127,17,25]

for i in docids:
    dockey = "docid:"+str(i)
    ss = get_document(dockey)
    context_string += ss

main_context =""
for i in context_string:
    if(i!='\n'):
        main_context +=i

print(main_context)
