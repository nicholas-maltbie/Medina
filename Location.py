"""A location is a place within the game board that has a row and column

Locations are used to reference different board elements"""

def make_location(row, column):
    """This method creates a location with a given row and column"""
    return (row, column)
    
def get_row(location):
    """Gets the row of a location"""
    return location[0]
    
def get_column(location):
    """Gets the column of a location"""
    return location[1]

def get_translate(location, rows, columns):
    """Gets a new location that is location translated rows and columns."""
    return make_location(get_row(location) + rows, get_column(location) + columns);

def get_adjacent(location):
    """Gets the eight adjacent spots to a location"""
    row = get_row(location)
    column = get_column(location)
    return [make_location(row - 1, column - 1), make_location(row - 1, column), 
        make_location(row - 1, column + 1), make_location(row, column + 1), 
        make_location(row + 1, column + 1), make_location(row + 1, column), 
        make_location(row + 1, column - 1), make_location(row, column - 1)]

def get_adjacent_within_bounds(location, max_row, max_column, min_row = 0, min_column = 0):
    """Gets the adjacent locations filtering out those that are not within 
    bounds as defined in is_within_bounds."""
    return [loc for loc in get_adjacent(location) if is_within_bounds(loc, \
            max_row, max_column, min_row, min_column)]

def get_orthogonal(location):
    """Gets the four orthogonally adjacent spots to a location"""
    row = get_row(location)
    column = get_column(location)
    return [make_location(row - 1, column), make_location(row, column + 1),
        make_location(row + 1, column), make_location(row, column - 1)]

def get_orthogonal_within_bounds(location, max_row, max_column, min_row = 0, min_column = 0):
    """Gets the orthogonally adjacent locations filtering out those that are not
     within bounds as defined in is_within_bounds."""
    return [loc for loc in get_orthogonal(location) if is_within_bounds(loc, \
            max_row, max_column, min_row, min_column)]

def is_within_bounds(location, max_row, max_column, min_row = 0, min_column = 0):
    """Checks if a location is within a specified bounds (inclusive on min 
    bound and exclusive on max bound)
        min_row <= row < max_row and 
        min_column <= column < max_column"""
    return min_row <= get_row(location) < max_row and \
            min_column <= get_column(location) < max_column
