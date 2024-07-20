import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import keyboard
import time
from datetime import datetime
import assemblyai as aai
import pyaudio
import wave

def transcribe(fname):
    print("Just Hearing Your Answer.....")
    aai.settings.api_key = "5ec5fbbb505341458df9b9181c11b5d1"

    transcriber = aai.Transcriber()

    audio_url = fname

    config = aai.TranscriptionConfig(speaker_labels=True)

    transcript = transcriber.transcribe(audio_url, config)

    print(transcript.text)
    print("Done")


is_recording = False
recording_data = []
fs = 44100  # Sample rate

def callback(indata, frames, time, status):
    if is_recording:
        recording_data.append(indata.copy())

def start_recording():
    global is_recording, recording_data
    is_recording = True
    recording_data = []
    print("Recording started")

def stop_recording():
    global is_recording
    is_recording = False
    print("Recording stopped")
    filename = save_recording()
    return filename

def save_recording():
    global recording_data
    if recording_data:
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".wav"
        recording_data_np = np.concatenate(recording_data, axis=0)
        wav.write(filename, fs, recording_data_np)
        print(f"Recording saved as {filename}")
    return filename

def main():
    global is_recording

    # Create the audio input stream
    stream = sd.InputStream(callback=callback, channels=1, samplerate=fs)
    stream.start()

    print("Press and hold the space bar to start recording...")
    print("Release the space bar to stop recording.")

    while True:
        if keyboard.is_pressed('space'):
            if not is_recording:
                start_recording()
        else:
            if is_recording:
                fname = stop_recording()
                transcribe(fname)
        time.sleep(0.1)


if __name__ == "__main__":
    print("Welcome To Transcrier")
    main()