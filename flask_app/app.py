import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, g

app = Flask(__name__)
app.secret_key = 'supersecret'

DATABASE = 'database.db'

# Get DB connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db

# Close DB after each request
@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db:
        db.close()

# Initialize database (run once manually)
def init_db():
    with sqlite3.connect(DATABASE) as db:
        db.execute('CREATE TABLE IF NOT EXISTS greetings (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)')
        db.commit()

@app.route('/')
def home():
    db = get_db()
    cur = db.execute('SELECT id, name FROM greetings ORDER BY id DESC')
    names = cur.fetchall()  # List of (id, name)
    return render_template('index.html', names=names)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            db = get_db()
            db.execute('INSERT INTO greetings (name) VALUES (?)', (name,))
            db.commit()
            flash(f"Hello, {name}!", 'success')
            return redirect(url_for('home'))
        else:
            flash("Please enter a name.", 'danger')
    return render_template('hello.html')

@app.route('/delete/<int:name_id>', methods=['POST'])
def delete(name_id):
    db = get_db()
    db.execute('DELETE FROM greetings WHERE id = ?', (name_id,))
    db.commit()
    flash("Name deleted.", 'warning')
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
