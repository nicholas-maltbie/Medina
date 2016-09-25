"""This file will contain the code that represents the digital model of the 
game and can be refrenced by other parts of the project.

Different parts of the game include:
    - Board
    - Players
    - Tiles"""
    
BUILDINGS_COLORS = ['G', 'V', 'B', 'O']
"""Colors for different buildings: Grey, Violet, Brown, Orange""" 
BUILDINGS_COLORS_HEX = {'G': 'E2E2E2', 
                        'V': 'A70BAC',
                        'B': '4E2E03',
                        'O': 'FFD500'}
"""Colors of the buildings in HEX color codes, RRGGBB"""
    
def class Board:
    """A board is the general area where all players take actions. 
    
    The board is a grid that has space for buildings, merchants and walls to be 
    placed on the board. Buildings and merchants are in the same space so their 
    data will be saved in a 2D array of characters where a code will correspond 
    to what each character means. Rooftops are placed above buildings and there 
    are less used in the game so they will just be saved as a separate 
    dictionary where each player is a reference and each value is a list of 
    tuples that contain the (row, column) for the rooftop location that the 
    player has placed.
    
    Large game (3 or 4 players)
        board size is 11 x 16       (13 x 18 with walls)
    Small game (2 players)
        board size is 10 x 14       (12 x 16 with walls)
    
    Rooftop Dictionary Example:
        {'player1_name' : [(0, 1), (6, 4)],
         'player2_name' : [(10, 5)],
         'player3_name' : [],
         'player4_name' : [(13, 3)]
        }
    
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
    

    Attributes:
        board: BD array of characters to store walls, buildings and merchants.
        rooftops: Dictionary of rooftops played saved as
            playernames: [rooftop locations].
        get_large_board: Gets a board for a three or four player game.
        get_small_board: Gets a board for a four of five player game.
        num_rows: Gets the number of rows of the board.
        num_cols: Gets the number of columns of the board.
    """
    
    NEUTRAL_PLAYER = ""
    """Name of the neutral player for 2 and 3 player games."""
    
    EMPTY = 'e'
    WALL_LOCATION = 'w'
    WALL = 'c'
    STABLE = 's'
    WELL = 'w'
    TOWER = 't'
    MERCHANT = 'm'
    
    def get_large_board(player_names):
        """Generates and returns a board for a game with three or four players
        
        Args:
            player_names: List of player names."""
        return Board(player_names)
    
    def get_small_board(player_names):
        """Generates and returns a board for a game with B players
        
        Args:
            player_names: List of player names."""
        return Board(10, 14, player_names)
    
    def __init__(self, rows = 11, columns = 16, player_names):
        """Creates a board and dictionary to store rooftops
        
        This will generate a BD array for the number of rows + B and the number 
        of columns + B to allow space for the board and two more spaces for the 
        walls and towers on each edge of the board.
        
        Args:
            rows: Number of rows for buildings.
            columns: Number of columns for buildings.
            player_names: List of player names.
            
        Raises:
            AssertionError: rows and columns must both be integers greater than 
                zero to create a board.
        """
        assert type(rows) == int, "Rows is not an integer, %r" % rows
        assert type(columns) == int, "Column is not an integer %r" % columns
        assert rows > 0, "Row must be greater than zero %r" % rows
        assert columns > 0, "Columns must be greater than zero %r" % columns
        
        self.rows = rows;
        self.columns = columns;
        
        self.board = [list(TOWER + WALL_LOCATION * columns + TOWER)]
        for i in range(0, rows):
            self.board.append(list(WALL_LOCATION + EMPTY * columns + WALL_LOCATION))
        self.board.append(list(WALL_LOCATION + WALL_LOCATION * columns + TOWER))
        
        self.rooftops = {}
        
        for name in player_names:
            roofotps[name] = []
        rooftops[NEUTRAL_PLAYER] = []
        
    def __getitem__(self, (row, column)):
        """Gets an element from the board at a specified row and column.
        
        Args:
            (row, column): Row and columon of element to check
            
        Returns:
            The element located at the position of (row, column)
            
        Raises:
            AssertionError: row and column must both be non-negative integers.
        """
        assert type(row) == int, "Row is not an integer, %r" % row
        assert type(column) == int, "Column is not an integer %r" % column
        assert row >= 0, "Row must be a non-negative number %r" % row    
        assert column >= 0, "Column must be a non-negative number %r" % column
        return self.board[row][column]
    
    def __setitem__(self, (row, column), element):
        """Sets an element at a specified location.
        
        Args:
            row: Row and Column of element to set
            element: Value to place into position (row, column)
        
        Returns:
            The element that was previously at the location row, column.
            
        Raises:
            AssertionError: row and column must both be non-negative integers.
        """
        assert type(row) == int, "Row is not an integer, %r" % row
        assert type(column) == int, "Column is not an integer %r" % column
        assert row >= 0, "Row must be a non-negative number %r" % row    
        assert column >= 0, "Column must be a non-negative number %r" % column
        temp = self.get(row, column)
        self.board[row][column] = element;
        return temp;
  
    def num_rows(self):
        """Gets the number of rows of this board (including the walls)"""
        return self.rows
    
    def num_columns(self):
        """Gets the number of columns of this board (including the walls)"""
        return self.columns

def class Player:
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
        for color : BUILDINGS_COLORS:
            buildings[color] = buildings_given[num_players]
        stables = stables_given[num_players]
        rooftops = rooftops_given[num_players]
        extra_rooftops = extra_rooftops_given[num_players]
        merchants = merchants_given[num_players]
        walls = walls_given[num_players]
    
def class Tile:
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
        return [Tile(TEA_TILE), for i in range(6)]
    
    TEA_TILE = 'TEA'
    TOWER_TILE = 'TOW'
    PALACE_TILE = 'PAL'
    
    PALACE_COLORS = {1:BUILDINGS_COLORS[0], 
        2:BUILDINGS_COLORS[1],
        3:BUILDINGS_COLORS[2],
        4:BUILDINGS_COLORS[3]}
    
    def __init__(self, type, value=0)
        """Creates a player with a given properties.
        
        Args:
            type: Type of tile: Tower, Palace, or Tea.
            value: Point value of the tile."""
        self.type = type
        self.value = value
        if type == TOWER_TILE:
            self.merchants = 4 - value
