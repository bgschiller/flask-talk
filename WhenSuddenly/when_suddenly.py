from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
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
# Views

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/story/<room_name>/', methods=['GET', 'POST'])
def story(room_name):
    """Return the story for a given room"""
    if request.method == 'POST':
        return "Received data to add to a story: {}".format(dict(request.form))
    # This story taken from http://foldingstory.com/pfuf2/
    return render_template('story.html',
                           room_name=room_name,
                           lines=Paragraph.query
                                 .filter_by(room=room_name)
                                 .order_by(Paragraph.id)
                                 .all())


if __name__ == '__main__':
    app.run()
