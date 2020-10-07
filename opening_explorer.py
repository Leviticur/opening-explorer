import json
import operator
import chess.pgn
import explorer_functions
import opening_explorer_flask

pgn = open('./lichess_Leviticur_2020-06-12.pgn')
username = "Leviticur"

with open('game_data.json') as f:
    game_data = json.load(f)

if not game_data:

    print("No game data found")
    game_data = list()
    while True:

        game = chess.pgn.read_game(pgn)  # Reads next game from pgn

        if not game:
            with open('game_data.json', 'w') as f:
                json.dump(game_data, f)
            break

        game_moves = str(game.mainline_moves()).split()
        del game_moves[0::3]
        game_data.append([game_moves, game.headers.get('White'), game.headers.get('Black'), game.headers.get('Result'),
                          game.headers.get('Event'), game.headers.get('WhiteElo'), game.headers.get('BlackElo')])
        print(game_data)

else:
    print("Game data already found")

white = True
opponent = None
time_control = None

moves = list()


def opening_explorer(jsdata):
    global white
    global opponent
    global time_control
    global moves
    if jsdata.startswith("setcolor"):
        white = True if jsdata[8:] == "white" else False
    elif jsdata.startswith("setopponent"):
        opponent = jsdata[11:]
    elif jsdata.startswith("settimecontrol"):
        if jsdata[14:] == "all":
            time_control = None
        else:
            time_control = jsdata[14:]
    else:  # If board position is sent
        moves = jsdata.replace("_", " ").split()  # Could split at _
        del moves[0::3]

    games = explorer_functions.get_games(white, username, game_data, moves, time_control, opponent)
    moves_data = explorer_functions.get_moves_data(games, moves)

    ordered_moves_data = sorted(moves_data.items(), key=operator.itemgetter(1))  # sorts responses by moves played
    opening_explorer_flask.pythondata = ordered_moves_data[::-1]  # Immediately after function call js reads pythondata

