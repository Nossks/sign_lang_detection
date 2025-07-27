const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const predictedEl = document.getElementById("predicted");
const currentWordEl = document.getElementById("currentWord");
const sentenceEl = document.getElementById("sentence");
const backspaceBtn = document.getElementById("backspace");
const clearAllBtn = document.getElementById("clearAll");
const speakBtn = document.getElementById("speak");

let buffer = [];
const BUFFER_SIZE = 10;
const THRESHOLD = 7;
let lastStable = "";
let currentWord = "";
let sentence = [];

navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => { video.srcObject = stream; })
  .catch(console.error);

setInterval(async () => {
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  const dataUrl = canvas.toDataURL("image/png");
  
  const res = await fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ image: dataUrl })
  });
  const { letter } = await res.json();
  handlePrediction(letter);
}, 300);

function handlePrediction(letter) {
  predictedEl.textContent = letter === " " ? "␣" : letter;
  
  buffer.push(letter);
  if (buffer.length > BUFFER_SIZE) buffer.shift();
  
  const counts = buffer.reduce((acc, l) => {
    acc[l] = (acc[l] || 0) + 1;
    return acc;
  }, {});
  const [cand, cnt] = Object.entries(counts).sort((a,b) => b[1]-a[1])[0];
  
  if (cnt >= THRESHOLD && cand !== lastStable) {
    lastStable = cand;
    if (cand === "Space") {
      if (currentWord) {
        sentence.push(currentWord);
        currentWord = "";
      }
    } else {
      currentWord += cand;
    }
    updateDisplay();
  }
}

function updateDisplay() {
  currentWordEl.textContent = currentWord;
  sentenceEl.textContent = sentence.join(" ");
}

backspaceBtn.onclick = () => {
  currentWord = currentWord.slice(0, -1);
  updateDisplay();
};

clearAllBtn.onclick = () => {
  currentWord = "";
  sentence = [];
  updateDisplay();
};

speakBtn.onclick = () => {
  const text = sentence.join(" ");
  if (text) {
    const utter = new SpeechSynthesisUtterance(text);
    speechSynthesis.speak(utter);
  }
};
