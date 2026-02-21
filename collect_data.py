import cv2, mediapipe as mp, csv, sys, time

gesture_name = sys.argv[1] if len(sys.argv) > 1 else "Unknown"
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
cap = cv2.VideoCapture(0)
start_time = time.time()
duration = 20 

with open('hand_data.csv', mode='a', newline='') as f:
    writer = csv.writer(f)
    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if not ret: break
        
        frame = cv2.flip(frame, 1) # Mirror image
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        if results.multi_hand_landmarks:
            lm_list = []
            for lm in results.multi_hand_landmarks[0].landmark:
                lm_list.extend([lm.x, lm.y])
            lm_list.append(gesture_name)
            writer.writerow(lm_list)
            
        remaining = int(duration - (time.time() - start_time))
        cv2.putText(frame, f"Recording {gesture_name}: {remaining}s", (10, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("Data Collection", frame)
        cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()