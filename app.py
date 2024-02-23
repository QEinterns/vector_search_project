
from flask import Flask, render_template, jsonify, request, redirect,send_file
import time
import threading
import main
import zipfile
import os
from flask import Flask, render_template, request, jsonify, session,g
from llama_cpp import Llama
from user_query import user_query
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster
from couchbase.options import (ClusterOptions, ClusterTimeoutOptions,QueryOptions)
from datetime import timedelta
from vector_search import vector_search
from m2s_converter import multiline_to_single_conv
import json
from vecsearch import vector_search1
session_no = 1
session_name = "session" + str(session_no)




app = Flask(__name__)
app.secret_key = "hmm"

def call_helper(movie_name,query,text_to_image):
    main.driver_function(movie_name, query,text_to_image)


llm = Llama(
            model_path='/Users/spatra/Desktop/Movie/query_enhancer/mistral-7b-openorca.Q4_0.gguf',
            # n_gpu_layers=-1, # Uncomment to use GPU acceleration
            # seed=1337, # Uncomment to set a specific seed
            n_ctx=10000, # Uncomment to increase the context window
      )

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

db = cluster.bucket(bucket_name)
db_coll = db.scope(scope_name).collection("c3")


def generate_bot_response(user_input,context):
    if(len(context)>9600):
            context = context[:9200]
    print("context : ",context)
    print("\n\n")
    history = session.get('history', '')
    history_list = session.get('history_list', [])
    user_input = user_input + "Answer in paragraph."
    output = llm(
        
         f"Q: Context:{context}. Conversation History: {history} .Query:{user_input} . You are a couchbase documentation chatbot, answer the given query based on the context provided to you by docs provided as context. Also use conversation history to keep track of the conversation. A:", # Prompt
        max_tokens=None, # Generate up to 32 tokens, set to None to generate up to the end of the context window
    # Echo the prompt back in the output
    ) # Generate a completion, can also call create_completion
    # print(output)
    print("output::",output)
    ut = str(output['choices'][0]['text'])
    ut  = multiline_to_single_conv(ut)

    history += f"Query: {user_input}. Your response:{ut}"
    
    history_list.append({"user":user_input,"ai":ut})
    
    session['history'] = history
    session['history_list'] = history_list
    # print(history)
    print("\n")
    print(history_list)
    print("\n")
    return str(output['choices'][0]['text'])
    
    # return user_input









@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')








@app.route("/chatmain")
def chatmain():
    
    if 'history' in session:
        session.pop('history')
    session['history'] = ""

    if 'history_list' in session:
        session.pop('history_list')
    session['history_list'] = []

    return render_template("index_chat.html",session_name=session_name)


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form.get("user_input")
    search_vector = user_query(user_input)
    context = vector_search1("docs", search_vector, 6, cb_coll)
    context  = multiline_to_single_conv(context)
    print(context)
    bot_response = generate_bot_response(user_input,context)
    print(bot_response)
    return jsonify({"bot_response": bot_response})


@app.route("/newsession", methods=["POST"])
def newsession():
    name = request.form.get("session_name")
    past = session['history_list']
    result = db_coll.upsert(name, past)
    print(result.cas)

    if(session['history']!=""):
        session['history'] = ""
        session['history_list'] = []
    global session_no
    
    print("name :",name)
    current = int(''.join(filter(str.isdigit, name)))
    print("current: ",current)
    new_val = max(current, session_no)
    print("newval:",new_val)

    new_val +=1
    session_no = new_val
    new_name = "session"+str(new_val)
    print(new_name)
    global session_name
    session_name = new_name
    return jsonify({"new_name":new_name})


@app.route("/loadsession", methods=["POST"])
def loadsession():


    global session_name
    name = request.form.get("session_name")
    past = session['history_list']
    # if(session['history']!=""):
    #     result = db_coll.upsert(name, past)
    
    result1 = db_coll.upsert(session_name, past)

    session_name = name
    result = db_coll.get(name)
    data = result.value

    print(data)
    print(type(data))
    session['history'] = data
    session['history_list'] = data

    data  = json.dumps(data)
    return jsonify({"data":data})


















@app.route('/create', methods=['POST'])
def run_task():
    # Start the task in a separate threa    
    movie_name = request.form.get('movie_name')
    query = request.form.get('query')

    query_enhancer = request.form.get('queryEnhancer')
    text_to_image = request.form.get('textToImage')
    quality = request.form.get('quality')

    # print(movie_name+"\n"+query+"\n"+query_enhancer+"\n"+text_to_image+"\n"+quality)
    print("movie:",movie_name)
    print("query:",query)
    print("query_enhancer:",query_enhancer)
    print("texttoim:",text_to_image)
    print("quality:",quality)

    
    


    task_thread = threading.Thread(target=call_helper(movie_name,query,text_to_image))
    task_thread.start()
    return render_template('result.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/download_files', methods=['GET'])
def download_files():
    # Define the directory where your files are located
    directory = './static/output/'

    # List of file names to be included in the zip archive
    file_names = ['q1.png', 'q2.png', 'q3.png', 'q4.png']

    # Create a zip file in memory
    memory_file = zipfile.ZipFile('files.zip', 'w', zipfile.ZIP_DEFLATED)
    
    # Add each file from the directory to the zip file
    for file_name in file_names:
        file_path = os.path.join(directory, file_name)
        if os.path.exists(file_path):
            memory_file.write(file_path, file_name)

    # Close the zip file
    memory_file.close()

    # Send the zip file as a response to the client
    return send_file('files.zip', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True,port=5100)
