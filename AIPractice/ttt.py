"""This is the saved state of the board and moves for a tic tac toe game"""

import json
import random

def print_board(board):
    """Prints the board for a game"""
    disp = ""
    for row in range(3):
        for col in range(3):
            if is_empty(board, row, col):
                disp += " "
            else:
                disp += get_piece(board, row, col)
            
            if col != 2:
                disp += "|"
        if row != 2:
            disp += "\n------\n"
    print(disp)

def make_board():
    """Makes a board for tic tac toe"""
    return [[None, None, None], [None, None, None], [None, None, None]]
    
def get_piece(board, row, col): 
    "Gets a piece from the board"""
    return board[row][col]

def is_empty(board, row, col):
    """Checks if a location on the board is empty"""
    return board[row][col] == None
    
def play_piece(board, row, col, piece):
    """Plays a piece on the board"""
    board[row][col] = piece
    
def check_winner(board):
    """Checks if a player has won the game, returns 'x' if player one has won,
    'o' if player two has won, 'cat' if the board is full and there is no 
    winner, and None if no player has won yet"""
    for row in range(3):
        if not is_empty(board, row, 0) and get_piece(board, row, 0) == \
                get_piece(board, row, 1) == get_piece(board, row, 2):
            return get_piece(board, row, 0);
    for col in range(3):
        if not is_empty(board, 0, col) and get_piece(board, 0, col) == \
                get_piece(board, 1, col) == get_piece(board, 2, col):
            return get_piece(board, 0, col);
    if not is_empty(board, 0,0) and get_piece(board, 0,0) == \
            get_piece(board, 1, 1) == get_piece(board, 2, 2):
        return get_piece(board, 0,0)
    elif not is_empty(board, 2, 0) and get_piece(board, 2, 0) == \
            get_piece(board, 1, 1) == get_piece(board, 0, 2):
        return get_piece(board, 1, 1)
    allfilled = True
    for row in range(3):
        for col in range(3):
            if is_empty(board, row, col):
                allfilled = False
    if allfilled:
        return 'cat'
    return None

def make_move(row, col, player):
    """Makes and returns a move"""
    return {"row": row, "col":col, "player":player}

def get_move_row(move):
    """Gets the row of a move"""
    return move['row']

def get_move_col(move):
    """Gets the col of a move"""
    return move['col']
    
def get_move_player(move):
    """Gets the player who made a move"""
    return move['player']

def get_json_move(move):
    """Makes a move into JSON format"""
    return json.dumps(move)

def get_move_from_json(json_move):
    """Reads in a move from JSON format"""
    getter = json.loads
    return {'row':getter['row'], 'col':getter['col'], 'player':getter['player']}

def apply_move(board, move):
    """Does the affect of a move to the board"""
    play_piece(board, get_move_row(move), get_move_col(move), get_move_player(move))

def get_possible_moves(board, player):
    """Gets all possible moves a player can make."""
    moves = []
    for row in range(3):
        for col in range(3):
            if is_empty(board, row, col):
                moves.append(make_move(row, col, player))
    return moves

def make_human_agent():
    """Gets a human agent, this will prompt the standard IO for input from the 
    person running the game."""
    def get_move(board, player):
        row, col = 0, 0
        valid = False
        print_board(board)
        while not valid:
            print("You are " + player + ". Where do you want to play? 'row col': ")
            try:
                row, col = (int(val) for val in input().split(' '))
            except:
                print("That is not a valid input... 'row col' is the format")
                continue
            if row < 0 or row > 2:
                print("Row must be between 0 and 2")
            elif col < 0 or col > 2:
                print("Col must be between 0 and 2")
            elif not is_empty(board, row, col):
                print("That location is alreay filled")
            else:
                valid = True
        return make_move(row, col, player)
    return get_move

def make_random_agent():
    """Gets an agent that will make random moves"""
    def get_move(board, player):
        return random.choice(get_possible_moves(board, player))
    return get_move
    
def play_game(agent1, agent2, name1, name2):
    """Plays a game of tic tac toe with two agents and returns the winner."""
    board = make_board()
    names = [name1, name2]
    players = [agent1, agent2]
    pieces = ['x', 'o']
    current = random.randint(0,1)
    while check_winner(board) == None:
        move = players[current](board, pieces[current])
        apply_move(board, move)
        current = (current + 1) % 2
    win = check_winner(board)
    if win == 'o':
        return name2
    elif win == 'x':
        return name1
    else:
        return 'tie'
    
if __name__ == "__main__":
    distrib = {'player1':0, 'player2':0, 'tie':0}
    plays = 10000
    for i in range(plays):
        distrib[play_game(make_random_agent(), make_random_agent(), \
                'player1', 'player2')] += 1;
    print('player1 won ' + str(distrib['player1']) + ' times ' + \
            str(int(distrib['player1'] / plays * 100)) + "%")
    print('player2 won ' + str(distrib['player2']) + ' times ' + \
            str(int(distrib['player2'] / plays * 100)) + "%")
    print('tied        ' + str(distrib['tie']) + ' times ' + \
            str(int(distrib['tie'] / plays * 100)) + "%")
    
