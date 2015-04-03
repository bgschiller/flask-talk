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
                           lines=[
        {"author": "lucielucie", "text": "Nobody knows how Saturn got its rings. But I have a theory."},
        {"author": "MoralEnd", "text": "A theory that has been ignored by pretty much everyone at this Cosmic Conference. It's really because my theory is so awesome that all these so-called academics are jealous. Saturn"},
        {"author": "MangoMania", "text": "should not be a planet anymore. We got rid of Pluto and no one misses it, so Saturn should be next, because real planets don't have rings. The Cosmic Conference started throwing"},
        {"author": "49erFaithful", "text": "planets out left & right. Mercury was too small. Neptune? Who cares? Pretty soon it was just Venus, Earth, Mars, and Jupiter. Oh, and the sun. Who could forget good old Planet Sun."},
        {"author": "Chaz", "text": "After creationism became the law of the land, they issued a decree that the Sun did indeed revolve around the Earth. Elsewhere, pagans decided to bring back"},
        {"author": "Benwicky", "text": "Worship of the stag god, and to that end they first had to rescue the Gundestrup Cauldron from the heathens who had taken over the senate, and who were using it to"},
        {"author": "SlimWhitman", "text": "promote the cult of Cernunnos. Even Torquatus showed them favor. The Republic was in danger. The cult could not persist without the rites..The Gundestrup Cauldron must be taken!"},
        {"author": "grok", "text": "I hastily drafted some legionnaires at a local taverna, and stormed the villa where the cult held its mysterious cauldron. Some of my men fell at the gate out of sheer befuddlement"},
        {"author": "BlastedHeath", "text": "but the rest of us closed ranks and persisted until we found the villa's inner sanctum. The residents round their cauldron looked at us from their bizarre masks. Our legionnaires f"},
        {"author": "PurpleProf", "text": "formed, once again, the ancient circle and spoke the mystic oath. The aftermath, indescribable. At last our mission was complete. Silently, we exited, the treasure was ours."}
    ])


if __name__ == '__main__':
    app.run()
