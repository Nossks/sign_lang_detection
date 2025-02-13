import os
import mediapipe as mp
import cv2 as cv

mp_hands=mp.solutions.hands
mp_drawing=mp.solutions.drawing_utils
mp_drawing_styles=mp.solutions.drawing_styles

hands=mp_hands.Hands()

webcam=cv.VideoCapture(1)

while True:
    ret,frame=webcam.read()
    x_=[]
    y_=[]
    h,w,_=frame.shape

    img_rgb=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
    results=hands.process(img_rgb)
    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,  # image to draw
                hand_landmarks,  # model output
                mp_hands.HAND_CONNECTIONS,  # hand connections
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
        
        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x_.append(hand_landmarks.landmark[i].x)
                y_.append(hand_landmarks.landmark[i].y)

        x1=int(min(x_)*w)-10
        y1=int(min(y_)*h)-10
        x2=int(max(x_)*w)-10
        y2=int(max(y_)*h)-10

        cv.rectangle(frame,(x1,y1),(x2,y2),(0,0,0),2)

    cv.imshow("webcam",frame)
    if cv.waitKey(10) & 0xFF==ord("q"):
        break

webcam.release()
cv.destroyAllWindows()
