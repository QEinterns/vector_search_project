from app_python_srcs.dependencies import *
from app_python_srcs.m2s_converter import multiline_to_single_conv
from app_python_srcs.movie_srcs.chunk_plot import chunk_text
from app_python_srcs.movie_srcs.embedder import embed
from app_python_srcs.movie_srcs.index_creator import create_index
from app_python_srcs.user_query import user_query
from app_python_srcs.movie_srcs.vector_search import vector_search
from app_python_srcs.movie_srcs.query_enhancer import query_enhancer
from app_python_srcs.movie_srcs.t2i_SD1 import t2i_SD1
from app_python_srcs.movie_srcs.query_enhancer_orca import query_enhancer_orca
from app_python_srcs.movie_srcs.query_enhancer_mistral import query_enhancer_mistral
from app_python_srcs.movie_srcs.opendalle import opendalle
from app_python_srcs.movie_srcs.openjourney import openjourney
from app_python_srcs.movie_srcs.playground import playground
from app_python_srcs.movie_srcs.proteus import proteus
import logging
import time
from app_python_srcs.movie_srcs.get_data import get_data
from app_python_srcs.movie_srcs.stable_diff_x1 import sdx
import multiprocessing
import threading
from app_python_srcs.movie_srcs.threading_t2i import threadit
from FlagEmbedding import BGEM3FlagModel




def driver_function(movie_name,query,text_to_image,model):

    plot =  get_data(movie_name)

    #m2s conversion
    plot_text = multiline_to_single_conv(plot)

    #chunking
    chunked_text = chunk_text(plot_text)


    #connect2couchbase
    username = "Administrator"
    password = "password"
    bucket_name = "b1"
    scope_name = "s1"
    collection_name = "movies"
        
    auth = PasswordAuthenticator(
        username,
        password,
    )

    cluster = Cluster('couchbase://172.23.108.107', ClusterOptions(auth))
    cluster.wait_until_ready(timedelta(seconds=5))
    cb = cluster.bucket(bucket_name)
    cb_coll = cb.scope(scope_name).collection(collection_name)
    
    #embedding the chunks and storing in Couchbase Vector DB
    ok = embed(model,chunked_text,movie_name,cb_coll)

    #vector index creation
    ok = create_index("hollywood")  

    #user query
    user_raw_query = query
    search_vector = user_query(model,query)

    #similarity search
    context = vector_search("hollywood",search_vector,6,cb_coll) #k=6

    #query_enhancer
    enhanced_query = query_enhancer(context,user_raw_query)
    # enhanced_query = query_enhancer_orca(context,user_raw_query)
    # enhanced_query = query_enhancer_mistral(context,user_raw_query)


    #text2image

    ok = threadit(enhanced_query,text_to_image)

    # if(text_to_image == "Stable diffusion X"):
    #     for i in range(1,5):
    #         ok = threadit(enhanced_query, )
    # elif(text_to_image == "Proteus"):
    #     for i in range(1,5):
    #         ok = proteus(movie_name,enhanced_query,str("q" + str( i)))
    # elif(text_to_image == "Playground"):
    #     for i in range(1,5):
    #         ok = playground(movie_name,enhanced_query,str("q" + str( i)))
    # else:
    #     for i in range(1,5):
    #         ok = openjourney(movie_name,enhanced_query,str("q" + str( i)))

    
    
    # ok = t2i_SD1(movie_name,enhanced_query,"q3")
    # ok = t2i_SD1(movie_name,enhanced_query,"q4")

    # p1 = multiprocessing.Process(target=t2i_SD1,args=(movie_name,enhanced_query,"q1"))
    # p2 = multiprocessing.Process(target=t2i_SD1,args=(movie_name,enhanced_query,"q2"))
    # p3 = multiprocessing.Process(target=t2i_SD1,args=(movie_name,enhanced_query,"q3"))
    # p4 = multiprocessing.Process(target=t2i_SD1,args=(movie_name,enhanced_query,"q4"))

    # p1.start()
    # p2.start()
    # p3.start()
    # p4.start()


    # p1.join()
    # p2.join()
    # p3.join()
    # p4.join()
            


    # ok = opendalle(movie_name, enhanced_query)
    # ok = playground(movie_name, enhanced_query)
    # ok = proteus(movie_name, enhanced_query)
    # # ok = sd1(movie_name, enhanced_query)
    # # ok = sd2(movie_name, enhanced_query)
    # ok = sdx(movie_name, enhanced_query)
    return 1


