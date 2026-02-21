import cv2, mediapipe as mp, numpy as np, tensorflow as tf, pyautogui, pandas as pd, time, os, json
import google.generativeai as genai

# --- CONFIGURATION ---
GENAI_KEY = "AIzaSyCvydkaMYRIva7jR5AZ2vZbUi9az-93ncY"
genai.configure(api_key=GENAI_KEY)
llm = genai.GenerativeModel('gemini-pro')

# Load files
try:
    data = pd.read_csv('hand_data.csv', header=None)
    actions = sorted(data.iloc[:, -1].unique())
    model = tf.keras.models.load_model('gesture_model.h5')
    with open('intents.json', 'r') as f:
        intents = json.load(f)
except Exception as e:
    print(f"Error loading files: {e}")
    exit()

def execute_safe_action(json_str):
    try:
        # Clean potential markdown from LLM
        clean_json = json_str.replace('```json', '').replace('```', '').strip()
        res = json.loads(clean_json)
        cmd = res.get("action")
        target = res.get("target", "")

        if cmd == "hotkey":
            pyautogui.hotkey(*target.split('+'))
        elif cmd == "open":
            pyautogui.press('win'); time.sleep(0.3)
            pyautogui.write(target); time.sleep(0.5); pyautogui.press('enter')
        elif cmd == "type":
            pyautogui.write(target); pyautogui.press('enter')
        elif cmd == "press":
            pyautogui.press(target)
        print(f"Executed: {cmd} {target}")
    except Exception as e:
        print(f"Failed to execute LLM command: {e}")

def process_with_llm(gesture_name):
    user_intent = intents.get(gesture_name, "Do nothing")
    prompt = f"""
    The user did gesture '{gesture_name}'. Goal: '{user_intent}'.
    Return ONLY raw JSON. 
    If they want a screenshot, return: {{"action": "hotkey", "target": "win+prtscr"}}.
    If they want to open an app, return: {{"action": "open", "target": "appname"}}.
    """
    try:
        response = llm.generate_content(prompt)
        execute_safe_action(response.text)
    except Exception as e:
        print(f"LLM Error: {e}")

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
last_action_time = 0

while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    
    if time.time() - last_action_time > 3: # 3-second cooldown
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            lm_list = []
            for lm in results.multi_hand_landmarks[0].landmark:
                lm_list.extend([lm.x, lm.y])
            
            prediction = model.predict(np.array([lm_list]), verbose=0)
            if np.max(prediction) > 0.90:
                gesture = actions[np.argmax(prediction)]
                process_with_llm(gesture)
                last_action_time = time.time()

    cv2.imshow("Safe AI Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()