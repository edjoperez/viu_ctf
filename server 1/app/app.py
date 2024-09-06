from flask import Flask, render_template, request, redirect, url_for, g # Import 'g'
import sqlite3

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True  # Enable template auto-reloading



app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True 

# Database setup
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('cms.db')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Create table (if it doesn't exist)
with app.app_context():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')

# Homepage (list all posts)
@app.route('/')
def index():
    db = get_db()
    posts = db.execute('SELECT * FROM posts').fetchall()
    return render_template('index.html', posts=posts) 

@app.route('/login')
def login():
    return render_template('login.html') 

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
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = db.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        db.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (title, content, id))
        db.commit()
        return redirect(url_for('index'))
    return render_template('edit_post.html', post=post)

# Delete post
@app.route('/delete/<int:id>')
def delete_post(id):
    db.execute('DELETE FROM posts WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)