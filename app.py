import config
config.init()
from flask import Flask, render_template, request
from etude import Etude
from abc_converter import convert_to_abc
from generator import Generator
from random import choice
from utils import *
import websocket_events


app = Flask(__name__)
config.socketio.init_app(app)
etude: Etude = Etude()

@app.route("/")
@app.route("/index")
def index():
    config.yin_mode = True
    websocket_events.stop_audio_stream()
    return render_template("index.html")

@app.route("/latencyTest")
def latency_test():
    config.yin_mode = True
    return render_template("latencyTest.html")

@app.route("/simpleReadPractice")
def simple_read_practice():
    config.yin_mode = True
    return render_template("simpleReadPractice.html")

@app.route("/startChordPractice", methods=["GET", "POST"])
@app.route("/chordReadPractice")
def chord_read_practice():
    config.yin_mode = False
    if request.method == "POST":
        if request.form["mode"] == "random":
            mode = choice(["maj", "min"])
            if mode == "maj":
                key = choice(["C", "G", "F", "D", "Bb", "A", "Eb", "E", "Ab", "B", "Db"])
            else:
                key = choice(["A", "E", "D", "B", "G", "F#", "C", "F", "C#", "Bb", "G#"])
        else:
            mode = request.form["mode"]
            key = request.form["key"]
    else:
        key = "C"
        mode = "maj"
        
    return render_template("chordReadPractice.html", key=key, mode=mode)

@app.route("/startFullReadPractice", methods=["GET", "POST"])
@app.route("/fullReadPractice")
def full_read_practice():
    global etude
    config.yin_mode = True
    if request.method == "POST":
        etude.tempo = ["", request.form["tempo"]]
        mode = request.form["mode"]
        key = request.form["key"]
    else:
        etude.set_tempo(choice(["very_slow"]))
        mode = "random"
        key = "random"
    
    etude.set_key(key, mode)
    etude.title = ""
    etude.focus = "air_column"
    etude.length = "2"
    etude.metre = "4/4"
    etude.ambitus = [0, 15]
    generator: Generator = Generator(etude)
    etude = generator.generate_etude()
    abc: str = convert_to_abc(etude)
    print("\n", abc, "\n")

    return render_template("fullReadPractice.html", abc=abc)

if __name__ == "__main__":
    config.socketio.run(app, host="0.0.0.0", port=5000, debug=True, use_reloader=False)
