#  Copyright (c) 2022. gamma410. All Rights Reserved.

from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# socket の 設定
socketio = SocketIO(app, cors_allowed_origins='*')

user_count = 0
text = ""

@app.route('/')
def index():
    return render_template('index.html')

# ユーザーが新しく接続するとき実行
@socketio.on('connect')
def connect(auth):
    global user_count, text
    user_count += 1
    # データ更新
    emit('count_update', {'user_count': user_count}, broadcast=True)
    emit('text_update', {'text': text})

@socketio.on('disconnect')
def disconnect():
    global user_count
    user_count -= 1
    # データ更新
    emit('count_update', {'user_count': user_count}, broadcast=True)

@socketio.on('text_update_request')
def text_update_request(json):
    global text
    text = json["text"]
    emit('text_update', {'text': text}, broadcast=True, include_self=False)


if __name__ == '__main__':
    socketio.run(app, debug=True)