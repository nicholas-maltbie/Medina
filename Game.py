"""This file will contain the code that represents the digital model of the 
game and can be refrenced by other parts of the project.

Different parts of the game include:
    - Board
    - Players
    - Tiles
"""

import random

def make_board(rows, columns):
    """Creates a dictionary of the board and rooftops played.
    
    A board is the general area where all players take actions. 

    The board is a grid that has space for buildings, merchants and walls to be 
    placed on the board. Buildings and merchants are in the same space so their 
    data will be saved in a 2D array of characters where a code will correspond 
    to what each character means. Rooftops are placed above buildings and hence 
    will be saved separate from the board. The board is saved under the key of 
    'board' and each player is saved under the key of 'p_%name%', where %name% is 
    the name of the player. 

    Large game (3 or 4 players)
        board size is 11 x 16       (13 x 18 with walls)
    Small game (2 players)
        board size is 10 x 14       (12 x 16 with walls)

    Rooftop Example:
        'p_name' : [(0, 1), (6, 4)],
        'p_name2' : [(10, 5)],
        'p_name3' : [],
        'p_name4' : [(13, 3)]

    Character Code Key:
        'e' = empty
        'l' = wall location     (not constructed)
        'c' = constructed wall
        's' = stable
        'w' = well              (One on the board)
        't' = tower             (One at each corner)
        'm' = merchant          (builds in a chain)
        Building color character codes.

    Example of Saved Buildings and walls:
        
        New Game:
        
        t l l l l l l l l l l l l l l l l t
        l e e e e e e e e e e e e e e e e l
        l e e e e m e e e e e e e e e e e l
        l e e e e e e e e e e w e e e e e l
        l e e e e e e e e e e e e e e e e l
            ... more rows ...
        l e e e e e e e e e e e e e e e e l
        l e e e e e e e e e e e e e e e e l
        t l l l l l l l l l l l l l l l l t
        
        Game in progress:
        
        
        t w w w w w l l l l l l l l w w w t
        l e e e e e e e e e e e e e e e e w
        l e m m m m e e B e e e e V e e e w
        l e e e e m m m B B e w e V V e e w
        l e e e e e e m m B e e e e e e e l
            ... more rows ...
        l e e R R R e e e e e e e e e e e l
        w e R R R R e e e e e e e e e e e l
        t w w w w l l l l l l l l l l l l t
    
    Args:
        rows: Number of rows for buildings.
        columns: Number of columns for buildings.
        
    Raises:
        AssertionError: rows and columns must both be integers greater than 
            zero to create a board.
    """
    assert type(rows) == int, "Rows is not an integer, %r" % rows
    assert type(columns) == int, "Column is not an integer %r" % columns
    assert rows > 0, "Row must be greater than zero %r" % rows
    assert columns > 0, "Columns must be greater than zero %r" % columns
    
    places = [list(TOWER + WALL_LOCATION * columns + TOWER)]
    for i in range(0, rows):
        places.append(list(WALL_LOCATION + EMPTY * columns + WALL_LOCATION))
    places.append(list(WALL_LOCATION + WALL_LOCATION * columns + TOWER))
    
    return {'board': places, 'p_' + NEUTRAL_PLAYER:[]}

def get_large_board():
    """Generates and returns a board for a game with three or four players
    
    Args:
        player_names: List of player names."""
    return make_board(11, 16)

def get_small_board(player_names):
    """Generates and returns a board for a game with B players
    
    Args:
        player_names: List of player names."""
    return Board(rows=10, columns=14)

def get_game_board(board):
    """Gets the game board element of a board."""
    return board['board']

def get_board_element(board, row, column):
    """Gets an element at a specified location of a board."""
    return get_game_board(board)[row][column]

def is_space_empty(board, row, column):
    """Checks if a location on a board is empty."""
    return get_board_element(board, row, column) == EMPTY

def set_board_element(board, row, column, element):
    """Sets an element at a specified location of a board."""
    before = get_board_element(board, row, column)
    get_game_board(board)[row][column] = element;
    return before

def place_well(board):
    """Places the well in a board and then returns the row and column of the 
    location in which the well was placed."""
    game_board = get_game_board(board)
    row_range, column_range = len(board) - 2, len(board[0]) - 2
    location = (random.randrange(row_range), random.randrange(column_range))
    set_board_element(board, location[0], location[1], WELL)
    return location

def get_played_rooftops(board, player):
    """Gets the rooftops played by the player as a list of locations saved in 
    the format of [(row, column), (row, column), ...]. An empty list means the 
    player has not played any rooftops."""
    ref = 'p_' + player.name
    if not ref in board:
        return []
    return board[ref]

