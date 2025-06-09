import queue
import sounddevice as sd
import vosk
import sys
import json

# Load the Vosk model
model = vosk.Model("vosk-model-small-en-us-0.15")

# Queue for audio
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

samplerate = 16000

with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    print("🎙️ Speak now (Ctrl+C to stop)...\n")
    rec = vosk.KaldiRecognizer(model, samplerate)

    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            print("✅", result.get("text", ""))
        else:
            partial = json.loads(rec.PartialResult())
            if partial["partial"]:
                print("...", partial["partial"], end='\r')
