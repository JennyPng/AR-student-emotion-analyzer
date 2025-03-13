import whisper
import pyaudio
import numpy as np
import wave

model = whisper.load_model("base") 

def record_audio(filename="lecture.wav", duration=10, sample_rate=16000):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=1024)
    
    frames = []
    print("Recording...")
    
    for _ in range(0, int(sample_rate / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)
    
    print("Finished recording.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

def transcribe_audio():
    result = model.transcribe("lecture.wav")
    print("Transcription:", result["text"])
    return result["text"]

# Run the pipeline
record_audio(duration=5) 
transcription = transcribe_audio()
