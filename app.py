from flask import Flask, render_template, request, redirect, url_for
import subprocess
import sys
import os
import pandas as pd
import json

app = Flask(__name__)
active_process = None

def get_gestures():
    if os.path.exists('hand_data.csv'):
        try:
            df = pd.read_csv('hand_data.csv', header=None)
            return sorted(df.iloc[:, -1].unique().tolist())
        except:
            return []
    return []

@app.route('/')
def index():
    return render_template('index.html', gestures=get_gestures())

@app.route('/record', methods=['POST'])
def record():
    name = request.form.get('name')
    subprocess.run([sys.executable, 'collect_data.py', name])
    return redirect('/')

@app.route('/save_intent', methods=['POST'])
def save_intent():
    name = request.form.get('name')
    intent = request.form.get('intent')
    mapping = {}
    if os.path.exists('intents.json'):
        with open('intents.json', 'r') as f:
            mapping = json.load(f)
    mapping[name] = intent
    with open('intents.json', 'w') as f:
        json.dump(mapping, f, indent=4)
    return redirect('/')

@app.route('/delete/<name>', methods=['POST'])
def delete(name):
    if os.path.exists('hand_data.csv'):
        df = pd.read_csv('hand_data.csv', header=None)
        df = df[df.iloc[:, -1] != name]
        df.to_csv('hand_data.csv', index=False, header=False)
    return redirect('/')

@app.route('/train', methods=['POST'])
def train():
    subprocess.run([sys.executable, 'train_model.py'])
    return redirect('/')

@app.route('/start', methods=['POST'])
def start():
    global active_process
    if active_process is None:
        active_process = subprocess.Popen([sys.executable, 'main_control.py'])
    return redirect('/')

@app.route('/stop', methods=['POST'])
def stop():
    global active_process
    if active_process:
        active_process.terminate()
        active_process = None
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)