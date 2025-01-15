from flask_socketio import SocketIO


def init():
    global current_audio_task, is_streaming, yin_mode, socketio, open_stream
    current_audio_task = None
    is_streaming = False
    yin_mode = False
    socketio = SocketIO(async_mode='threading', ping_timeout=1, ping_interval=1)
    open_stream = True
