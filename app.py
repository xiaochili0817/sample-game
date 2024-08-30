from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

rooms = {}  # Store the state of each room

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    room = data['room']
    username = data['username']

    session['room'] = room
    session['username'] = username

    join_room(room)

    if room not in rooms:
        rooms[room] = {'players': [], 'choices': {}}

    if username not in rooms[room]['players']:
        rooms[room]['players'].append(username)

    emit('player_joined', {'username': username, 'players': rooms[room]['players']}, room=room)

@socketio.on('make_choice')
def handle_make_choice(data):
    room = session.get('room')
    username = session.get('username')
    choice = data['choice']

    rooms[room]['choices'][username] = choice

    if len(rooms[room]['choices']) == 2:
        player1, player2 = rooms[room]['players']
        choice1 = rooms[room]['choices'][player1]
        choice2 = rooms[room]['choices'][player2]

        result = determine_winner(choice1, choice2)
        emit('result', {'result': result, 'player1': player1, 'choice1': choice1, 'player2': player2, 'choice2': choice2}, room=room)
        rooms[room]['choices'] = {}  # Reset choices for the next round

def determine_winner(choice1, choice2):
    if choice1 == choice2:
        return 'Draw'
    elif (choice1 == 'rock' and choice2 == 'scissors') or \
         (choice1 == 'scissors' and choice2 == 'paper') or \
         (choice1 == 'paper' and choice2 == 'rock'):
        return 'Player 1 Wins'
    else:
        return 'Player 2 Wins'

if __name__ == '__main__':
    socketio.run(app, debug=True)

