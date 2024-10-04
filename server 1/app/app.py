from flask import Flask, render_template, request, redirect, url_for, g, jsonify, session # Import 'g'
from functools import wraps

import subprocess
import sqlite3
import hashlib


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True 
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Database setup
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('cms.db')
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Create table (if it doesn't exist)
with app.app_context():
    db = get_db()
    db.executescript('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        );
               
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER,
            name TEXT,
            lastname TEXT,
            username TEXT,
            password TEXT
        );
               
        INSERT OR IGNORE INTO posts (title,content) VALUES
	 ("This is a title","The magnificent content");

        INSERT OR IGNORE INTO users (id,name,lastname,username,password) VALUES
	 (1,"web","master","webmaster","15c4683193f210ca9c640af9241e8c18");
               
    ''')

# Homepage (list all posts)
@app.route('/')
def index():
    db = get_db()
    posts = db.execute('SELECT * FROM posts').fetchall()
    return render_template('index.html', posts=posts) 

@app.route('/about')
def about():
    db = get_db()
    posts = db.execute('SELECT * FROM posts').fetchall()
    return render_template('about.html', posts=posts) 


@app.route('/contact')
def contact():
    db = get_db()
    posts = db.execute('SELECT * FROM posts').fetchall()
    return render_template('contact.html', posts=posts) 


@app.route('/solutions')
def solutions():
    db = get_db()
    posts = db.execute('SELECT * FROM posts').fetchall()
    return render_template('solutions.html', posts=posts) 

@app.route('/investor')
def investor():
    db = get_db()
    posts = db.execute('SELECT * FROM posts').fetchall()
    return render_template('investor.html', posts=posts) 

# Create new post form
@app.route('/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        db.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
        db.commit()
        return redirect(url_for('index'))
    return render_template('new_post.html')

# Edit post form
@app.route('/api/posts', methods=['GET'])
def get_posts():
    db = get_db()
    cursor = db.execute('SELECT * FROM posts')  # Get the cursor
    posts = cursor.fetchall()  # Fetch all the rows

    # Convert the rows to a list of dictionaries for easy JSON serialization
    post_list = []
    for row in posts:
        post_dict = {}
        for idx, col in enumerate(cursor.description):  # Get column names
            post_dict[col[0]] = row[idx]
        post_list.append(post_dict)
    return jsonify(post_list)

@app.route('/api/posts/detail', methods=['GET'])
def get_post():
    db = get_db()
    post_id = request.args.get('id')

    # Vulnerable query with string concatenation
    query = 'SELECT * FROM posts WHERE id = ' + post_id 
    cursor = db.execute(query) 

    posts = cursor.fetchall()

    # Convert rows to a list of JSON objects
    post_list = []
    for row in posts:
        post_dict = {}
        for idx, col in enumerate(cursor.description):
            post_dict[col[0]] = row[idx]
        post_list.append(post_dict)

    return jsonify(post_list) 


#Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'] or ''
        password = request.form['password'] or ''
        hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()


        # Vulnerable query (intentionally insecure for the CTF)
        with get_db() as db:
            user = db.execute(
                'SELECT * FROM users WHERE username = ? AND password = ?',
                (username, hashed_password)
            ).fetchone()

        if user:
            session['user_id'] = user['id']
            return redirect(url_for('panel'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()  # Clear the entire session data
    return redirect(url_for('login'))

#Login required websites
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' in session:  # Or whatever key you use to store user info
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))  # Redirect to login if not logged in
    return decorated_function

#panel
@app.route('/panel')
@login_required
def panel():
    return render_template('panel.html') 

@app.route('/stats')
@login_required
def stats():
    return render_template('stats.html') 


@app.route('/api/dashboard/stats')
# @login_required
def dashboard_stats():
    command = request.args.get('command')
    # Vulnerable: Direct use of user input in subprocess
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT) 
        return jsonify(output.decode())  # Decode the output for display
    except subprocess.CalledProcessError as e:
        return jsonify(e.output.decode())



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')