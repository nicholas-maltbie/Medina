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
from Move import *


def make_board(rows, columns):
    """Makes a board with a default game setup,
    One well will be randomly placed.
    A set of towers will be made.
    A market will be created with a randomly placed merchant.

    A board has Buildings, a market, towers, and a well
    """
    well_location = random_central_location(rows, columns)
    market_start = random_central_location(rows, columns)
    while market_start == well_location:
        market_start = random_central_location(rows, columns)

    return {'Rows':rows, 'Columns':columns, 'Buildings':[], \
        'Market':make_market(market_start), 'Towers':make_towers(rows, columns), \
        'Well':well_location}

def clone_board(board):
    """makes a deep clone of a board"""
    return {'Rows':get_rows(board), 'Columns':get_columns(board), \
        'Buildings':[clone_building(building) for building in get_buildings(board)], \
        'Market':clone_market(get_market(board)),
        'Towers':clone_towers(get_towers(board)),
        'Well':get_well(board)}

def get_piece(board, location):
    """Gets a piece at a given location with from a board. The piece type
    returned will be that of those found in Move"""
    row = get_row(location)
    col = get_column(location)
    assert 0 <= row < get_rows(board) and 0 <= col < get_columns(board)
    if market_contains_location(get_market(board),(board)):
        return MERCHANT
    for building in get_buildings(board):
        if location in get_stable_locations(building):
            return STABLE
        elif building_contains_location(building, location):
            return BUILDING
    if location == get_well(board):
        return WELL

def random_central_location(rows, columns):
	"""Creates a random location in the center part of town: Not touching a wall"""
	return make_location(random.randrange(rows - 2) + 1, random.randrange(columns - 2) + 1)

def get_rows(board):
    """Gets the number of rows in a board."""
    return board['Rows']

def get_columns(board):
    """Gets the number of columns in a board."""
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
    """Gets the location of the well on a board."""
    return board['Well']

