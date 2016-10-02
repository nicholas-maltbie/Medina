"""A board is the main area of play for different players in the game. This is 
were all game pieces are played and is used to determine most of the players' 
final scores.

A board inclues multiple elements: buildings (contigious blocks of building 
pieces and stables), a market street (or streets), towers with walls branching 
off them, and a well.
"""

import random
from Player import *
from Location import *
from Building import *
from Market import *
from Tower import *

def make_board(rows, columns):
    """Makes a board with a default game setup, 
    One well will be randomly placed.
    A set of towers will be made.
    A market will be created with a randomly placed merchant.
    
    A board has Buildings, a market, towers, and a well
    """
    well_location = make_location(random.randrange(rows - 2) + 1, \
        random.randrange(columns - 2) + 1)
    market_start = make_location(random.randrange(rows - 2) + 1, \
        random.randrange(columns - 2) + 1)
    while market_start == well_location:
        market_start = make_location(random.randrange(rows - 2) + 1, \
            random.randrange(columns - 2) + 1)
        
    return {'Rows':rows, 'Columns':columns, 'Buildings':[], \
        'Market':make_market(street_start), 'Towers':make_towers(rows, columns), 
        'Well':well_location}

