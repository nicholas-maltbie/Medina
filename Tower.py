"""There are four towers in the Medina board game. Each tower starts at a corner 
of the board and the towers have walls that branch off of them. The walls 
must have a gap left between them called a gate. Additionally, each tower 
has a Tower Tile associated with them. The different towers are numbered, 
the tower in the top left is tower 1, the tower in the top right is 2,
the tower in the bottom left is 3, the tower in the bottom right is 4. Each 
tower is saved as its value and the length of the walls streching out from 
each side of the tower. Additionally, the towers must know the length and the 
columns of the board so there is always room for a gate."""

def make_towers(rows, columns):
    """This method will make a the towers for a game with the towers 
    numbered 1, 2, 3, and 4."""
    return {'rows': rows, 'columns': columns, 'towers': [make_tower(i + 1) for i in range(0, 4)]}

def get_rows(towers):
    """Gets the rows of the board for towers."""
    return towers['rows']
    
def get_columns(towers):
    """Gets the columns of the board for towers."""
    return towers['columns']

def get_structures(towers):
    """Gets the list of towers from a tower structure made by make_towers"""
    return towers['towers']

def get_tower(towers, tower_number):
    """Gets a tower of a specific number from towers"""
    assert 1 <= tower_number <= 4
    return get_structures(towers)[tower_number - 1]

def can_add_c(towers, tower_number):
    """Checks if an addition can be made to a tower on the horizontal wall. 
    tower_number must be between 1 and 4 (inclusive both)"""
    assert 1 <= tower_number <= 4
    if tower_number % 2 == 0:
        return get_tower_wall_h(get_tower(towers, tower_number)) + \
            get_tower_wall_h(get_tower(towers, tower_number - 1)) < get_rows(towers) - 1
    else:
        return get_tower_wall_h(get_tower(towers, tower_number)) + \
            get_tower_wall_h(get_tower(towers, tower_number + 1)) < get_rows(towers) - 1

def can_add_r(towers, tower_number):
    """Checks if an addition can be made to a tower on the vertical wall. 
    tower_number must be between 1 and 4 (inclusive both)"""
    assert 1 <= tower_number <= 4
    if tower_number <= 2:
        return get_tower_wall_v(get_tower(towers, tower_number)) + \
            get_tower_wall_v(get_tower(towers, tower_number + 2)) < get_columns(towers) - 1
    else:
        return get_tower_wall_v(get_tower(towers, tower_number)) + \
            get_tower_wall_v(get_tower(towers, tower_number - 2)) < get_columns(towers) - 1
    
def make_tower(number):
    """Creates a tower with a given number."""
    return {'builtV': 0, 'builtH': 0, 'number':number}

def get_tower_wall_v(tower):
    """Gets the rows of a tower's verticial wall."""
    return tower['builtV']
    
def get_tower_wall_h(tower):
    """Gets the rows of a tower's horizontal wall."""
    return tower['builtH']
    
def get_tower_number(tower):
    """Gets a tower's number."""
    return tower['builtV']
