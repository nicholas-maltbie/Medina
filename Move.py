"""This module is responsible for making moves in a JSON format then interpreting
the results of a move by changing a board or making new moves. A move consists
of different pieces of information:

player_name: name
move_type: {PASS or NONE_POSSIBLE or NORMAL}
piece_played: {WALL or BUILDING or STABLE or MERCHANT or ROOFTOP or NO_PLAY}
location: {row, column}

>>> move = make_move('Bob',PASS)
>>> get_player_name(move)
'Bob'
>>> get_move_type(move)
'PASS'
>>> get_piece(move) is None
True
>>> get_location(move) is None
True

>>> move = make_move('Bob',NORMAL,WALL,(1,2))
>>> get_player_name(move)
'Bob'
>>> get_move_type(move)
'NORMAL'
>>> get_piece(move)
'WALL'
>>> get_location(move)
[1, 2]
"""

import Location
import json

#Move types
PASS = 'PASS'
NONE_POSSIBLE = 'NONE_POSSIBLE'
NORMAL = 'NORMAL'

#Piece types
WALL = 'WALL'
BUILDING = 'BUILDING'
STABLE = 'STABLE'
MERCHANT = 'MERCHANT'
ROOFTOP = 'ROOFTOP'
WELL = 'WELL'
NO_PLAY = 'NO PLAY'


def make_move(player_name, move_type, piece_type=None, location=None):
    if move_type != NORMAL:
        assert piece_type == None and location == None

    return json.dumps({"player_name": player_name, "move_type": move_type, "piece_type": piece_type, "location": location})
    #this should return a move with the following information in a JSON format

def get_player_name(move):
    getter = json.loads(move)
    return getter['player_name']
    #This should parse a move and return the player name

def get_move_type(move):
    getter = json.loads(move)
    return getter['move_type']
    #This should parse the move and reutrn either 'PASS', 'NONE_POSSIBLE', or 'NORMAL'

def get_piece(move):
    getter = json.loads(move)
    if get_move_type(move) != NORMAL:
        return None
    return getter['piece_type']
    #This should parse the move and return the piece type played (or NO_PLAY)

def get_location(move):
    getter = json.loads(move)
    if get_move_type(move) != NORMAL:
        return None
    return getter['location']
    #This should return a location of where the move specifies
