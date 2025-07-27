import io
import base64
import cv2
import numpy as np
import pickle
import mediapipe as mp
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8,
)

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json.get("image", "")
    if not data.startswith("data:image"):
        return jsonify({"letter": ""})
    header, b64 = data.split(",", 1)
    img_bytes = base64.b64decode(b64)
    img_arr = np.frombuffer(img_bytes, dtype=np.uint8)
    frame = cv2.imdecode(img_arr, flags=cv2.IMREAD_COLOR)
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    letter = ""
    if results.multi_hand_landmarks:
        data_aux = []
        H, W, _ = frame.shape
        for hand_landmarks in results.multi_hand_landmarks:
            xs, ys = [], []
            for lm in hand_landmarks.landmark:
                xs.append(lm.x)
                ys.append(lm.y)
                data_aux.extend([lm.x, lm.y])

        X = np.array(data_aux[:42]).reshape(1, -1)  
        pred = model.predict(X)[0]

        labels = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ ")
        letter = pred if isinstance(pred, str) else labels[pred]

    return jsonify({"letter": letter})


if __name__ == "__main__":
    app.run(debug=True)
