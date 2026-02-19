import cv2
import mediapipe as mp
import csv
import os

# 1. Setup MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# 2. Setup Camera
cap = cv2.VideoCapture(0)

# CHANGE THIS LABEL (0-8) for each gesture you record!
current_label = 9
file_name = 'hand_data.csv'

print(f"Recording for Label {current_label}. Press 's' to save, 'q' to quit.")

while cap.isOpened():
    success, image = cap.read()
    if not success: break

    image = cv2.flip(image, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_image)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Press 's' to save the current frame's landmarks
            if cv2.waitKey(1) & 0xFF == ord('s'):
                data_row = [current_label]
                for lm in hand_landmarks.landmark:
                    # We save x and y coordinates
                    data_row.extend([lm.x, lm.y])
                
                with open(file_name, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(data_row)
                print(f"Saved frame for label {current_label}")

    cv2.imshow('Hand Data Collector', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()