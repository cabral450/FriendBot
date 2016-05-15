from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import ast
from bot_app.parser import handleInput

app = Flask(__name__)
app.config['SECRET_KEY'] = 'RPI_INTRO_TO_AI_SPRING2016'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('msg:send')
def chat_message(message):
    response = handleInput(message['text'])
    print(response)
    emit('msg:response', {'user': 'FriendBot:', 'text': response})
