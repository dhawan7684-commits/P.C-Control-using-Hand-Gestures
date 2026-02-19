import pyautogui
pyautogui.FAILSAFE = False
import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import time

# 1. Load the brain you just trained
model = tf.keras.models.load_model('gesture_model.h5')

# 2. Setup MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)

# The actions mapped to your labels
actions = ["Idle", "Screenshot", "Start Menu", "Scroll Down", "Scroll Up", 
           "Vol Up", "Vol Down", "Settings", "Minimize", "Chrome"]

print("AI Control Active! Show your hand...")

while cap.isOpened():
    success, image = cap.read()
    if not success: break

    image = cv2.flip(image, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_image)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Extract coordinates for the model
            coords = []
            for lm in hand_landmarks.landmark:
                coords.extend([lm.x, lm.y])
            
            # Predict!
            prediction = model.predict(np.array([coords]), verbose=0)
            class_id = np.argmax(prediction)
            confidence = np.max(prediction)

            if confidence > 0.8: # Only act if the AI is 80% sure
                gesture_name = actions[class_id]
                cv2.putText(image, f"{gesture_name} ({int(confidence*100)}%)", (10, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # --- TRIGGER ACTIONS ---
                if gesture_name == "Idle":
                    pass
                elif gesture_name == "Screenshot":
                    pyautogui.hotkey('win', 'prtscr')
                    time.sleep(1)
                elif gesture_name == "Start Menu":
                    time.sleep(0.2)
                    pyautogui.press('win')
                elif gesture_name == "Scroll Down":
                    pyautogui.scroll(-300)
                elif gesture_name == "Scroll Up":
                    pyautogui.scroll(300)
                elif gesture_name == "Vol Up":
                    pyautogui.press('volumeup')
                elif gesture_name == "Vol Down":
                    pyautogui.press('volumedown')
                elif gesture_name == "Settings":
                    pyautogui.hotkey('win', 'i')
                elif gesture_name == "Chrome":
                    pyautogui.press('win')
                    time.sleep(0.3)
                    pyautogui.write('chrome')
                    time.sleep(0.3)
                    pyautogui.press('enter')
                    time.sleep(2)
                elif gesture_name == "Minimize":
                    pyautogui.hotkey('win', 'd')
    cv2.imshow('AI Gesture Control', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()