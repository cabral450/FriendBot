from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import ast

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('msg:send')
def chat_message(message):
    print(message['text'])
