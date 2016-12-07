"""There are four towers in the Medina board game. Each tower starts at a corner
of the board and the towers have walls that branch off of them. The walls
must have a gap left between them called a gate. Additionally, each tower
has a Tower Tile associated with them. The different towers are numbered,
the tower in the top left is tower 1, the tower in the top right is 2,
the tower in the bottom left is 3, the tower in the bottom right is 4. Each
tower is saved as its value and the length of the walls streching out from
each side of the tower. Additionally, the towers must know the length and the
columns of the board so there is always room for a gate."""

from Location import *

def make_towers(rows, columns):
    """This method will make a the towers for a game with the towers
    numbered 1, 2, 3, and 4."""
    return {'rows': rows, 'columns': columns, 'towers': [make_tower(i + 1) for i in range(0, 4)]}

def clone_towers(towers):
    """Clones a group of towers"""
    return {'rows': get_rows(towers), 'columns': get_columns(towers), \
            'towers':[clone_tower(get_tower(towers, i)) for i in range(1, 5)]}

def get_rows(towers):
    """Gets the rows of the board for towers."""
    return towers['rows']

def get_columns(towers):
    """Gets the columns of the board for towers."""
    return towers['columns']

def get_wall_locations_for_tower(towers, num):
    """Gets all the locations adjacent to a specific tower number."""
    walls = []
    h_mod = -1
    v_mod = -1
    if num == 0 or num == 2:
        h_mod = 1
    if num == 0 or num == 1:
        v_mod = 1
    start = make_location(-1, -1)
    if num == 1:
        start = make_location(-1, get_columns(towers))
    elif num == 2:
        start = make_location(get_rows(towers), -1)
    elif num == 3:
        start = make_location(get_rows(towers), get_columns(towers))
    tower = get_tower(towers, num + 1)
    for wall in range(get_tower_wall_h(tower)):
        walls.append(get_translate(start, 0, h_mod * (wall + 1)))
    for wall in range(get_tower_wall_v(tower)):
        walls.append(get_translate(start, v_mod * (wall + 1), 0))

    return walls

def get_wall_locations(towers):
    """Gets the locations of all walls attached to the towers. The wall locations
    are outside of the bounds of the board, they will strech from -1 to the number
    of rows and the number of columns."""
    walls = []
    for num in range(4):
        walls.extend(get_wall_locations_for_tower(towers, num))
    return walls

def get_structures(towers):
    """Gets the list of towers from a tower structure made by make_towers"""
    return towers['towers']

def get_tower(towers, tower_number):
    """Gets a tower of a specific number from towers"""
    assert 1 <= tower_number <= 4
    return get_structures(towers)[tower_number - 1]

def add_tower_r(tower):
    """Adds one to a tower's row size."""
    tower['builtV'] += 1

def add_tower_c(tower):
    """Adds one to a tower's column size."""
    tower['builtH'] += 1;

def get_possible_wall_additions(towers):
    """Gets all the possible addtions from each tower."""
    possible = []
    for i in range(1, 5):
        if can_add_c(towers, i):
            possible.append(get_tower_addition_c(towers, i))
        if can_add_r(towers, i):
            possible.append(get_tower_addition_r(towers, i))
    return possible

def can_add_c(towers, tower_number):
    """Checks if an addition can be made to a tower on the horizontal wall.
    tower_number must be between 1 and 4 (inclusive both)"""
    assert 1 <= tower_number <= 4
    if tower_number % 2 == 0:
        return get_tower_wall_h(get_tower(towers, tower_number)) + \
            get_tower_wall_h(get_tower(towers, tower_number - 1)) < get_columns(towers) - 1
    else:
        return get_tower_wall_h(get_tower(towers, tower_number)) + \
            get_tower_wall_h(get_tower(towers, tower_number + 1)) < get_columns(towers) - 1

def can_add_r(towers, tower_number):
    """Checks if an addition can be made to a tower on the vertical wall.
    tower_number must be between 1 and 4 (inclusive both)"""
    assert 1 <= tower_number <= 4
    if tower_number <= 2:
        return get_tower_wall_v(get_tower(towers, tower_number)) + \
            get_tower_wall_v(get_tower(towers, tower_number + 2)) < get_rows(towers) - 1
    else:
        return get_tower_wall_v(get_tower(towers, tower_number)) + \
            get_tower_wall_v(get_tower(towers, tower_number - 2)) < get_rows(towers) - 1

def get_tower_addition_r(towers, num):
    """Gets the locaiton of the next tower addition for the rows of this tower.
    This does not check the validity of a move."""
    tower = get_tower(towers, num)
    num -= 1
    v_mod = -1
    if num == 0 or num == 1:
        v_mod = 1
    start = make_location(-1, -1)
    if num == 1:
        start = make_location(-1, get_columns(towers))
    elif num == 2:
        start = make_location(get_rows(towers), -1)
    elif num == 3:
        start = make_location(get_rows(towers), get_columns(towers))
    return get_translate(start, v_mod * (get_tower_wall_v(tower) + 1), 0)

def get_tower_addition_c(towers, num):
    """Gets the location of the next towe raddition for the columns of this tower.
    This does not check the validity of a move."""
    tower = get_tower(towers, num)
    h_mod = -1
    num -= 1
    if num == 0 or num == 2:
        h_mod = 1
    start = make_location(-1, -1)
    if num == 1:
        start = make_location(-1, get_columns(towers))
    elif num == 2:
        start = make_location(get_rows(towers), -1)
    elif num == 3:
        start = make_location(get_rows(towers), get_columns(towers))
    return get_translate(start, 0, h_mod * (get_tower_wall_h(tower) + 1))

def make_tower(number):
    """Creates a tower with a given number."""
    return {'builtV': 0, 'builtH': 0, 'number':number}

def clone_tower(tower):
    """Clones a tower"""
    return tower.copy()

def get_tower_wall_v(tower):
    """Gets the rows of a tower's verticial wall."""
    return tower['builtV']

def get_tower_wall_h(tower):
    """Gets the rows of a tower's horizontal wall."""
    return tower['builtH']

def get_tower_number(tower):
    """Gets a tower's number."""
    return tower['builtV']