def get_num_played_rooftops(board, player):
    """Gets the number of rooftops the player has played."""
    return len(get_played_rooftops(board, player))

def play_rooftop(board, player, row, column):
    """Plays a rooftop on the board for a player. If the player has not played 
    any rooftops yet, a new key pair will be added to the board reffering to the 
    player and a new empty list of rooftops."""
    ref = 'p_' + player.name
    if not ref in board:
        board[ref] = []
    board[ref].append((row, column))

BUILDINGS_COLORS = ['G', 'V', 'B', 'O']
"""Colors for different buildings: Grey, Violet, Brown, Orange""" 
BUILDINGS_COLORS_HEX = {'G': 'E2E2E2', 
                        'V': 'A70BAC',
                        'B': '4E2E03',
                        'O': 'FFD500'}
"""Colors of the buildings in HEX color codes, RRGGBB"""

NEUTRAL_PLAYER = ""
"""Name of the neutral player for 2 and 3 player games."""

#Code for the different kinds of locations within a board
EMPTY = 'e'
WALL_LOCATION = 'w'
WALL = 'c'
STABLE = 's'
WELL = 'w'
TOWER = 't'
MERCHANT = 'm'

class Player:
    """A Player needs to be able to hold pieces and have a name.
    
    A player plays games in medina and is responsible to hold peices and be 
    identifyable on the board.
    
    Attributes:
        name: Name of the player.
        buildings: Dictionary of number of buildings for each color building
             the player owns. Dictionary is in the format of:
            {Building_color: num_held,
                Building_color2: num_hel2,
                ...
            }
        stables: Number of stables the player has.
        rooftops: Number of roofotps the player has.
        extra_rooftops: Number of extra rooftops given.
        merchants: Number of merchants the player has.
        walls: The number of walls the player has.
        tiles: Tiles the player has acquired."""
        
    buildings_given = {2:8,3:6,4:5} 
    #Buildings given to each player depending on game size
    rooftops_given = {2:4,3:4,5:4}
    #Rooftops given to each player
    extra_rooftops_given = {2:2, 3:1, 4:0}
    #Neutral rooftops given to players
    stables_given = {2:4, 3:4, 4:3}
    #Number of stables given to players
    merchants_given = {2:12, 3:8, 4:6}
    #Number of merchants given to players
    walls_given = {2:15, 3:12, 4:9}
    
    
    def __init__(self, name, num_players):
        """Creates a player with a given name and game size.
        
        Args:
            name: Name of the player.
            num_players: Number of players in the game."""
        self.name = name
        self.buildings = {};
        for color in BUILDINGS_COLORS:
            buildings[color] = buildings_given[num_players]
        stables = stables_given[num_players]
        rooftops = rooftops_given[num_players]
        extra_rooftops = extra_rooftops_given[num_players]
        merchants = merchants_given[num_players]
        walls = walls_given[num_players]
    
class Tile:
    """Define different kinds of tiles here and describe. Tiles should be held 
    by players in the game
    
    Tiles can be one of three types: Tower, Tea or Palace. Palace tiles are 
    awarded for building the largest of a building color. Tower tiles are 
    awarded for building a building connected to a wall from a tower. Tea tiles 
    are awarded for claiming purple buildings.
    
    If a tile is a tower tile, it will also hold merchants for the first player 
    who claims the tile.
    
    Attributes:
        type: Type of tile, Tea, Tower, or Palace.
        value: Point value of the tile.
        merchants: Only for Tower tiles, the number of merchants left on the 
            tile for players to pickup."""
    
    def get_tower_tiles():
        """Gets all the tower tiles in the game"""
        return [Tile(TOWER_TILE, value+1) for value in range(4)]
    
    def get_palace_tiles():
        """Gets all the palace tiles in the game"""
        return [Tile(PALACE_TILE, value+1) for value in range(4)]
        
    def get_tea_tiles():
        """Gets all the tea tiles in the game"""
        return [Tile(TEA_TILE) for i in range(6)]
    
    TEA_TILE = 'TEA'
    TOWER_TILE = 'TOW'
    PALACE_TILE = 'PAL'
    
    PALACE_COLORS = {1:BUILDINGS_COLORS[0], 
        2:BUILDINGS_COLORS[1],
        3:BUILDINGS_COLORS[2],
        4:BUILDINGS_COLORS[3]}
    
    def __init__(self, type, value=0):
        """Creates a player with a given properties.
        
        Args:
            type: Type of tile: Tower, Palace, or Tea.
            value: Point value of the tile."""
        self.type = type
        self.value = value
        if type == TOWER_TILE:
            self.merchants = 4 - value
