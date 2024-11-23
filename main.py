from flask import Flask, Response, render_template
import threading
import time
import pyaudio
import numpy as np
from yinPitchDetection import *

app = Flask(__name__)
detected_note = None

def audio_stream():
  global detected_note
  p = pyaudio.PyAudio()
  
  stream = p.open(
    format=pyaudio.paFloat32,
    channels=1,
    rate=SAMPLE_RATE,
    input=True,
    frames_per_buffer=CHUNK,
  )
  while True:
    data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.float32)
    frequency = get_pitch_yin(data, SAMPLE_RATE)
    if frequency:
      detected_note = find_nearest_note(frequency)
  stream.stop_stream()
  stream.close()
  p.terminate()

@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/simpleReadPractice')
def simpleReadPractice():
  return render_template('simpleReadPractice.html')

@app.route('/stream_notes')
def stream_notes():
  def generate():
    global detected_note
    last_note = None
    while True:
      if detected_note and detected_note != last_note:
        last_note = detected_note
        yield f"data: {detected_note}\n\n"
      time.sleep(0.1)
  return Response(generate(), content_type='text/event-stream')

if __name__ == "__main__":
  thread = threading.Thread(target=audio_stream)
  thread.daemon = True
  thread.start()
  app.run(host="0.0.0.0", port=8000)
