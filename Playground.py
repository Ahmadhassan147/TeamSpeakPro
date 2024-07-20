import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import keyboard
import time
from datetime import datetime
import assemblyai as aai
import pyaudio
import wave
import os
from together import Together


def genrate_part1():
    client = Together(api_key= "27b92a686e62fa3c74cb22729a1d0bc26e377cb64ac39d3694355f4c5a1b804f")

    stream = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3-70B-Instruct-Turbo",
        messages=[{"role": "user", "content": """Do not include any starting lines like "here's the question" or anything else.Provide me IELTS Part One of the speaking module with random questions. Provide only the questions, nothing else. Include two general lines like "What's your name?" and "What do you do?" followed by 7-8 random questions for Part One."""}],
        max_tokens=512,
        temperature=0.7,
        top_p=0.7,
        top_k=50,
        repetition_penalty=1,
        stop=["<|eot_id|>"],
        stream=True
    )
    # print(response.choices[0].message.content)
    with open("Question_for_part01.txt", "w") as file:
        for chunk in stream:            
            if hasattr(chunk.choices[0].delta, 'content'):
                content = chunk.choices[0].delta.content
                # print(content, end="", flush=True)
                file.write(content)




def transcribe(fname,question_statement):
    print("Transcribing.....")
    aai.settings.api_key = "5ec5fbbb505341458df9b9181c11b5d1"

    transcriber = aai.Transcriber()

    audio_url = fname

    config = aai.TranscriptionConfig(speaker_labels=True)

    transcript = transcriber.transcribe(audio_url, config)
    # print(transcript.text)
    # print("Done")
    R_filename = "Answers_part01.txt"
    save_text_to_file(R_filename, transcript.text,question_statement)
    return

def save_text_to_file(filename, text , question_statement):
    with open(filename, 'a') as file:
        file.write(f"Question: {question_statement}\n")
        file.write(f"Answer: {text}")
    return

    
# Define global variables

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

def show_questions_p1(fname_to_open):
    genrate_part1()
    with open(fname_to_open, 'r') as file:
        # Read the first line
        lines = file.readlines()
        line_count = len(lines)
        for i in range(line_count):
            first_line = lines[i] if lines else "File is empty"
            print(f"Quesntion {i}: {first_line}")
            record(first_line)



def record(question_statement):
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
                transcribe(fname,question_statement)
                return
        time.sleep(0.1)

def main():
    print("Welcome To Ielts SpeakPro")
    print("Here you can practice for your Ielts Speaking Module and Improve your Speaking")
    input("Press Enter to continue with First part of ielts...")
    instructions = """
        Instructions for IELTS Speaking Part One:
        ----------------------------------------
        1. Read the question displayed.
        2. After seeing the question, press and hold the space bar to start your answer.
        3. Release the space bar when you finish answering.
        """
    print(instructions)
    input("Press Enter to Start part 01.....")
    qfname = "Question_for_part01.txt"
    show_questions_p1(qfname)



if __name__ == "__main__":
    main()

