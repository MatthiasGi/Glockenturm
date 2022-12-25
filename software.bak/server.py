from flask import Flask

from lib.carillon import Carillon
from lib.direktorium import TodayDirektorium
from lib.songs import Library

from customstriker import CustomStriker

app = Flask(__name__)
lib = Library('../songs')

carillon = Carillon()
direktorium = TodayDirektorium()
striker = CustomStriker(carillon, direktorium)

@app.route('/')
def hello():
    return dict(hello='world!')

@app.route('/songs')
def songs_index():
    songs = [dict(id=i, number=s.number, title=s.title) for i, s in enumerate(lib.songs)]
    return dict(songs=songs)

@app.route('/songs/<int:song_id>')
def songs_show(song_id):
    s = lib.songs[song_id]
    return dict(id=song_id, number=s.number, title=s.title)

@app.route('/songs/<int:song_id>/play')
def songs_play(song_id):
    s = lib.songs[song_id]
    striker.play(s.messages)
    return songs_show(song_id)
