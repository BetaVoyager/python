from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'supersecret'  # Needed for sessions and CSRF

DATABASE = 'database.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db:
        db.close()

def init_db():
    with sqlite3.connect(DATABASE) as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS greetings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            )
        ''')
        db.commit()

class NameForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    submit = SubmitField('Greet Me')

@app.route('/')
def home():
    db = get_db()
    cur = db.execute('SELECT id, name FROM greetings ORDER BY id DESC')
    names = cur.fetchall()
    return render_template('index.html', names=names)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        db = get_db()
        db.execute('INSERT INTO greetings (name) VALUES (?)', (name,))
        db.commit()
        flash(f"Hello, {name}!", 'success')
        return redirect(url_for('home'))
    return render_template('hello.html', form=form)

@app.route('/delete/<int:name_id>', methods=['POST'])
def delete(name_id):
    db = get_db()
    db.execute('DELETE FROM greetings WHERE id = ?', (name_id,))
    db.commit()
    flash("Name deleted.", 'warning')
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
