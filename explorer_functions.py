import re


def filter_casual(game_data):

    games_buffer = list()
    for game in game_data:
        if game[5] != "?" and game[6] != "?":
            games_buffer.append(game)
    return games_buffer


def filter_color(white, username, game_data):
    games_buffer = list()
    if white:  # If user is playing white in js position
        for game in game_data:
            if game[1] == username:  # If user is white in game
                games_buffer.append(game)
    else:  # If user is playing black in js position
        for game in game_data:
            if game[2] == username:  # If user is black in game
                games_buffer.append(game)
    return games_buffer


def filter_time_control(time_control, game_data):
    games_buffer = list()
    if time_control == "blitz":
        for game in game_data:
            if game[4] == "Rated Blitz game":
                games_buffer.append(game)
    if time_control == "classical":
        for game in game_data:
            if game[4] == "Rated Classical game":
                games_buffer.append(game)
    return games_buffer


def filter_opponent(opponent, white, game_data):
    games_buffer = list()
    if white:
        for game in game_data:
            if game[2] == opponent:
                games_buffer.append(game)
    else:
        for game in game_data:
            if game[1] == opponent:
                games_buffer.append(game)
    return games_buffer


def filter_moves(moves, game_data):
    games_buffer = list()
    for game in game_data:
        if game[0][:len(moves)] == moves:
            games_buffer.append(game)
    return games_buffer


def get_moves_data(game_data, moves):
    moves_data = dict()
    for game in game_data:
        move = str(game[0][len(moves):len(moves) + 1])  # Finds next move of game
        move = re.sub("\[|\]|'", "", move)

        if len(moves) % 2 == 0:  # If white made last move
            move_elo = int(game[5])  # White's elo
        else:  # If black made last move
            move_elo = int(game[6])  # Black's elo

        if move not in moves_data:

            if game[3] == "1-0":
                moves_data[move] = [1, [1, 0, 0], move_elo]
            elif game[3] == "1/2-1/2":
                moves_data[move] = [1, [0, 1, 0], move_elo]
            elif game[3] == "0-1":
                moves_data[move] = [1, [0, 0, 1], move_elo]
        elif move in moves_data:
            moves_data[move][0] += 1
            moves_data[move][2] += move_elo
            if game[3] == "1-0":
                moves_data[move][1][0] += 1
            elif game[3] == "1/2-1/2":
                moves_data[move][1][1] += 1
            elif game[3] == "0-1":
                moves_data[move][1][2] += 1

    for move in moves_data.keys():
        moves_data[move][2] = int(moves_data[move][2] / moves_data[move][0])
        moves_data[move][1][0] = round(((moves_data[move][1][0] / moves_data[move][0]) * 100), 1)
        moves_data[move][1][1] = round(((moves_data[move][1][1] / moves_data[move][0]) * 100), 1)
        moves_data[move][1][2] = round(((moves_data[move][1][2] / moves_data[move][0]) * 100), 1)
    return moves_data


def get_games(white, username, game_data, moves, time_control, opponent):
    game_data = filter_casual(game_data)
    game_data = filter_color(white, username, game_data)
    if time_control:
        game_data = filter_time_control(time_control, game_data)
    if opponent:
        game_data = filter_opponent(opponent, white, game_data)
    game_data = filter_moves(moves, game_data)
    return game_data

