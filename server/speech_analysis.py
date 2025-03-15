import pyaudio
import wave
import numpy as np
import whisper
from faster_whisper import WhisperModel
import queue
import datetime
import re
import threading
import global_vars

import emotion

# AUDIO SETTINGS
MAX_AUDIO_QUEUE = 7 # max length audio data to process together
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
rate = 16000  # samples per second to record
# seconds = 3
filename = "output.wav"

# Whisper settings
WHISPER_LANGUAGE = "en"
WHISPER_THREADS = 4

# hold 1-second audio chunks for processing
audio_queue = queue.Queue()
limited_queue = queue.Queue(maxsize=MAX_AUDIO_QUEUE)

whisper = WhisperModel("base", device="cpu", compute_type="int8", cpu_threads=WHISPER_THREADS, download_root="./models")

def get_audio():
    # Record audio and place in queue 
    print('Recording')
    p = pyaudio.PyAudio() 

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=rate,
                    frames_per_buffer=chunk,
                    input=True)

    print("-" * 50)
    print("Microphone initialized")
    print("-" * 50)

    while True:
        audio_data = b""
        for _ in range(1):
            curr_chunk = stream.read(rate) # length of audio data to read
            audio_data += curr_chunk
        audio_queue.put(audio_data)

def transcribe_audio():
    print("transcribing")
    # Get from queue and parse
    try:
        while True:
            if audio_queue.qsize() >= MAX_AUDIO_QUEUE: # if we have num seconds of audio, transcribe it and store it
                audio_to_process = b""
                qsize = audio_queue.qsize()
                for i in range(qsize):
                    audio_to_process += audio_queue.get()
                
                audio_array : np.ndarray = np.frombuffer(audio_to_process, np.int16).astype(np.float32) / 255.0
                
                segments, _ = whisper.transcribe(audio_array,
                                                    language=WHISPER_LANGUAGE,
                                                    beam_size=5,
                                                    vad_filter=True,
                                                    vad_parameters=dict(min_silence_duration_ms=1000))
                segments = [s.text for s in segments] 

                transcription = " ".join(segments)
                # remove non-speech, which is in () or []
                transcription = re.sub(r"\[.*\]", "", transcription)
                transcription = re.sub(r"\(.*\)", "", transcription)

                timestamp = datetime.datetime.now()
                truncated_timestamp = timestamp.replace(microsecond=0)

                global_vars.lecture_df.loc[truncated_timestamp] = [transcription]

                # for multithreading, signals that enqueued task was processed
                audio_queue.task_done()
    except KeyboardInterrupt:
        print("quitting transcribe")

if __name__ == "__main__":
    emotion_thread = threading.Thread(target=emotion.analyze_emotions)
    emotion_thread.start()

    audio_thread = threading.Thread(target=get_audio)
    audio_thread.start() 

    transcription_thread = threading.Thread(target=transcribe_audio)
    transcription_thread.start()
    
    try:
        audio_thread.join()
        transcription_thread.join()
        emotion_thread.join()
    except KeyboardInterrupt:
        print("Quitting")
        