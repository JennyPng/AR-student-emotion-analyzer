# AR-student-emotion-analyzer
Understanding where students struggle is crucial in providing a good educational experience,
yet many students suffer in silence, making it difficult for instructors to adjust.

We propose a real-time system that integrates emotion classification, live speech-to-text transcription, and augmented reality to provide instructors with immediate feedback during live lectures when students are confused. 

## implementation
<img src="VR Diagram.png" alt="pipeline diagram"></img>
<img src="sad.png" width=400em alt="pipeline diagram"></img>
<img src="sc.png" width=400em alt="pipeline diagram"></img>
The computer vision pipeline runs YOLOv11 to detect faces, and a CNN to constantly predict
emotions of all students. A baseline average of negative emotions is calibrated at the beginning of the lecture.
When a spike of 1.5 standard deviations above the baseline is detected, we consider students to be particularly confused. 

The speech-to-text pipeline is constantly recording and transcribing the lecture with Faster-Whisper. Both the emotion and speech
data is stored indexed by timestamp. When there is a spike in confusion, the corresponding chunk of lecture transcript
is retrieved and passed with a prompt to GPT to determine which specific topics in the lecture may be what is confusing.
The generated response is then streamed to the Unity application to be displayed to the instructor, providing live feedback
during teaching.

## server setup
`pip install -r ./requirements.txt`

Start server:
`python ./speech_analysis`

## unity setup
- Set up ngrok domain and change serverUrl in SocketManager.cs
- Run and build Unity app to Quest headset

## resources + references
- YOLO for face detection: https://github.com/akanametov/yolo-face?tab=readme-ov-file
- Pre-trained emotion detection model: https://github.com/atulapra/Emotion-detection
- Live transcription with Whisper: https://github.com/gaborvecsei/whisper-live-transcription
- Unity UI tutorial: https://www.youtube.com/watch?v=XOc71-Og0Kg
