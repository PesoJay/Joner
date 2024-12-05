from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import pyaudio
import numpy as np
from utils import *
from yinPitchDetection import *

current_audio_task = None
is_streaming = False

app = Flask(__name__)
socketio = SocketIO(app)

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
    return render_template("fullReadPractice.html")

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