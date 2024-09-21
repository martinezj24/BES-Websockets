from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO()

socketio.init_app(app, cors_allowed_origin='*')  # Set CORS to allow all origins with '*'

# Global HashMap to store messages
message_storage = {}

@socketio.on('connect')  # Triggered when a client connects
def handle_connect():
    print('Client Connected')

@socketio.on('disconnect')  # Triggered when a client disconnects
def handle_disconnect():
    print('Client Disconnected')

@socketio.on('message')  # Listening for incoming messages
def handle_message(message):
    # Store the message in message_storage, using a unique key
    message_id = len(message_storage) + 1
    message_storage[message_id] = message

    # Print all stored messages to the terminal
    print("Stored Messages:")
    for msg_id, msg in message_storage.items():
        print(f"{msg_id}: {msg}")

    # Emit the message back to the client
    socketio.emit('message', message)

@app.route("/")  # Serve the home page
def home():
    return render_template('base.html')

if __name__ == '__main__':
    app.debug = True
    socketio.run(app)
