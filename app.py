from flask import Flask, request, render_template
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from random import randrange
from game import Game, GameException
from player import Player

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/', methods=['GET'])
def root():
    return render_template('index.html', data={ 'url': request.url })

@socketio.on('hello')
def handle_hello(json):
    try:
        room = 'pokerroom'
        join_room(room)
        player = Player(json['name'])
        player.setid(request.sid)
        thegame.addplayer(player)
        emit('message', { 'message' : player.name() + ' has joined the game' }, room=room)
        players = thegame.players()
        playernames = []
        for p in players:
            playernames.append(p.name())
        emit('players', { 'players' : playernames }, room=room)
        if len(playernames) > 2:
            gameready = True
        else:
            gameready = False
        if gameready:
            emit('start', {}, room=players[0].getid())
    except GameException as gerr:
        emit('error', {'message': str(gerr)})
    except Exception as err:
        emit('error', {'message': 'Unexpected error, please try later'})

@socketio.on('ready')
def handle_ready(json):
    # Choose a dealer
    rotate = randrange(0, len(thegame.players()))
    while True:
        thegame.rotatedealer()
        rotate = rotate - 1
        if rotate < 0:
            break
    emit('message', { 'message' : thegame.players()[0].name() + ' to deal' }, room='pokerroom')
    thegame.newhand()
    thegame.deal()
    for player in thegame.players():
        hand = []
        for card in player.hand():
            cardastup = card.tup()
            hand.append({'value': cardastup[0], 'suit': cardastup[1]})
        emit('deal', {'hand': hand}, room=player.getid())

if __name__ == '__main__':
    thegame = Game()
    socketio.run(app, port=5001, debug=True)
