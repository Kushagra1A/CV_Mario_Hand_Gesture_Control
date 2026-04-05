import cv2
import mediapipe as mp
from directkey import ReleaseKey, PressKey, W, A, S, D

mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Key states
w_down = False
a_down = False
d_down = False

video = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2) as hands:
    while True:
        success, image = video.read()
        if not success: break

        image = cv2.flip(image, 1)
        h, w, _ = image.shape
        
        # Draw Zones for visual feedback
        # Right zone (D), Left zone (A), Center is deadzone
        cv2.line(image, (int(w * 0.4), 0), (int(w * 0.4), h), (255, 255, 255), 1)
        cv2.line(image, (int(w * 0.6), 0), (int(w * 0.6), h), (255, 255, 255), 1)

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)
        
        current_w = False
        current_a = False
        current_d = False

        if results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                # Identify Hand
                label = results.multi_handedness[idx].classification[0].label
                lm = hand_landmarks.landmark
                mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # --- JUMP LOGIC (Left Hand) ---
                # Sometimes MediaPipe flips labels, so we check position too
                if label == "Left":
                    if lm[8].y < lm[6].y: # Index finger up
                        current_w = True

                # --- MOVEMENT LOGIC (Right Hand) ---
                if label == "Right":
                    wrist_x = lm[0].x
                    # If wrist is to the left of 40% of screen -> Move Left (A)
                    if wrist_x < 0.40: 
                        current_a = True
                    # If wrist is to the right of 60% of screen -> Move Right (D)
                    elif wrist_x > 0.60:
                        current_d = True

        # --- KEY ACTUATION ---
        # Handle A (Left)
        if current_a and not a_down:
            PressKey(A)
            a_down = True
        elif not current_a and a_down:
            ReleaseKey(A)
            a_down = False

        # Handle D (Right)
        if current_d and not d_down:
            PressKey(D)
            d_down = True
        elif not current_d and d_down:
            ReleaseKey(D)
            d_down = False

        # Handle W (Jump)
        if current_w and not w_down:
            PressKey(W)
            w_down = True
        elif not current_w and w_down:
            ReleaseKey(W)
            w_down = False

        # On-screen Status
        status = f"JUMP: {w_down} | LEFT: {a_down} | RIGHT: {d_down}"
        cv2.putText(image, status, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow("Mario Controller", image)
        if cv2.waitKey(1) & 0xFF == ord('e'):
            break

# Emergency release
for k in [W, A, D]: ReleaseKey(k)
video.release()
cv2.destroyAllWindows()