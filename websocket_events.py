from audio_stream import audio_stream
import config


@config.socketio.on("start_audio_stream")
def start_audio_stream():
    
    print("Started Audio Stream")
    if config.is_streaming:
        print("Audio Stream already running: " + "YIN" if config.yin_mode else "Audio Stream already running: " + "CHORD")
        return
    
    config.is_streaming = True
    config.current_audio_task = config.socketio.start_background_task(target=audio_stream)

@config.socketio.on("stop_audio_stream")
def stop_audio_stream():
    config.is_streaming = False
    config.current_audio_task = None
    print("Stop audio stream requested")
