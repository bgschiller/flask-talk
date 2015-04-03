from flask import Flask, render_template

app = Flask(__name__)
app.debug = True
@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/story/<room_name>')
def story(room_name):
    """Return the story for a given room"""
    # This story taken from http://foldingstory.com/pfuf2/
    return render_template('story.html', lines=[
      "Nobody knows how Saturn got its rings. But I have a theory.",
      "A theory that has been ignored by pretty much everyone at this Cosmic Conference. It's really because my theory is so awesome that all these so-called academics are jealous. Saturn",
      "should not be a planet anymore. We got rid of Pluto and no one misses it, so Saturn should be next, because real planets don't have rings. The Cosmic Conference started throwing",
      "planets out left & right. Mercury was too small. Neptune? Who cares? Pretty soon it was just Venus, Earth, Mars, and Jupiter. Oh, and the sun. Who could forget good old Planet Sun.",
      "After creationism became the law of the land, they issued a decree that the Sun did indeed revolve around the Earth. Elsewhere, pagans decided to bring back",
      "Worship of the stag god, and to that end they first had to rescue the Gundestrup Cauldron from the heathens who had taken over the senate, and who were using it to",
      "promote the cult of Cernunnos. Even Torquatus showed them favor. The Republic was in danger. The cult could not persist without the rites..The Gundestrup Cauldron must be taken!",
      "I hastily drafted some legionnaires at a local taverna, and stormed the villa where the cult held its mysterious cauldron. Some of my men fell at the gate out of sheer befuddlement",
      "but the rest of us closed ranks and persisted until we found the villa's inner sanctum. The residents round their cauldron looked at us from their bizarre masks. Our legionnaires f",
      "formed, once again, the ancient circle and spoke the mystic oath. The aftermath, indescribable. At last our mission was complete. Silently, we exited, the treasure was ours."
    ])


if __name__ == '__main__':
    app.run()
