import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

import json
import random
import string
from flask import Flask, render_template, request, session, redirect, url_for, Response
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = "shh, it's a secret!"

db = SQLAlchemy(app)

##################
# Models

class Paragraph(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(5))
    author = db.Column(db.String(63))
    text = db.Column(db.Text())

##################
# Helpers


def rand_str(length):
    return ''.join(random.choice(string.letters + string.digits)
                   for _ in range(length))

def event_stream(room_name, latest_event=None):
    while True:
        updates = (Paragraph.query
                   .filter(Paragraph.room == room_name, Paragraph.id > (latest_event or 0))
                   .order_by(Paragraph.id))
        gevent.sleep(0.5)
        for update in updates:
            yield 'data: {}\n\n'.format(
                json.dumps(dict(text=update.text, author=update.author, id=update.id)))
            latest_event = update.id

##################
# Views

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('story', room_name=rand_str(5)))
    else:
        return redirect(url_for('login'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        if 'next' in request.args:
            room_name = request.args['next']
        else:
            room_name = rand_str(15)
        return redirect(url_for('story', room_name=room_name))
    return render_template('login.html')

@app.route('/logout/')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/story/<room_name>/', methods=['GET', 'POST'])
def story(room_name):
    """Return the story for a given room"""
    if 'username' not in session:
        return redirect(url_for('login', next=room_name))

    if request.method == 'POST':
        p = Paragraph(room=room_name,
                      author=session['username'],
                      text=request.form['new_paragraph'])
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('story', room_name=room_name))

    return render_template('story.html',
                           room_name=room_name,
                           username=session['username'],
                           lines=Paragraph.query
                                 .filter_by(room=room_name)
                                 .order_by(Paragraph.id)
                                 .all())


@app.route('/stream/<room_name>/')
def stream(room_name):
    return Response(event_stream(room_name,
                                 latest_event=request.args.get('since')),
                    mimetype='text/event-stream')


if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', 5000), app)
    http_server.serve_forever()
