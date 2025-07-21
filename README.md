# 🖱️ AirMouse – Control Your Mouse with Hand Gestures

**AirMouse** lets you control your computer's mouse using only your hand gestures via webcam.  
Built with **OpenCV**, **MediaPipe**, and **PyAutoGUI**, it tracks your index finger in real time to move the cursor — and even lets you **click** by pinching your fingers together!

---

## 🚀 Features

- ✅ Real-time hand tracking using MediaPipe
- ✅ Smooth mouse movement based on index finger tip
- ✅ Click using a **pinch gesture** (thumb and index finger tip close together)
- ✅ On-screen visual indicators for cursor and click
- ✅ FPS counter and responsive UI
- ✅ Easy to set up, works on any screen size

---

## 🖥️ How It Works

- **Move the Cursor**:  
  Simply raise your hand to the webcam and move your **index finger** — the mouse cursor will follow.

- **Click**:  
  Bring your **thumb and index finger tips close together** (like a "pinch") — this triggers a **left mouse click**.  
  ![click gesture](https://user-images.githubusercontent.com/355bbd67/attachments/Screenshot-click-gesture.png)  
  A red circle appears on-screen to indicate a successful click.

---

## 📸 Demo

<img width="1919" height="1030" alt="AirMouse Demo Screenshot" src="https://github.com/user-attachments/assets/355bbd67-42fe-4b5b-ae45-c1caab970a75" />

> ✋ Raise your hand > 🖱️ Move your index finger > 👌 Pinch to click  
> Press `ESC` to exit.

---

## 📦 Requirements

Install dependencies using:

```bash
pip install opencv-python mediapipe pyautogui
