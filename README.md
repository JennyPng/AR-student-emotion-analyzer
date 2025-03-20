# AR-student-emotion-analyzer
Understanding where students struggle is crucial in providing a good educational experience,
yet many students suffer in silence, making it difficult for instructors to adjust.

We propose a context-aware AR system that utilizes real-time computer vision to analyze student engagement
and understanding, dynamically providing suggestions on how to adjust the teaching pace and
focus areas.

## implementation
<img src="VR Diagram.png" alt="pipeline diagram"></img>

## server setup
`pip install -r ./requirements.txt`

## unity setup
- Set up Meta Quest settings
- Set up ngrok domain and change serverUrl in SocketManager.cs

## resources + references
- YOLO for face detection: https://github.com/akanametov/yolo-face?tab=readme-ov-file
- Pre-trained emotion detection model: https://github.com/atulapra/Emotion-detection
- Live transcription with Whisper: https://github.com/gaborvecsei/whisper-live-transcription
- Unity UI tutorial: https://www.youtube.com/watch?v=XOc71-Og0Kg
