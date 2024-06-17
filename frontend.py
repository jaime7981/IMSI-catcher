from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import zmq
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

# ZeroMQ context and subscriber socket
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")
socket.setsockopt_string(zmq.SUBSCRIBE, "")

# Rate limiting parameters
PUBLISH_INTERVAL = 0.1  # 100ms

def zmq_listener():
    last_emit_time = time.time()
    while True:
        try:
            # Receive data as bytes
            data_bytes = socket.recv(flags=zmq.NOBLOCK)
            # Convert bytes to list of integers
            data_ints = list(data_bytes)

            # Rate limit the publishing
            current_time = time.time()
            if current_time - last_emit_time >= PUBLISH_INTERVAL:
                print("Sending data")
                socketio.emit('new_data', data_ints)
                last_emit_time = current_time

        except zmq.Again:
            pass

# Start ZeroMQ listener in a separate thread
threading.Thread(target=zmq_listener, daemon=True).start()

@app.route('/display')
def display():
    return render_template('display.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
