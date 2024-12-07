from flask import Flask, redirect, url_for, render_template, request
from etude import Etude
from abc_converter import convert_to_abc
from generator import Generator
from flask_socketio import SocketIO, emit
import pyaudio
import numpy as np
from random import choice
from utils import *
from yinPitchDetection import *

current_audio_task = None
is_streaming = False

app = Flask(__name__)
socketio = SocketIO(app)
etude: Etude = Etude()

def audio_stream():
    global is_streaming
    p = pyaudio.PyAudio()
    
    stream = p.open(
        format=pyaudio.paFloat32,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )
    try:
        while is_streaming:
            data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.float32)
            frequency = get_pitch_yin(data, SAMPLE_RATE)
            if frequency:
                note = find_nearest_note(frequency)
            else:
                note = None
            if note:
                socketio.emit("note_detected", {"note": note})
            socketio.sleep(0)  # Allow other tasks to run
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        is_streaming = False
        print("Audio stream stopped")  # Debug print


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/latencyTest")
def latency_test():
    return render_template("latencyTest.html")

@app.route("/simpleReadPractice")
def simple_read_practice():
    return render_template("simpleReadPractice.html")

@app.route("/fullReadPractice")
def full_read_practice():
    global etude
    etude.title = ""
    etude.focus = "air_column"
    etude.length = "2"
    etude.set_tempo(choice(["very_slow"]))
    etude.metre = "4/4"
    mode = "maj"
    key = "C"
    etude.set_key(key, mode)
    etude.ambitus = [0, 10]
    generator: Generator = Generator(etude)
    etude = generator.generate_etude()
    abc: str = convert_to_abc(etude)
    print("\n", abc, "\n")

    return render_template("fullReadPractice.html", abc=abc)

@socketio.on("start_audio_stream")
def start_audio_stream():
    global current_audio_task, is_streaming
    print("Started Audio Stream")
    if is_streaming:
        print("Audio Stream already running")
        return
    
    is_streaming = True
    current_audio_task = socketio.start_background_task(target=audio_stream)

@socketio.on("stop_audio_stream")
def stop_audio_stream():
    global is_streaming, current_audio_task
    is_streaming = False
    current_audio_task = None
    print("Stop audio stream requested")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)