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
    max_num_hands=1,  #max one hand only
    min_detection_confidence=0.75, 
    min_tracking_confidence=0.75
)
mp_draw = mp.solutions.drawing_utils #use to draw lines

# Screen size
screen_width, screen_height = pyautogui.size() #computer screen width and height

# Webcam
camera = cv2.VideoCapture(0) #open webcam
camera.set(3, 640) #width
camera.set(4, 480) #height

# Cursor smoothing
plocX, plocY = 0, 0 #prev loc
clocX, clocY = 0, 0 #curr loc
smoothening = 7

# FPS
prev_time = 0 # calc fps

# Click cooldown
last_click_time = 0 #after one click wait for 0.4s
click_cooldown = 0.4

# Region margin
frame_margin = 80 #create a safe zone

while True:
    success, image = camera.read() #capture one frame
    if not success:
        continue

    image = cv2.flip(image, 1) #mirror effect
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #bgr to rgb
    result = hands.process(rgb_image) #detect hand landmarks
    hand_landmarks = result.multi_hand_landmarks #store hand points(detect and give location)

    h, w, _ = image.shape #height and width
    index_finger_pos, thumb_tip_pos, pinky_tip_pos = None, None, None 
    thumb_base_pos = None #var to store finger points

    if hand_landmarks:
        for handLms in hand_landmarks:
            mp_draw.draw_landmarks(image, handLms, mp_hands.HAND_CONNECTIONS) #draw 21 point on hand
#id which finger joint and lm actual coordintes
            for id, lm in enumerate(handLms.landmark): #loop through all 21 landmark points
                cx, cy = int(lm.x * w), int(lm.y * h) #lm.x and lm.y are x and y pos of that landmark
#(rel to 0 and 1)so mulitply by w and h to get actual
                if id == 8:   # Index tip
                    index_finger_pos = (cx, cy)
                    cv2.circle(image, (cx, cy), 10, (0, 255, 255), cv2.FILLED) #draw yellow circle

                    # Cursor mapping
                    x = max(frame_margin, min(w - frame_margin, cx)) #keep cursor inside safe zone
                    y = max(frame_margin, min(h - frame_margin, cy)) #x and y always stays in inner rect

                    screen_x = int((x - frame_margin) / (w - 2*frame_margin) * screen_width) #camera coordinate to screen coordinate
                    screen_y = int((y - frame_margin) / (h - 2*frame_margin) * screen_height) #normalize(where the cursor should go in screen)

                    clocX = plocX + (screen_x - plocX) / smoothening #moves cursor gradually
                    clocY = plocY + (screen_y - plocY) / smoothening

                    pyautogui.moveTo(clocX, clocY) #move to new coordinates
                    plocX, plocY = clocX, clocY #put curr to prev

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
                distance = math.hypot(ix - tx, iy - ty) #dist b/w index and thumb

                if distance < 35: #if thumb and index are <35 pixel far
                    curr_time = time.time()
                    if curr_time - last_click_time > click_cooldown: #check if enough time has passed since last click
                        pyautogui.click(button="left")
                        last_click_time = curr_time #last click time is now
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
                    pyautogui.scroll(40) #scroll units
                    cv2.putText(image, "Scroll Up", (10, 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                elif ty > by + 40:  # Thumb pointing down
                    pyautogui.scroll(-40)
                    cv2.putText(image, "Scroll Down", (10, 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # -----------------------------
    # FPS display how many times per second your code detects hand landmarks, maps gestures
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
