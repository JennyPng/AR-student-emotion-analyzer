from flask import Flask
from flask_socketio import SocketIO
import time
import threading
import jsonify
from flask_cors import CORS

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

@app.route('/')
def index():
    return "Server is running"

# Stream text to Unity every second
def stream_text():
    while True:
        text = f"Current time: {time.strftime('%H:%M:%S')}"
        socketio.emit('update_text', {'text': text})  # Send to Unity client
        time.sleep(1)

@socketio.on('connect')
def handle_connect():
    print('Unity client connected')

if __name__ == '__main__':
    # Start text streaming in a separate thread
    thread = threading.Thread(target=stream_text)
    thread.daemon = True
    thread.start()

    socketio.run(app, host='0.0.0.0', port=5000)
    