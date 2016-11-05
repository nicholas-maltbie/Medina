"""This module is responsible for making moves in a JSON format then interpreting 
the results of a move by changing a board or making new moves. A move consists 
of different pieces of information:

player_name: name
move_type: {PASS or NONE_POSSIBLE or NORMAL}
piece_played: {WALL or BUILDING or STABLE or MERCHANT or ROOFTOP or NO_PLAY}
location: {row, column} """

import Location

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
NO_PLAY = 'NO PLAY'


def make_move(player_name, move_type, peice_type=None, location=None):
    return ""
    #this should return a move with the following information in a JSON format

def get_player_name(move):
    pass
    #This should parse a move and return the player name

def get_move_type(move):
    pass
    #This should parse the move and reutrn either 'PASS', 'NONE_POSSIBLE', or 'NORMAL'

def get_peice(move):
    pass
    #This should parse the move and return the piece type played (or NO_PLAY)
    
def get_location(move):
    pass
    #This should return a location of where the move specifies

