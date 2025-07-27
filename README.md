# Sign Language Detection 
A real-time ASL-to-text web app that uses live webcam input to detect ASL alphabet signs and builds words and sentences based on your hand gestures. Includes a Flask backend for prediction and a responsive frontend with video stream, prediction logic, word handling, and text-to-speech.

## Features  
**Live ASL Recognition** via webcam.  
**Prediction Stability Buffer** to ensure consistent output.  
**Current Word + Sentence Builder** using space gestures.  
**Text-to-Speech Support** for spoken output.  
**Backspace & Clear All Controls** for easy correction.  
**Static ASL Symbol Guide** for user reference.  
**Collage Generator Script** for generating a labeled symbol grid from images.

## Tech Stack  
**Backend**: Python, Flask, MediaPipe, pickle  
**Frontend**: HTML, CSS, Vanilla JavaScript  
**ML Model**: Random Forest classifier saved as `model.pkl`  
**Utilities**: hand_landmarks.py

## Setup Instructions  

### 1. Clone the Repository  
```bash  
git clone https://github.com/Nossks/sign_lang_detection  
cd sign_lang_detection  
```  

### 2. Set Up Virtual Environment  
```bash  
python3 -m venv venv  
source venv/bin/activate  
```  

### 3. Install Dependencies  
```bash  
pip install -r requirements.txt  
```  

### 4. Add Your Model  
Place your trained model in the project root as:  
`model.pkl`  

### 5. Symbol Images  
Add a collage of all symbols  

---

## Running the App  
```bash  
python app.py  
```  

Then open your browser and visit:  
`http://127.0.0.1:5000/`

## How It Works  
**Webcam Feed** captures your hand gesture.  
**Model Prediction** detects the character (A–Z or space).  
**Buffering Logic** ensures the character is consistent across multiple frames.  
**"Space" Gesture** finalizes the current word and adds it to the sentence.  
**Backspace** removes a letter from the current word.  
**Clear All** resets the entire sentence.  
**Speak** uses the browser's speech synthesis to read out the sentence.

## Future Enhancements  
Implement for gesture rather than just static symbols.  
Use a deep learning model like LSTM RNN for gestures instead of cpu based ml algo's.
