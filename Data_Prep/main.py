from get_files import get_files
from get_data import get_data
from dependencies import *
from m2s_converter import multiline_to_single_conv
from chunk_plot import chunk_text
from embedder import embed
from index_creator import create_index

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


dir = get_files()
for file in dir:
    with open(file, 'r') as f:
        html_content = f.read()

    title, text = get_data(html_content)

    # #m2s conversion
    data = multiline_to_single_conv(text)

    # #chunking
    chunked_text = chunk_text(data)

    #embedding the chunks and storing in Couchbase Vector DB
    ok = embed(chunked_text, title, cb_coll)


#vector index creation
index_name = "docs"
ok = create_index(index_name)   

