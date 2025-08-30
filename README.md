# 🖱️ AirMouse – AI Powered Hand Gesture Controlled Virtual Mouse  

---

## 📖 Overview  
**AirMouse** is a gesture-based virtual mouse that allows you to control your computer using only **hand gestures** captured by a webcam.  
It leverages **MediaPipe Hands (21 landmarks)**, **OpenCV**, and **PyAutoGUI** to map finger movements to mouse actions such as cursor control, clicks, and scrolling.  

The project demonstrates **real-time Human-Computer Interaction (HCI)** powered by computer vision with an average of ~30 FPS, gesture smoothing, and reduced noise for robust performance.  

---

## ✨ Features  

- 🎯 **Cursor Control** – Index finger tip controls the cursor position.  
- 👆 **Left Click** – Pinch **Index + Thumb**.  
- 🤏 **Right Click** – Pinch **Thumb + Pinky**.  
- 👍 **Scroll Up** – Thumb pointing upward.  
- 👎 **Scroll Down** – Thumb pointing downward.  
- 🔄 **Noise Reduction** – Distance thresholds, gesture smoothing, and cooldown logic reduce misfires by ~70%.  
- ⚡ **30 FPS Real-Time Performance** – Ensures smooth gesture tracking and reliable interaction.  
- 🖥️ **On-Screen Feedback** – FPS counter, scroll/click indicators, and branding for clear demos.  

---

## 📂 Tech Stack  

- [MediaPipe Hands](https://developers.google.com/mediapipe/solutions/hands) – detects 21 hand landmarks  
- [OpenCV](https://opencv.org/) – webcam feed & visualization  
- [PyAutoGUI](https://pyautogui.readthedocs.io/) – cursor, clicks & scrolling automation  
- **Python 3.8+**  

---

## 🛠️ Installation  

1. Clone this repository:  
   ```bash
   git clone https://github.com/yourusername/AirMouse.git
   cd AirMouse
2. pip install -r requirements.txt
3. python airmouse.py

<img width="1124" height="649" alt="image" src="https://github.com/user-attachments/assets/46710e6e-dd72-4672-9f6f-1a3f89053ea4" />
