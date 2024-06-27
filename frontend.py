from flask import Flask, render_template
from flask_socketio import SocketIO
import zmq
import threading
import time

# Rate limiting parameters
PUBLISH_INTERVAL = 0.1  # 100ms

app = Flask(__name__)
socketio = SocketIO(app)

def zmq_listener():
    # ZeroMQ context and subscriber socket
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

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
                print(data_ints)
                socketio.emit('new_data', {'message': str(data_ints)})
                last_emit_time = current_time

        except zmq.Again:
            pass

# Start ZeroMQ listener in a separate thread
threading.Thread(target=zmq_listener, daemon=True).start()

@app.route('/display')
def display():
    return render_template('display.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    client_thread = threading.Thread(target=zmq_listener, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
