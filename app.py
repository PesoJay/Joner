from flask import Flask, redirect, url_for, render_template, request
from etude import Etude
from abc_converter import convert_to_abc
from generator import Generator
from flask_socketio import SocketIO, emit
import pyaudio
import numpy as np
from random import choice
from utils import *
from yinPitchDetection import get_pitch_yin
from chordDetection import *

current_audio_task = None
is_streaming = False
yin_mode = False

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading', ping_timeout=1, ping_interval=1)
etude: Etude = Etude()

def callback(in_data, frame_count, time_info, status):
    global is_streaming, yin_mode
    if not is_streaming:
        return (None, pyaudio.paComplete)
    
    data = np.frombuffer(in_data, dtype=np.float32)
    rms = np.sqrt(np.mean(np.square(data)))
    
    if rms > 0.01:
        if yin_mode:
            frequency = get_pitch_yin(data, SAMPLE_RATE)
            if frequency:
                note = find_nearest_note(frequency)
                if note: 
                    socketio.emit("note_detected", {"note": note}, namespace="/")
        else:
            frequencies = get_note_frequencies(data, SAMPLE_RATE)
            notes = find_notes_in_chord(frequencies)
            if notes:
                chord = identify_chord(notes)
                if chord:
                    socketio.emit("chord_detected", {"chord": chord}, namespace="/")
    
    return (in_data, pyaudio.paContinue)

def audio_stream():
    global is_streaming, yin_mode
    p = pyaudio.PyAudio()
    try:
        stream = p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=SAMPLE_RATE,
            input=True,
            frames_per_buffer= YIN_CHUNK if yin_mode else CHORD_CHUNK,
            stream_callback=callback,
            input_device_index=None
        )
        print("Mode: " + "YIN" if yin_mode else "CHORD")
        stream.start_stream()
        
        while is_streaming:
            socketio.sleep(0.1)
        
        stream.stop_stream()
        stream.close()
    except Exception as e:
        print(f"Audio stream error: {e}")
    finally:
        p.terminate()
        is_streaming = False
        print("Audio stream stopped")

@app.route("/")
@app.route("/index")
def index():
    global yin_mode
    yin_mode = True
    stop_audio_stream()
    return render_template("index.html")

@app.route("/latencyTest")
def latency_test():
    global yin_mode
    yin_mode = True
    return render_template("latencyTest.html")

@app.route("/simpleReadPractice")
def simple_read_practice():
    global yin_mode
    yin_mode = True
    return render_template("simpleReadPractice.html")

@app.route("/chordReadPractice")
def chord_read_practice():
    global yin_mode
    yin_mode = False
    return render_template("chordReadPractice.html")

@app.route("/fullReadPractice")
def full_read_practice():
    global etude, yin_mode
    yin_mode = True
    etude.title = ""
    etude.focus = "air_column"
    etude.length = "2"
    etude.set_tempo(choice(["very_slow"]))
    etude.metre = "4/4"
    mode = "maj"
    key = "C"
    etude.set_key(key, mode)
    etude.ambitus = [0, 12]
    generator: Generator = Generator(etude)
    etude = generator.generate_etude()
    abc: str = convert_to_abc(etude)
    print("\n", abc, "\n")

    return render_template("fullReadPractice.html", abc=abc)

@socketio.on("start_audio_stream")
def start_audio_stream():
    global current_audio_task, is_streaming, yin_mode
    print("Started Audio Stream")
    if is_streaming:
        print("Audio Stream already running, Yin: " + "YIN" if yin_mode else "CHORD")
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
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, use_reloader=False)
