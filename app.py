from flask import Flask, flash,url_for,render_template, jsonify, request, redirect,send_file,session
from FlagEmbedding import BGEM3FlagModel
import json
import threading
import zipfile
import os
import psutil
from datetime import datetime
import ollama
import re
import time
from flask_session import Session
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from app_python_srcs.vector_search_chat import vector_search_chat
from app_python_srcs.m2s_converter import multiline_to_single_conv
from app_python_srcs.user_query import user_query
from app_python_srcs.couchbase_init import couchbase_init
from app_python_srcs.generate_bot_response import llm_container
import app_python_srcs.main as main

    
#session variable declaration
session_no = 1
session_name = "session" + str(session_no)

session_no_a = 1
session_name_a = "session" + str(session_no_a)


#flask init
app = Flask(__name__)
app.secret_key = "hmm"


app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


EMAIL_REGEX = re.compile(r'^[\w\.-]+@couchbase\.com$')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    search_history = db.Column(db.JSON)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
with app.app_context():
    db.create_all()

def require_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session and request.endpoint != 'login':
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return decorated_function


with open('execution_time.txt', 'a') as file:
    print("execution time recording active")


    start_time = time.time()

    #models
    embed_model = BGEM3FlagModel('BAAI/bge-m3',  use_fp16=True)

    file.write("Time for embed model startup: {}\n".format(time.time() - start_time))

    start_time = time.time()

    #couchbase init
    cb_coll,db_coll,eb_coll,rb_coll,architect_coll = couchbase_init()

    file.write("Time for couchbase connection: {}\n".format(time.time() - start_time))

    #helper
    def imagine(movie_name,query,text_to_image):
        main.driver_function(movie_name, query,text_to_image,embed_model)


    @app.route('/view_logs',methods=['POST','GET'])
    def view_logs():
        log_data = session.get('log_data', [])
        return render_template('logs.html', log_data=log_data)


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            # Check if the user is already logged in
            if 'logged_in' in session:
                flash('You are already logged in.', 'info')
                return redirect(url_for('dashboard'))

            # Find the user by username
            user = User.query.filter_by(username=username).first()

            if user and user.check_password(password):
                # Check if the user is already logged in elsewhere
                if 'user_id' in session and session['user_id'] != user.id:
                    flash('Another session is active for this user. You cannot log in multiple times.', 'error')
                    return redirect(url_for('logout'))
                
                session['search_history'] = [] 
                # Log in the user
                session['logged_in'] = True
                session['user_id'] = user.id
                 # Initialize search history
                flash('You are now logged in.', 'success')
                return redirect(url_for('dash'))
            else:
                flash('Invalid username or password. Please try again.', 'error')
                return redirect(url_for('login'))

        return render_template('login.html')


    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']

            # Check if the email is valid
            if not EMAIL_REGEX.match(email):
                flash('Invalid email. Email must end with @couchbase.com.', 'error')
                return redirect(url_for('signup'))

            # Check if the email or username already exists
            if User.query.filter((User.email == email) | (User.username == username)).first():
                flash('Email or username already exists. Please choose different ones.', 'error')
                return redirect(url_for('signup'))
            
            session['search_history'] = [] 
            # Create a new user
            new_user = User(email=email, username=username)
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            flash('You have successfully signed up! You are now logged in.', 'success')
            session['log_data'] = []
            
            session['logged_in'] = True
            session['log_data'].append(f"Sign up successful. Username : {username}")
            return redirect(url_for('dash'))

        return render_template('login.html')

    @app.route('/logout',methods=['POST'])
    def logout():
        print(f"\nsearch history before :{session['search_history']}\n\n ")
        if 'user_id' in session:
            user_id = session.get('user_id')
            if user_id:
                user = User.query.get(user_id)  # Query the User model using SQLAlchemy
                if user:
                    search_history = session.get('search_history', [])
                    if user.search_history is None:
                        user.search_history = []  # Initialize search history if None
                    # Append session search history to user's existing search history
                    user.search_history.extend(search_history)
                    db.session.commit()
                    flash('Search history saved.', 'success')

        # Clear session data
        session.pop('logged_in', None)
        session.pop('user_id', None)
        session.pop('search_history', None)
        flash('You have been logged out.', 'info')
        return redirect(url_for('login'))

    @app.route('/',methods=['GET'])
    @require_login
    def dash():
        return render_template('dashboard.html')


    #doc-chat
    @app.route('/doc_chat')
    @require_login
    def launch_docchat():
        session['log_data'].append(f"CB Doc chat app launched")

        session['history'] = ""
        session['history_list'] = []

        return render_template('docchat.html',session_name=session_name)


    @app.route("/chat", methods=["POST"])
    @require_login
    def chat():
        # #log_cpu_mem_usage()
        main_start_time = time.time()
        start_time = time.time()
        user_input = request.form.get("user_input")
        print(user_input)

        session['search_history'].append(user_input)
        
        # print("search vector: ",search_vector)
        pattern1 = r'MB-\d+'
        tt = bool(re.search(pattern1, user_input))
        tt2 = 0
        if("issue" in user_input):
            tt2 =1
        
        if(tt==True or tt2 ==1):
            if(tt):
                pattern2 = r'MB-\d+'
                match = re.search(pattern2, user_input)
                iy = match.group(0)
                sss = ""
                for i in range(0,10):
                    sss+=iy
                    sss+=" "
                user_input = user_input + sss
            file.write("Time for parsing input (release): {}\n".format(time.time() - start_time))
            start_time = time.time()
            emb = embed_model.encode(user_input)['dense_vecs']
            file.write("Time for embedding the input (release): {}\n".format(time.time() - start_time))
            start_time = time.time()
            search_vector = emb.tolist()
            context = vector_search_chat("release_dot_p", search_vector, 1, rb_coll)
            file.write("Time for getting the context (release): {}\n".format(time.time() - start_time))
            start_time = time.time()

        else:
            file.write("Time for parsing input: {}\n".format(time.time() - start_time))
            start_time = time.time()
            emb = embed_model.encode(user_input)['dense_vecs']
            file.write("Time for embedding the input: {}\n".format(time.time() - start_time))
            start_time = time.time()
            search_vector = emb.tolist()
            context = vector_search_chat("tab1", search_vector, 6, cb_coll)
            file.write("Time for getting the context: {}\n".format(time.time() - start_time))
            start_time = time.time()

        context = multiline_to_single_conv(context)

        print(f"context : {context}")
        # bot_response = llm_container(user_input,context,session['history'])
        # response = ollama.chat(model='couch1', messages=[
        # {
        #     'role': 'user',
        #     'content': f"assistant, Q: Context:{context}. Conversation History: {session['history']} .Query:{user_input} . You are a couchbase documentation chatbot, answer the given query based on the context provided to you by docs provided as context. Also use conversation history to keep track of the conversation. Give the answer in less than 100 words. A:", # Prompt,
        # },
        # ])

        # response = ollama.chat(model='couch1',messages = [
        # {"role": "system", "content": "You are a helpful bot who reads texts and conversation history and answers questions about them.Answer precisely and in less then 70 words. Only use the texts and conversation history to answer the question. Don't make up answers if you can't find it in the texts."},
        # {"role": "user", "content": f"text :{context}. Conversation history:{session['history']}. QUESTION: {user_input}"},
        # ])
        # bot_response = response['message']['content']
        # print(bot)
        g  = 1
        bot_response = ''
        while(g):
            g+=1
            if(g==5):
                bot_response = "Sorry! There is some problem with LLM. Try again!"
                break
            user_input = user_input + "Answer in short and precise."
            response = ollama.chat(model='couch1',messages = [
            {"role": "system", "content": "You are a helpful bot who reads context and conversation history and answers questions about them.Answer precisely and in less than 50 words. Only use the context and conversation history to answer the question."},
            {"role": "user", "content": f"text :{context}. Conversation history:{session['history']}. QUESTION: {user_input}"},
            ])
            bot_response = response['message']['content']
            if(bot_response!=""):
                break
        # print(bot)
        pattern = r'[^a-zA-Z0-9\s\n.,]'
        bot_response =  re.sub(pattern, '', bot_response)
        bot_response = re.sub(re.escape("answer"), '', bot_response, flags=re.IGNORECASE)
        bot_response = bot_response.replace("\n\n","\n")

        file.write("Time for model response(current oi): {}\n".format(time.time() - start_time))
        start_time = time.time()

        session['history'] += f"Query: {user_input}. Your response:{bot_response}"
        session['history_list'].append({"user":user_input,"ai":bot_response})
        print("history:",session['history'])
        print("his list:",session['history_list'])
        print("res:",bot_response)
        file.write("Time for all the operations : {}\n".format(time.time() - main_start_time))
        return jsonify({"bot_response": bot_response})


    #new session 
    @app.route("/newsession", methods=["POST"])
    @require_login
    def newsession():
        # #log_cpu_mem_usage()
        session['log_data'].append(f"New session created")
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


    #load session
    @app.route("/loadsession", methods=["POST"])
    @require_login
    def loadsession():
        # #log_cpu_mem_usage()

        global session_name
        name = request.form.get("session_name")
        past = session['history_list']

        db_coll.upsert(session_name, past)

        session_name = name
        result = db_coll.get(name)
        data = result.value

        session['history'] = data
        session['history_list'] = data

        data  = json.dumps(data)
        return jsonify({"data":data})


    #doc-chat
    @app.route('/archi_chat')
    @require_login
    def launch_docchat_a():
        # #log_cpu_mem_usage()

        session['history_a'] = ""
        session['history_list_a'] = []

        return render_template('archichat.html',session_name=session_name_a)

    #gets the user input and sends the LLM response back
    @app.route("/chat_a", methods=["POST"])
    @require_login
    def chat_a():
        # #log_cpu_mem_usage()
        user_input = request.form.get("user_input")
        print(user_input)
        session['search_history'].append(user_input)
        
        # print("search vector: ",search_vector)
        pattern1 = r'MB-\d+'
        tt = bool(re.search(pattern1, user_input))
        tt2 = 0
        if("issue" in user_input):
            tt2 =1
        
        if(tt==True or tt2 ==1):
            if(tt):
                pattern2 = r'MB-\d+'
                match = re.search(pattern2, user_input)
                iy = match.group(0)
                sss = ""
                for i in range(0,10):
                    sss+=iy
                    sss+=" "
                user_input = user_input + sss
            emb = embed_model.encode(user_input)['dense_vecs']
            search_vector = emb.tolist()
            context = vector_search_chat("release_dot_p", search_vector, 1, rb_coll)

        else:
            emb = embed_model.encode(user_input)['dense_vecs']
            search_vector = emb.tolist()
            context = vector_search_chat("architect", search_vector, 6, architect_coll)

        context = multiline_to_single_conv(context)

        print(f"context : {context}")
        # bot_response = llm_container(user_input,context,session['history'])
        # response = ollama.chat(model='mistral', messages=[
        # {
        #     'role': 'user',
        #     'content': f"assistant, Q: Context:{context}. Conversation History: {session['history']} .Query:{user_input} . You are a couchbase documentation chatbot, answer the given query based on the context provided to you by docs provided as context. Also use conversation history to keep track of the conversation. Give the answer in less than 100 words. A:", # Prompt,
        # },
        # ])
        g  = 1
        bot_response = ''
        while(g):
            g+=1
            if(g==5):
                bot_response = "Sorry! There is some problem with LLM. Try again!"
                break
            user_input = user_input + "Answer in short and precise."
            response = ollama.chat(model='architect1',messages = [
            {"role": "system", "content": "You are a helpful bot who reads context and conversation history and answers questions about them.Answer precisely and in less than 50 words. Only use the context and conversation history to answer the question."},
            {"role": "user", "content": f"text :{context}. Conversation history:{session['history_a']}. QUESTION: {user_input}"},
            ])
            bot_response = response['message']['content']
            # bot_response = llm_container(context,user_input,session['history_a'])
            if(bot_response!=""):
                break
        # print(bot)
        pattern = r'[^a-zA-Z0-9\s\n.,]'
        bot_response =  re.sub(pattern, '', bot_response)
        bot_response = re.sub(re.escape("answer"), '', bot_response, flags=re.IGNORECASE)
        bot_response = bot_response.replace("\n\n","\n")
        session['history_a'] += f"Query: {user_input}. Your response:{bot_response}"
        session['history_list_a'].append({"user":user_input,"ai":bot_response})
        print("history:",session['history_a'])
        print("his list:",session['history_list_a'])
        print("res:",bot_response)
        return jsonify({"bot_response": bot_response})


    #new session 
    @app.route("/newsession_a", methods=["POST"])
    @require_login
    def newsession_a():
        #log_cpu_mem_usage()
        name = request.form.get("session_name")
        past = session['history_list_a']
        result = eb_coll.upsert(name, past)
        print(result.cas)

        session['history_a'] = ""
        session['history_list_a'] = []
        global session_no_a
        
        print("name :",name)
        current = int(''.join(filter(str.isdigit, name)))
        print("current: ",current)
        new_val = max(current, session_no_a)
        print("newval:",new_val)

        new_val +=1
        session_no_a = new_val
        new_name = "session"+str(new_val)
        print(new_name)
        global session_name_a
        session_name_a = new_name
        return jsonify({"new_name":new_name})


    #load session
    @app.route("/loadsession_a", methods=["POST"])
    @require_login
    def loadsession_a():
        #log_cpu_mem_usage()

        global session_name_a
        name = request.form.get("session_name")
        past = session['history_list_a']

        eb_coll.upsert(session_name, past)

        session_name_a = name
        result = eb_coll.get(name)
        data = result.value

        session['history_a'] = data
        session['history_list_a'] = data

        data  = json.dumps(data)
        return jsonify({"data":data})


    @app.route('/create', methods=['POST'])
    @require_login
    def run_task():
        #log_cpu_mem_usage()
        # Start the task in a separate threa    
        movie_name = request.form.get('movie_name')
        query = request.form.get('query')
        session['search_history'].append(query)

        query_enhancer = request.form.get('queryEnhancer')
        text_to_image = request.form.get('textToImage')
        quality = request.form.get('quality')

        # print(movie_name+"\n"+query+"\n"+query_enhancer+"\n"+text_to_image+"\n"+quality)
        print("movie:",movie_name)
        print("query:",query)
        print("query_enhancer:",query_enhancer)
        print("texttoim:",text_to_image)
        print("quality:",quality)

        task_thread = threading.Thread(target=imagine(movie_name,query,text_to_image))
        task_thread.start()
        return render_template('movie_result.html')


    @app.route('/create')
    @require_login
    def create():
        #log_cpu_mem_usage()
        return render_template('movie.html')


    @app.route('/download_files', methods=['GET'])
    @require_login
    def download_files():
        #log_cpu_mem_usage()
        directory = './static/output/'
        file_names = ['q1.png', 'q2.png', 'q3.png', 'q4.png']
        memory_file = zipfile.ZipFile('files.zip', 'w', zipfile.ZIP_DEFLATED)

        for file_name in file_names:
            file_path = os.path.join(directory, file_name)
            if os.path.exists(file_path):
                memory_file.write(file_path, file_name)

        memory_file.close()
        return send_file('files.zip', as_attachment=True)

    if __name__ == '__main__':
        app.run(debug=True,port=5100)


