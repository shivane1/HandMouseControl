import cv2
import mediapipe as mp
import pyautogui
import time
import math

# Initialize MediaPipe hand detector
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Get screen size
screen_width, screen_height = pyautogui.size()

# Capture video from webcam
camera = cv2.VideoCapture(0)

# For smoothing
plocX, plocY = 0, 0
clocX, clocY = 0, 0
smoothening = 5

# FPS counter
prev_time = 0

# Click cooldown control
click_cooldown = 0.5  # seconds
last_click_time = 0

while True:
    success, image = camera.read()
    if not success:
        continue

    image = cv2.flip(image, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_image)
    hand_landmarks = result.multi_hand_landmarks

    if hand_landmarks:
        for handLms in hand_landmarks:
            mp_draw.draw_landmarks(image, handLms, mp_hands.HAND_CONNECTIONS)

            h, w, _ = image.shape
            index_finger_pos = None
            thumb_tip_pos = None

            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)

                if id == 8:  # Index fingertip
                    index_finger_pos = (cx, cy)

                    # Draw index finger point
                    cv2.circle(image, (cx, cy), 15, (0, 255, 255), cv2.FILLED)

                    # Map to screen coordinates
                    screen_x = int(screen_width * lm.x)
                    screen_y = int(screen_height * lm.y)

                    clocX = plocX + (screen_x - plocX) / smoothening
                    clocY = plocY + (screen_y - plocY) / smoothening

                    pyautogui.moveTo(clocX, clocY)
                    plocX, plocY = clocX, clocY

                if id == 4:  # Thumb tip
                    thumb_tip_pos = (cx, cy)

            # Click detection (pinch)
            if index_finger_pos and thumb_tip_pos:
                ix, iy = index_finger_pos
                tx, ty = thumb_tip_pos
                distance = math.hypot(ix - tx, iy - ty)

                # Threshold for click gesture (tweak if needed)
                if distance < 40:
                    curr_time = time.time()
                    if curr_time - last_click_time > click_cooldown:
                        pyautogui.click()
                        last_click_time = curr_time
                        # Feedback: red circle for click
                        cv2.circle(image, index_finger_pos, 20, (0, 0, 255), cv2.FILLED)

    # FPS display
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time + 1e-5)
    prev_time = curr_time

    cv2.putText(image, f'FPS: {int(fps)}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Show the webcam feed
    cv2.imshow("Hand Tracking - Mouse Control", image)

    # Exit on ESC key
    if cv2.waitKey(1) == 27:
        break

# Cleanup
camera.release()
cv2.destroyAllWindows()
