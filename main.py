import cv2
import mediapipe as mp
import pyautogui
import time
import math
import os

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Initialize MediaPipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75
)
mp_draw = mp.solutions.drawing_utils

# Screen size
screen_width, screen_height = pyautogui.size()

# Webcam
camera = cv2.VideoCapture(0)
camera.set(3, 640)
camera.set(4, 480)

# Cursor smoothing
plocX, plocY = 0, 0
clocX, clocY = 0, 0
smoothening = 7

# FPS
prev_time = 0

# Click cooldown
last_click_time = 0
click_cooldown = 0.4

# Region margin
frame_margin = 80

while True:
    success, image = camera.read()
    if not success:
        continue

    image = cv2.flip(image, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_image)
    hand_landmarks = result.multi_hand_landmarks

    h, w, _ = image.shape
    index_finger_pos, thumb_tip_pos, pinky_tip_pos = None, None, None
    thumb_base_pos = None

    if hand_landmarks:
        for handLms in hand_landmarks:
            mp_draw.draw_landmarks(image, handLms, mp_hands.HAND_CONNECTIONS)

            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)

                if id == 8:   # Index tip
                    index_finger_pos = (cx, cy)
                    cv2.circle(image, (cx, cy), 10, (0, 255, 255), cv2.FILLED)

                    # Cursor mapping
                    x = max(frame_margin, min(w - frame_margin, cx))
                    y = max(frame_margin, min(h - frame_margin, cy))

                    screen_x = int((x - frame_margin) / (w - 2*frame_margin) * screen_width)
                    screen_y = int((y - frame_margin) / (h - 2*frame_margin) * screen_height)

                    clocX = plocX + (screen_x - plocX) / smoothening
                    clocY = plocY + (screen_y - plocY) / smoothening

                    pyautogui.moveTo(clocX, clocY)
                    plocX, plocY = clocX, clocY

                if id == 4:   # Thumb tip
                    thumb_tip_pos = (cx, cy)

                if id == 2:   # Thumb base
                    thumb_base_pos = (cx, cy)

                if id == 20:  # Pinky tip
                    pinky_tip_pos = (cx, cy)

            # -----------------------------
            # Gesture Priority
            # -----------------------------
            clicked = False

            # 1. Left Click (Index + Thumb pinch)
            if index_finger_pos and thumb_tip_pos:
                ix, iy = index_finger_pos
                tx, ty = thumb_tip_pos
                distance = math.hypot(ix - tx, iy - ty)

                if distance < 35:
                    curr_time = time.time()
                    if curr_time - last_click_time > click_cooldown:
                        pyautogui.click(button="left")
                        last_click_time = curr_time
                        clicked = True
                        cv2.putText(image, "Left Click", (10, 120),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # 2. Right Click (Thumb + Pinky pinch)
            if not clicked and thumb_tip_pos and pinky_tip_pos:
                tx, ty = thumb_tip_pos
                px, py = pinky_tip_pos
                distance = math.hypot(tx - px, ty - py)

                if distance < 40:  # slightly relaxed threshold
                    curr_time = time.time()
                    if curr_time - last_click_time > click_cooldown:
                        pyautogui.click(button="right")
                        last_click_time = curr_time
                        clicked = True
                        cv2.putText(image, "Right Click", (10, 150),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

            # 3. Scroll (Thumb Up / Down, only if no click happened)
            if not clicked and thumb_tip_pos and thumb_base_pos:
                tx, ty = thumb_tip_pos
                bx, by = thumb_base_pos

                if ty < by - 40:  # Thumb pointing up
                    pyautogui.scroll(40)
                    cv2.putText(image, "Scroll Up", (10, 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                elif ty > by + 40:  # Thumb pointing down
                    pyautogui.scroll(-40)
                    cv2.putText(image, "Scroll Down", (10, 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # -----------------------------
    # FPS display
    # -----------------------------
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time + 1e-5)
    prev_time = curr_time
    cv2.putText(image, f'FPS: {int(fps)}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # -----------------------------
    # Welcome text (Top-Right, Green)
    # -----------------------------
    text = "AirMouse by Shivane Kapoor"
    cv2.putText(image, text, (w - 350, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("AirMouse – Hand Gesture Mouse Control", image)

    if cv2.waitKey(1) == 27:  # ESC
        break

camera.release()
cv2.destroyAllWindows()
