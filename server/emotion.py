import cv2
import numpy as np
import time
from datetime import datetime, timedelta

from ultralytics import YOLO
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
import global_vars
     
# load pretrained models
face_model = YOLO("yolov11n-face.pt")
emotion_model = Sequential()

emotion_model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
emotion_model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
emotion_model.add(Dropout(0.25))
emotion_model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
emotion_model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
emotion_model.add(MaxPooling2D(pool_size=(2, 2)))
emotion_model.add(Dropout(0.25))
emotion_model.add(Flatten())
emotion_model.add(Dense(1024, activation='relu'))
emotion_model.add(Dropout(0.5))
emotion_model.add(Dense(7, activation='softmax'))

emotion_model.load_weights("model.h5")
emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

# Data Structures
baseline_stats = {
    'negative_faces': [],
    'baseline_negative_avg': -1,
    'start_time': time.time()
}
BASELINE_DURATION = 10 # 1 minute for calibration

# rolling window avg
rolling_stats = {
     'rolling_negative_faces': []
}
WINDOW_SIZE = 10

def analyze_emotions():
    # webcam, 0 for default
    cap = cv2.VideoCapture(0) 
    # run emotion analysis
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Detect faces
        results = face_model(frame)

        for r in results:
            for box in r.boxes:
                # face bounding box
                x1, y1, x2, y2 = map(int, box.xyxy[0])  
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

                # crop face, convert to grayscale, resize, normalize, reshape
                face = frame[y1:y2, x1:x2]
                face_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                face_resized = cv2.resize(face_gray, (48, 48))
                face_normalized = face_resized / 255.0 
                face_reshaped = np.expand_dims(np.expand_dims(face_normalized, -1), 0)

                # prediction
                pred = emotion_model.predict(face_reshaped, verbose=False)
                max_val = int(np.argmax(pred))
                emotion = emotion_dict[max_val]
                # confidence = intensity of the emotion
                confidence = float(np.max(pred))

                # CALIBRATION
                if (time.time() - baseline_stats['start_time'] < BASELINE_DURATION):
                    if (max_val in {0, 1, 2, 5}):
                        baseline_stats['negative_faces'].append(confidence)
                    else:
                        baseline_stats['negative_faces'].append(0) # positive emotions
                elif (baseline_stats['baseline_negative_avg'] == -1):
                        print(baseline_stats['negative_faces'])
                        baseline_stats['baseline_negative_avg'] = np.nan_to_num(np.mean(baseline_stats['negative_faces']))
                        
                        print("CALIBRATED")
                else: 
                    # Compare rolling window of emotions against baseline
                    if (max_val in {0, 1, 2, 5}):
                        rolling_stats['rolling_negative_faces'].append(confidence)
                    else: 
                        baseline_stats['negative_faces'].append(0) # positive emotions
                    if len(rolling_stats['rolling_negative_faces']) > WINDOW_SIZE:
                        # map curr HH:MM to avg emotion sample
                        timestamp = datetime.now()
                        truncated_timestamp = timestamp.replace(microsecond=0)

                        sampled_mean = np.nan_to_num(np.mean(rolling_stats['rolling_negative_faces']))
                        std = np.std(baseline_stats['negative_faces'])

                        print(f"baseline: {baseline_stats['baseline_negative_avg']}, sampled mean: {sampled_mean}, std: {std}")

                        # TODO PANDAS
                        global_vars.confusion_df.loc[truncated_timestamp] = [sampled_mean]
                        print("-" * 80)
                        print(global_vars.confusion_df)
                        print("-" * 80)

                        rolling_stats['rolling_negative_faces'].clear()

                        if (sampled_mean > baseline_stats['baseline_negative_avg'] + 1.5 * std):
                            # spike detected, get lecture content from past 30 seconds
                            print("SPIKE DETECTED")

                            spike_timestamp = global_vars.pd.Timestamp(truncated_timestamp)
                            
                            start_time = spike_timestamp - timedelta(seconds=30)
                            end_time = spike_timestamp

                            # Get the relevant lecture content
                            relevant_lecture_content = global_vars.lecture_df.loc[start_time:end_time]
                            print(f"Relevant content: {relevant_lecture_content}")

                            # look up lecture content, trigger gpt pipeline, send data to unity
                cv2.putText(frame, emotion, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # display webcam
        cv2.imshow("Emotion Analyzer", frame)

        # q to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):  
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    analyze_emotions()