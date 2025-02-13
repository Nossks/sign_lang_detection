import streamlit as st
import mediapipe as mp
import cv2 as cv
import pickle
import numpy as np

# Load model
with open("rolex.pkl", "rb") as f:
    model = pickle.load(f)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)

# Streamlit UI
st.title("Live Sign Language Detection")
st.write("Turn on your webcam and make signs to detect them.")

# OpenCV Webcam Feed
webcam = cv.VideoCapture(0)  # Change to 1 if using an external webcam
frame_window = st.image([])  # Placeholder for video frame

while webcam.isOpened():
    ret, frame = webcam.read()
    if not ret:
        st.warning("Failed to grab frame. Check webcam connection.")
        break

    data_aux, x_, y_ = [], [], []
    h, w, _ = frame.shape

    img_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )

            for i in range(len(hand_landmarks.landmark)):
                x, y = hand_landmarks.landmark[i].x, hand_landmarks.landmark[i].y
                data_aux.extend([x, y])
                x_.append(x)
                y_.append(y)

        x1, y1 = int(min(x_) * w) - 10, int(min(y_) * h) - 10
        x2, y2 = int(max(x_) * w) + 10, int(max(y_) * h) + 10

        prediction = model.predict([np.array(data_aux)[:42]])[0]
        cv.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 3)
        cv.putText(frame, prediction, (x1, y1 - 10), cv.FONT_HERSHEY_COMPLEX, 3, (0, 0, 0), 5)

    frame_window.image(frame, channels="BGR")

webcam.release()
cv.destroyAllWindows()
