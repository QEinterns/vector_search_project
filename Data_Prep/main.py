from get_files import get_files
from get_content import get_data
from dependencies import *
from m2s_converter import multiline_to_single_conv
from chunker import chunk_text
from embed import embed
from index import create_index

#connect2couchbase
username = "Administrator"
password = "password"
bucket_name = "b1"
scope_name = "s1"
collection_name = "c1"
    
auth = PasswordAuthenticator(
    username,
    password,
)

cluster = Cluster('couchbase://172.23.108.107', ClusterOptions(auth))
cluster.wait_until_ready(timedelta(seconds=5))
cb = cluster.bucket(bucket_name)
cb_coll = cb.scope(scope_name).collection(collection_name)
db_coll = cb.scope(scope_name).collection("c2")


dir = get_files()
for file in dir:
    with open(file, 'r') as f:
        html_content = f.read()

    title, text = get_data(html_content)

    #m2s conversion
    data = multiline_to_single_conv(text)

    #chunking
    chunked_text = chunk_text(data, ' '.join(title.split("_")))

    print(title)

    #embedding the chunks and storing in Couchbase Vector DB
    if chunked_text:
        # print("yes")
        ok = embed(chunked_text, title, db_coll)


#vector index creation
index_name = "docs2"
ok = create_index(index_name)   

