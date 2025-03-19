from flask import Flask, jsonify
import time
import json
import global_vars
from flask_cors import CORS
import threading 
import queue 

app = Flask(__name__)
CORS(app)

data_queue = queue.Queue()

@app.route('/data')
def send_data():
    if not data_queue.empty():
        data_to_send = data_queue.get()
        json_data = json.dumps(data_to_send) + "\n"  # Add newline for easier parsing on client
        encoded_data = json_data.encode('utf-8')
        print(f"Data in send_data SERVER: {encoded_data}")
        return encoded_data
    else:
        data_to_send = global_vars.DATA_TO_SEND
        json_data = json.dumps(data_to_send) + "\n"  # Add newline for easier parsing on client
        encoded_data = json_data.encode('utf-8')
        return encoded_data

def update_data(new_data):
    global_vars.DATA_TO_SEND = new_data

    data_queue.put(new_data)
    print(f"updated data: {global_vars.DATA_TO_SEND}")

def run_server():
    app.run(host="0.0.0.0", port=65432, threaded=True)

if __name__ == "main":
    run_server()
    