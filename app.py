from flask import Flask, render_template, request, url_for, flash,redirect,abort
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecretKey'

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

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html',posts=posts)

@app.route('/create/',methods=('GET','POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        points = request.form['points']

        if not name:
            flash('Name is required!')
        elif not points:
            flash('Points is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (name, points) VALUES (?, ?)',
                         (name, points))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html')

# ...

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        name = request.form['name']
        points = request.form['points']

        if not name:
            flash('Name is required!')

        elif not points:
            flash('Points is required!')

        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET name = ?, points = ?'
                         ' WHERE id = ?',
                         (name, points, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['name']))
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True) 