def get_all_locations(board):
    """Gets a set of all locations in a board."""
    rows = get_rows(board)
    columns = get_columns(board)
    return [make_location(i // columns, i % columns) for i in range(rows * columns)]

def get_buildings_claimed_by(board, player_name):
    """Gets all the buildings claimed by a player with the given name."""
    return [building for building in get_buildings(board) if get_owner(building) == player_name]

def get_bounded_set(board, location_set):
    """Gets a set of all locations in location_set that are within the bounds
    of the board. Locations are considered within the bounds if the row
    of the location is >= 0 and < row and if the column is >= 0 and < columns."""
    bounded = set()
    for loc in location_set:
        if get_row(loc) < get_rows(board) and get_row(loc) >= 0 and \
                get_column(loc) < get_columns(board) and get_column(loc) >= 0:
            bounded.add(loc)
    return bounded

def get_stable_piece_location(board):
    """Gets all the locations in which a stable can be attached to a building"""
    possible = set()
    for building in get_buildings(board):
        temp = set(get_building_peice_attach(building))
        for building2 in get_buildings(board):
            if building2 != building:
                temp = temp.difference(set(get_building_and_stables(building2)))
                temp = temp.difference(set(get_building_stable_adjacent(building2)))
        possible = possible.union(temp)
    for street in get_market(board):
        for loc in street:
            if loc in possible:
                possible.remove(loc)
    well = get_well(board)
    if well in possible:
        possible.remove(well)
    possible -= set(get_adjacent(get_well(board)))
    return get_bounded_set(board, possible)

def get_building_piece_locations(board, color):
    """Gets all the locations in which a building piece can be attached for a
    specific color. If there is no building of this color currently active,
    this will return all open locations on the board that are not adjacent to
    a structure. This will return an empty list if nothing can be attached to
    the building."""
    active = get_active_building(board, color)
    #If there is no active buidling, return all open locations
    possible = set()
    if active == None:
        possible = set(get_all_locations(board))
    else:
        possible = get_building_peice_attach(active)
        possible = get_bounded_set(board, possible)
    for street in get_market(board):
        possible -= set(street);
    for building in get_buildings(board):
        if building != active:
            #print(get_building_and_stables(building))
            for loc in get_building_and_stables(building):
                if loc in possible:
                    possible.remove(loc)
            for loc in get_building_stable_adjacent(building):
                if loc in possible:
                    possible.remove(loc)
    well = get_well(board)
    if well in possible:
        possible.remove(well)
    possible -= set(get_adjacent(get_well(board)))
    return get_bounded_set(board, possible);

def can_place_building_piece(board, location, color):
    """Checks if a piece can be added to a board at a specific location. This
    involves a few checks and can be one of two cases.

    The first case is if there is no active building of that color, then the
    building must be placed in an empty location that is not adjacent to any
    structure (well or other building).

    The second case is if there is an active building of that color. Then the
    piece must be placed in an empty location that is orthogonal to the
    active building. It must be placed contigious to the building pieces in the
    building and cannot be attached to a stable (stables attach to buidlings,
    buildings cannot attach to stables)."""
    #If the location is not empty, return False
    if not is_location_empty(board, location):
        return False
    #Get active building of given color
    active = get_active_building(board, color)
    #If there is no active building, check if is adjacent to a structure
    if active == None:
        return not is_adjacent_to_structure(board, location)
    #If there is an active building, check to make sure the location is
    #   contigious to the building
    return location in get_building_piece_attach(active)

def start_new_building(board, location, color):
    """Starts a new building at a given location."""
    get_buildings(board).append(make_building(color, location))

def is_adjacent_to_structure(board, location):
    """Checks if the location is adjacent to the well or a building. This
    includes the stables attached to a building."""
    if location in get_adjacent(get_well(board)):
        return True
    for building in get_buildings(board):
        if location in get_building_stable_adjacent(building):
            return True
    return False

def add_market_street(board, start):
    """Adds a new market street to the market and makes this street the active
    street."""
    get_market(board).add_market_street(market, start)

def can_place_on_current_street(board):
    """Checks if any additions can be made to the current active market
    street in the market."""
    market = get_market(board)
    #Get possible additions to current active street.
    possible = get_possible_addition(market)
    #Filter out locations already occupied
    possible = get_bounded_set(board, possible)
    for building in get_buildings(board):
        possible -= set(get_building_and_stables(building))
    possible.remove(get_well(board))
    #If there are open spaces, return the open spaces.
    return len(possible) > 0

def get_merchant_place_locations(board):
    """This will get all the locations on the board in which a merchant can be
    placed. If the market street has open locations at the head or tail of the
    street, this will return possible open locations. If the market street does
    not have open locations to attach a merchant, this will return every open
    location on the board in which a new street can be started. """
    market = get_market(board)
    #Get possible additions to current active street.
    possible = get_possible_addition(market)
    #Filter out locations already occupied
    possible = get_bounded_set(board, possible)
    for building in get_buildings(board):
        possible -= set(get_building_and_stables(building))
    well = get_well(board)
    if well in possible:
        possible.remove(well)
    #If there are open spaces, return the open spaces.
    if len(possible) > 0:
        return possible
    #If there are no open spaces, get all the locations.
    possible = set(get_all_locations(board))
    #Remove currently occupied locations and locations next to the streets.
    for street in market:
        possible -= set(street)
        possible -= set(get_adjacent_to_street(street))
    for building in get_buildings(board):
        possible -= set(get_building_and_stables(building))
    if well in possible:
        possible.remove(well)
    return get_bounded_set(board, possible)

def is_location_empty(board, location):
    """Checks if a location is empty on the board. This checks if the location
    is part of the market, building, or well."""
    if location == get_well(board):
        return False;
    for building in get_buildings(board):
        if buliding_contans_location_stables(building, location):
            return False
    if market_contains_location(market, location):
        return False
    return True

def get_buildings_by_color(board, color):
    """Gets all the buildings of a specified color on a board. This will return
    an empty list if the board has no builidngs of that color."""
    return [building for building in get_buildings(board) if get_building_color(building) == color]

def get_active_building(board, color):
    """Gets the active building of a color (aka, it doesn't have an owner), or
    None if there is no active building of that color."""
    for building in get_buildings_by_color(board, color):
        if not has_owner(building):
            return building
    return None

def get_num_walls_adjacent_to_building(board, building):
    """Gets the number of walls orthogonally adjacent to a given building."""
    wall_locations = get_wall_locations(get_towers(board))
    count = 0
    orthogonal = get_building_stable_orthogonal(building)
    for wall in wall_locations:
        if wall in orthogonal:
            count += 1
    return count

def get_num_merchants_adjacent_to_building(board, building):
    """Gets the number of merchants orthogonally adjacent to a given buidling."""
    merchant_locations = []
    for street in get_market(board):
        merchant_locations += street
    count = 0
    orthogonal = get_building_stable_orthogonal(building)
    for merchant in merchant_locations:
        if merchant in orthogonal:
            count += 1
    return count

def get_connected_towers(board, building):
    """Gets the tower numbers that a building is connected to. Tower's are
    numbered 1 through 4 each worth different points and has a different
    associated tile."""
    def is_connected_to_tower(tower_number, orthogonal):
        tower_walls = get_wall_locations_for_tower(get_towers(board), tower_number)
        for wall in tower_walls:
            if wall in orthogonal:
                return True
        return False
    orthogonal = get_building_stable_othogonal(building)
    return [num for num in range(1, 5) if is_connected_to_tower(num, orthogonal)]
