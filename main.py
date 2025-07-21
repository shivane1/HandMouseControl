import cv2
import mediapipe as mp
import pyautogui
import time

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
smoothening = 5  # You can adjust this (4–10) based on your comfort

# FPS counter
prev_time = 0

while True:
    success, image = camera.read()
    if not success:
        continue

    # Flip and convert to RGB
    image = cv2.flip(image, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process hand landmarks
    result = hands.process(rgb_image)
    hand_landmarks = result.multi_hand_landmarks

    if hand_landmarks:
        for handLms in hand_landmarks:
            mp_draw.draw_landmarks(image, handLms, mp_hands.HAND_CONNECTIONS)

            for id, lm in enumerate(handLms.landmark):
                h, w, _ = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                # Index finger tip (landmark id 8)
                if id == 8:
                    # Draw marker on fingertip
                    cv2.circle(image, (cx, cy), 15, (0, 255, 255), cv2.FILLED)

                    # Map to screen coordinates
                    screen_x = int(screen_width * lm.x)
                    screen_y = int(screen_height * lm.y)

                    # Smooth mouse movement (floating point approach)
                    clocX = plocX + (screen_x - plocX) / smoothening
                    clocY = plocY + (screen_y - plocY) / smoothening

                    # Move the mouse
                    pyautogui.moveTo(clocX, clocY)
                    plocX, plocY = clocX, clocY

                    # Show target mouse location on the camera feed
                    cv2.putText(image, f'Mouse: ({int(clocX)}, {int(clocY)})', (10, 70),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Show FPS
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time + 1e-5)
    prev_time = curr_time

    cv2.putText(image, f'FPS: {int(fps)}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Show webcam image
    cv2.imshow("Hand Tracking - Mouse Control", image)

    # Exit on ESC key
    if cv2.waitKey(1) == 27:
        break

# Cleanup
camera.release()
cv2.destroyAllWindows()
