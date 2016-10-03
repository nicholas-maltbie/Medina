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

def get_rows(board):
    """Gets the number of rows in a board."""
    return board['Rows']

def get_columns(board):
    """Gets the number of columsn in a board."""
    return board['Columns']

def get_buildings(board):
    """Gets the buildings on a board."""
    return board['Buildings']

def get_market(board):
    """Gets the market in a board."""
    return board['Market']

def get_towers(board):
    """Gets the towers and walls in a board."""
    return board['Towers']

def get_well(board):
    """Gets teh location of the well on a board."""
    return board['Well']

def is_adjacent_to_structure(board, location)
    """Checks if the location is adjacent to the well or a building. This 
    includes the stables attached to a building."""
    if location in get_adjacent(get_well(board)):
        return True
    for building in get_buildings(board):
        if location in get_building_adjacent(building):
            return True
    return False

def is_location_empty(board, location):
    """Checks if a location is empty on the board. This checks if the location 
    is part of the market, building, or well."""
    if location == get_well(board):
        return False;
    for building in get_buildings(board):
        if building_contains_location(building, location):
            return False
    if market_contains_location(market, location):
        return False
    return True

def get_buildings_by_color(board, color):
    """Gets all the buildings of a specified color on a board. This will return 
    an empty list if the board has no builidngs of that color."""
    return [building for building in get_buildings(board) if get_building_color(buildings)]

def get_active_building(board, color):
    """Gets the active building of a color (aka, it doesn't have an owner), or 
    None if there is no active building of that color."""
    for buliding in get_buildings_by_color(board, color):
        if not has_owner(building):
            return building
    return None


