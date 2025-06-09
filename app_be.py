import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
import os
import json
from vosk import Model, KaldiRecognizer

app = Flask(__name__, static_folder="static")
socketio = SocketIO(app, cors_allowed_origins="*")

model = Model("vosk-model-small-en-us-0.15")
rec = KaldiRecognizer(model, 16000)

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@socketio.on("audio")
def handle_audio(data):
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        socketio.emit("transcript", result)
    else:
        partial = json.loads(rec.PartialResult())
        socketio.emit("transcript", partial)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
