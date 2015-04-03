import random
import string
from flask import Flask, render_template, request, session, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = "shh, it's a secret!"
app.debug = True

db = SQLAlchemy(app)

##################
# Models

class Paragraph(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(15))
    author = db.Column(db.String(63))
    text = db.Column(db.Text())

##################
# Helpers


def rand_str(length):
    return ''.join(random.choice(string.letters + string.digits)
                   for _ in range(length))


##################
# Views

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('story', room_name=rand_str(15)))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('story', room_name=rand_str(15)))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/story/<room_name>/', methods=['GET', 'POST'])
def story(room_name):
    """Return the story for a given room"""
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        p = Paragraph(room=room_name,
                      author=session['username'],
                      text=request.form['new_paragraph'])
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('story', room_name=room_name))

    return render_template('story.html',
                           room_name=room_name,
                           lines=Paragraph.query
                                 .filter_by(room=room_name)
                                 .order_by(Paragraph.id)
                                 .all())


if __name__ == '__main__':
    app.run()
