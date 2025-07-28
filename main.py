import cv2
import mediapipe as mp
import pyttsx3
import time
from collections import deque, defaultdict

# MediaPipe Hand Setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Text-to-Speech Setup
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

# Webcam
cap = cv2.VideoCapture(0)

# Buffers & Timers
gesture_buffer = deque(maxlen=20)
last_spoken_time = 0
prev_word = ""
sentence = ""
gesture_timers = defaultdict(float)

# Emoji mapping function
def get_emoji(word):
    return {
        "Hello": "👋",
        "Bye": "🖐️",
        "Yes": "👍",
        "No": "☝🏻",
        "Thanks": "🤙🏻",
        "Wait": "⏳",
        "OK": "🖖🏻"
    }.get(word, "")

# Detect finger up/down
def get_finger_status(landmarks, is_right_hand):
    fingers = []
    # Thumb
    if is_right_hand:
        fingers.append(1 if landmarks[4].x > landmarks[3].x else 0)
    else:
        fingers.append(1 if landmarks[4].x < landmarks[3].x else 0)
    # Other fingers
    for tip in [8, 12, 16, 20]:
        fingers.append(1 if landmarks[tip].y < landmarks[tip - 2].y else 0)
    return fingers

# Open hand
def is_open_hand(f):
    return f.count(1) >= 4

# Closed fist
def is_closed_fist(f):
    return f.count(0) >= 4

# Motion-based gesture
def detect_motion_pattern(buffer):
    opens = sum(1 for b in buffer if b == "open")
    closes = sum(1 for b in buffer if b == "closed")
    return "Bye" if opens > 5 and closes > 5 else ""

# Static gestures
def detect_static_gesture(f, landmarks):
    if f == [0, 1, 1, 1, 1]:
        return "Hello"
    if f == [1, 0, 0, 0, 0] and landmarks[4].y < landmarks[3].y:
        return "Yes"
    if f == [0, 1, 0, 0, 0]:
        return "No"
    if f == [1, 0, 0, 0, 1]:
        return "Thanks"
    if f == [0, 0, 0, 0, 0]:
        return "Wait"

    # OK Gesture (Vulcan salute)
    mid_tip = landmarks[12]
    ring_tip = landmarks[16]
    gap = abs(mid_tip.x - ring_tip.x)
    if f == [1, 1, 1, 1, 1] and gap > 0.07:
        return "OK"

    return ""

# Main Loop
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    word = ""
    current_time = time.time()

    if result.multi_hand_landmarks:
        for i, handLms in enumerate(result.multi_hand_landmarks):
            hand_label = result.multi_handedness[i].classification[0].label
            is_right_hand = True if hand_label == "Right" else False

            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            finger_status = get_finger_status(handLms.landmark, is_right_hand)

            static_word = detect_static_gesture(finger_status, handLms.landmark)

            if is_open_hand(finger_status):
                gesture_buffer.append("open")
            elif is_closed_fist(finger_status):
                gesture_buffer.append("closed")

            motion_word = detect_motion_pattern(gesture_buffer)

            detected_word = motion_word if motion_word else static_word

            if detected_word:
                if gesture_timers[detected_word] == 0:
                    gesture_timers[detected_word] = current_time
                elif current_time - gesture_timers[detected_word] >= 2:
                    word = detected_word
            else:
                for key in gesture_timers:
                    gesture_timers[key] = 0

            if word:
                gesture_buffer.clear()
                gesture_timers.clear()
                break

    if word and word != prev_word and (time.time() - last_spoken_time > 1.5):
        print("Detected:", word)
        engine.say(word)
        engine.runAndWait()
        prev_word = word
        last_spoken_time = time.time()
        sentence += word + " "

    # Show emoji + word
    emoji = get_emoji(word)
    if emoji:
        cv2.putText(img, f"{emoji} {word}", (w - 250, 60),
                    cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 255, 255), 3)

    # Show sentence
    cv2.rectangle(img, (10, h - 60), (w - 10, h - 20), (50, 50, 50), -1)
    cv2.putText(img, f"Sentence: {sentence}", (20, h - 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("Sign Language Interpreter", img)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('c'):
        sentence = ""

cap.release()
cv2.destroyAllWindows()