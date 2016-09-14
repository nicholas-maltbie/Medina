"""This file will contain the code that represents the digital model of the 
game and can be refrenced by other parts of the project. This will contain 
mutable defenitions for all parts of the game.

Different parts of the game include:
    - Board
    - Players
    - Tiles

This file is not responsible for knowing the rules of the game, only for 
storing the data for the game and players."""

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
        {'player1' : [(0, 1), (6, 4)],
         'player2' : [(10, 5)],
         'player3' : [],
         'player4' : [(13, 3)]
        }
    
    Character Code Key:
        'e' = empty
        'l' = wall location     (not constructed)
        'c' = constructed wall
        's' = stable
        'w' = well              (One on the board)
        't' = tower             (One at each corner)
        'm' = merchant          (builds in a chain)
        '1', '2', ... '4' = buildings of color 1, 2, ... or 4
            - Specific colors are irellevant as long as there are four 
                distinct colors.
    
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
        l e m m m m e e 2 e e e e 1 e e e w
        l e e e e m m m 2 2 e w e 1 1 e e w
        l e e e e e e m m 2 e e e e e e e l
            ... more rows ...
        l e e 3 3 3 e e e e e e e e e e e l
        w e 3 3 3 3 e e e e e e e e e e e l
        t w w w w l l l l l l l l l l l l t
    

    Attributes:
        board: 2D array of characters to store walls, buildings and merchants.
        rooftops: Dictionary of rooftops played by players.
    """
    
    EMPTY = 'e'
    WALL_LOCATION = 'w'
    WALL = 'c'
    STABLE = 's'
    WELL = 'w'
    TOWER = 't'
    MERCHANT = 'm'
    
    def get_large_board():
        """Generates and returns a board for a game with 3 or four players"""
        return Board()
    
    def get_small_board():
        """Generates and returns a board for a game with 2 players"""
        return Board(10, 14)
    
    def __init__(self, rows = 11, columns = 16):
        """Creates a board and dictionary to store rooftops
        
        This will generate a 2D array for the number of rows + 2 and the number 
        of columns + 2 to allow space for the board and two more spaces for the 
        walls and towers on each edge of the board.
        
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
        
        self.rows = rows;
        self.columns = columns;
        
        self.board = [list('t' + 'l' * columns + 't')]
        for i in range(0, rows):
            self.board.append(list('l' + 'e' * columns + 'l'))
        self.board.append(list('t' + 'l' * columns + 't'))
        
        self.rooftops = {}
        
    def get(self, row, column):
        """Gets an element from the board at a specified row and column.
        
        Args:
            row: Row to element to check
            column: Columon of element to check
            
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
    
    def set(self, row, column, element):
        """Sets an element at a specified location.
        
        Args:
            row: Row of element to set
            column: Column of element to set
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
    
    def get_rooftops(self, name):
        """Gets the rooftops owned by a player with a given name.
        
        Checks the rooftop dictionary and returns a list of tuples in the format 
        of (row, column) for the location of each rooftop that the player owns.
        
        Args:
            name: The name of the player.
            
        Returns:
            A list of tuples for each rooftop that the player owns or an empty 
            list if the player owns no rooftops yet.
        """
        if name in self.rooftops:
            return self.rooftops[name]
        return [];

    def add_rooftop(self, name, row, column):
        """Gives name a rooftop at location row, column.
        
        Checks if that player already owns rooftops. If so, adds the rooftops 
        to the player's list of owned rooftops. If the player does not own any 
        rooftops, the name will be added as a key to the dictionary of rooftops 
        and then the element will be added to the player's list of rooftops.
        
        Args:
            name: The name of the player.
            row: A non-negative number within the range of the board.
            column: A non-negative number within the range of the board.
        
        Raises:
            AssertionError: row and column must both be non-negative integers.
        """
        assert type(row) == int, "Row is not an integer, %r" % row
        assert type(column) == int, "Column is not an integer %r" % column
        assert row >= 0, "Row must be a non-negative number %r" % row    
        assert column >= 0, "Column must be a non-negative number %r" % column
        if not name in self.rooftops:
            self.rooftops[name] = []
        self.rooftops[name].append((row, column))

def class Player:
    """A Player needs to be able to hold pieces and have a name"""
    #Finish documentation
    pass
    
def class Tile:
    """Define different kinds of tiles here and describe. Tiles should be held 
    by players in the game"""
    #Finish documentation
    pass
