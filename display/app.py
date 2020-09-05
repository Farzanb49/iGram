from flask import Flask, render_template, request, url_for, flash, redirect, Response
import sqlite3
from werkzeug.exceptions import abort
import blockchain
from chatbot_model import chatbot_response
from scrape import scrape_data


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hk416ak47m16'

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    user_request = request.args.get('msg')  # Fetching input from the user
    user_request = user_request.lower()
    if len(user_request.split(" ")) > 1:
        check_search = user_request.split(" ")[0]
        if check_search == 'google':
            user_request = user_request.replace("google","")
            user_request = user_request.translate ({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
            check_query = user_request.split(" ")[1]
            check_text = user_request.split(" ")[1:3]
            if check_text == check_wikipedia1 or check_text == check_wikipedia2:
                response = scrape_data(user_request, "wikipedia")
            elif check_text == check_wikihow:
                response = scrape_data(user_request, "wikihow")
            elif check_query == "nearby":
                response = scrape_data(user_request, "nearby")
            else:
                response = scrape_data(user_request, "")
                
        else:
            response = chatbot_response(user_request)                

    else:
        response = chatbot_response(user_request)
    
    return response
@app.route('/', methods=['GET', 'POST'])
def login():
   # if request.method == 'POST':
   #     session.pop('user_id', None)

   #     username = request.form['username']
    #    password = request.form['password']
        
    #    user = [x for x in users if x.username == username][0]
    #    if user and user.password == password:
     #       session['user_id'] = user.id
      #      return redirect(url_for('home'))

       # return redirect(url_for('login'))

    return render_template('login.html')
@app.route('/register', methods=['GET','POST'])
def register():
    return render_template('registration.html')
@app.route('/feed')
def feed():
    return render_template('home.html')

@app.route('/line')
def line():
    return render_template('analysis.html')

@app.route('/space')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('space.html', posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
    

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, category, content) VALUES (?, ?, ?)', (title, category, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    
    return render_template('create.html')



@app.route('/userinfo', methods = ('GET','POST'))
def userinfo():
    if request.method =='POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        blockchain.automation(name, address, email)
        
        if not name:
            flash('Name is required to proceed!')
        else:
            return redirect(url_for('create'))
        
    return render_template('userinfo.html')





