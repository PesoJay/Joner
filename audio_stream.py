import numpy as np
import pyaudio
import config
from chordDetection import find_notes_in_chord, get_note_frequencies, identify_chord
from utils import CHORD_CHUNK, SAMPLE_RATE, YIN_CHUNK, find_nearest_note
from yinPitchDetection import get_pitch_yin

def callback(in_data, frame_count, time_info, status):
    if not config.is_streaming:
        return (None, pyaudio.paComplete)
    
    if config.open_stream:
        data = np.frombuffer(in_data, dtype=np.float32)
        rms = np.sqrt(np.mean(np.square(data)))
        
        if rms > 0.01:
            if config.yin_mode:
                frequency = get_pitch_yin(data, SAMPLE_RATE)
                if frequency:
                    note = find_nearest_note(frequency)
                    if note: 
                        config.socketio.emit("note_detected", {"note": note}, namespace="/")
            else:
                frequencies = get_note_frequencies(data, SAMPLE_RATE)
                notes = find_notes_in_chord(frequencies)
                if notes:
                    chord = identify_chord(notes)
                    if chord:
                        config.socketio.emit("chord_detected", {"chord": chord}, namespace="/")
    
    return (in_data, pyaudio.paContinue)

def audio_stream():
    p = pyaudio.PyAudio()
    try:
        stream = p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=SAMPLE_RATE,
            input=True,
            frames_per_buffer= YIN_CHUNK if config.yin_mode else CHORD_CHUNK,
            stream_callback=callback,
            input_device_index=None
        )
        print("Mode: YIN" if config.yin_mode else "Mode: CHORD")
        stream.start_stream()
        
        while config.is_streaming:
            config.socketio.sleep(0.01)
        
        stream.stop_stream()
        stream.close()
    except Exception as e:
        print(f"Audio stream error: {e}")
    finally:
        p.terminate()
        config.is_streaming = False
        print("Audio stream stopped")