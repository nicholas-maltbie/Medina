"""This file will contain the code that represents the digital model of the 
game and can be refrenced by other parts of the project.

Different parts of the game include:
    - Board
    - Players
    - Tiles
    
    A board inclues multiple elements, buildings (contigious blocks of 
    building pieces and stables), a market street (or streets), towers with 
    walls branching off them, and a well.
"""

def make_location(row, column):
    """A location is a place within the game board that has a row and column
    
    Locations are used to reference different board elements"""
    return (row, column)
    
def get_row(location):
    """Gets the row of a location"""
    return location[0]
    
def get_column(location):
    """Gets the column of a location"""
    return location[1]

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

def make_building(color, start):
    """Makes a building of a given color starting at a location. A building is 
    a saved set of locations on a board and has a color and possibly an owner. 
    A building also includes the locations of attached stables."""
    return {'color':color, 'locations':[start], 'stables':[], 'owner':None}

def get_building_color(building):
    """Gets the color of a building"""
    return building['color']

def get_building_locations(building):
    """Gets all the locations a building pieces occupies."""
    return building['locations']

def attach_building_locations(building, location):
    """Attaches a building piece to the buliding. The building must no be 
    claimed in order to attach building segments."""
    assert not has_owner(building)
    get_building_locations(building).append(location)

def get_stable_locations(building):
    """Gets all the stables attached to a building"""
    return building['stables']

def attach_stable_location(building, location):
    """Attaches a building piece to a building."""
    get_stable_locations(building).append(location)
    
def get_owner(building):
    """Gets the owner of a building."""
    return building['owner']

def has_owner(building):
    """Checks if a building has an owner."""
    return get_owner(building) != None

def assign_owner(building, player):
    """Sets the owner of a building. The building must not have an owner to be 
    claimed."""
    assert not has_owner(building)
    building['owner'] = player

BUILDINGS_COLORS = ['Grey', 'Violet', 'Brown', 'Orange']
"""Colors for different buildings: Grey, Violet, Brown, Orange""" 
BUILDINGS_COLORS_HEX = {'Grey': 'E2E2E2', 
                        'Violet': 'A70BAC',
                        'Brown': '4E2E03',
                        'Orange': 'FFD500'}
"""Colors of the buildings in HEX color codes, RRGGBB"""

BUILDINGS_GIVEN = {2:8,3:6,4:5} 
#Buildings given to each player depending on game size
ROOFTOPS_GIVEN = {2:4,3:4,5:4}
#Rooftops given to each player
EXTRA_ROOFTOPS_GIVEN = {2:2, 3:1, 4:0}
#Neutral rooftops given to players
STABLES_GIVEN = {2:4, 3:4, 4:3}
#Number of stables given to players
MERCHANTS_GIVEN = {2:12, 3:8, 4:6}
#Number of merchants given to players
WALLS_GIVEN = {2:15, 3:12, 4:9}
#Number of walls given to players

def make_player(name, num_players):
    """A Player needs to be able to hold pieces and have a name.
    
    A player plays games in medina and is responsible to hold pieces and be 
    identifyable on the board.
    
    Args:
        name: Name of the player.
        num_players: Number of players in the game.
    
    Attributes:
        name: Name of the player.
        buildings: Dictionary of number of buildings for each color building
             the player owns. Dictionary is in the format of:
            {Building_color: num_held,
                Building_color2: num_hel2,
                ...
            }
        stables: Number of stables the player has.
        rooftops: Number of rooftops the player has.
        extra_rooftops: Number of extra rooftops given.
        merchants: Number of merchants the player has.
        walls: The number of walls the player has.
        tiles: Tiles the player has acquired."""
    
    buildings = {};
    for color in BUILDINGS_COLORS:
        buildings[color] = BUILDINGS_GIVEN[num_players]
    return {'name':name, 'buildings':buildings, 'stables':STABLES_GIVEN[num_players],
        'rooftops':ROOFTOPS_GIVEN[num_players], 'extra':EXTRA_ROOFTOPS_GIVEN[num_players],
        'merchants':MERCHANTS_GIVEN[num_players], 'walls':WALLS_GIVEN[num_players],
        'tiles':[]}

def get_player_name(player):
    """Gets the name of a player"""
    return player['name']

def get_held_buildings(player):
    """Gets the buildings held by a player"""
    return player['buildings']

def play_building(player, color):
    """Decrements the number of buildings a player is holding of a specific 
    color. If the player does not have any buildings of this color, an 
    exception will be thrown."""
    assert get_held_buildings_of_color(player, color) > 0
    get_held_buildings(player)[color] -= 1

def get_held_buildings_of_color(player, color):
    """Gets the number buildings held by a player of a specific color"""
    return get_held_buildings[color]

def get_held_rooftops(player):
    """Gets the number of rooftops a player has of their own color"""
    return player['rooftops']

def play_rooftop(player):
    """Decrements the number of rooftops the player is holding. If the player 
    does not have any rooftops, an exception will be thrown."""
    assert get_held_rooftops(player) > 0
    player['rooftops'] -= 1

def get_extra_rooftops(player):
    """Gets the number of rooftops of a nuetral player holds"""
    return player['extra']
    
def play_extra(player):
    """Decrements the number of neutral rooftops the player is holding. If the 
    player does not have any neutral rooftops, an exception will be thrown."""
    assert get_extra_rooftops(player) > 0
    player['extra'] -= 1

def get_held_merchants(player):
    """Gets the number of merchants a player is holding"""
    return player['merchants']

def play_merchant(player):
    """Decrements the number of merchants a player is holding. If the player 
    does not have any merchatns, an exception will be thrown."""
    assert get_held_merchants(player) > 0
    player['merchants'] -= 1

def give_merchants(player, num_add):
    """Adds merchants to a player's pool of tokens."""
    player['merchants'] += num_add

def get_held_walls(player):
    """Gets the number of walls a player is holding"""
    return player['walls']

def play_wall(player):
    """Decrements the number of walls a player is holding. if the player does 
    not have any walls, an exception will be thrown."""
    assert get_held_walls(player) > 0
    player['walls'] -= 1

def get_tiles(player):
    """Gets the tiles held by a player."""
    return player['tiles']

def get_num_tiles(player):
    """Gets the number of tiles held by a player."""
    return len(get_tiles(player))
    
def lose_tile(player, tile_type, value):
    """Takes away one tile of type tile_type and value value from player. If 
    the player does not have any tiles of tile_type and value, nothing will 
    happen."""
    for tile in get_tiles(player):
        if get_tile_type(tile) == tile_type and get_tile_value(tile) == value:
            get_tiles(player).remove(tile)
            return

def give_tile(player, tile):
    """Gives a player a tile of tile_type and the player will gain the 
    merchatns on the tile if the tile is a TOWER_TILE with merchants left."""
    if get_tile_type(tile) == TOWER_TILE:
        give_merchants(player, take_merchants(tile))
    get_tiles(player).append(tile)

def get_tiles_of_type(player, tile_type):
    """Gets all the tiles of a given type that a player owns."""
    return [tile for tile in get_tiles(player) if get_tile_type(tile) == tile_type]
    
TEA_TILE = 'TEA'
TOWER_TILE = 'TOW'
PALACE_TILE = 'PAL'
    
PALACE_COLORS = {1:BUILDINGS_COLORS[0], 
    2:BUILDINGS_COLORS[1],
    3:BUILDINGS_COLORS[2],
    4:BUILDINGS_COLORS[3]}

def get_tower_tiles():
    """Gets all the tower tiles in the game"""
    return [make_tile(TOWER_TILE, value+1) for value in range(4)]

def get_palace_tiles():
    """Gets all the palace tiles in the game"""
    return [make_tile(PALACE_TILE, value+1) for value in range(4)]
    
def get_tea_tiles():
    """Gets all the tea tiles in the game"""
    return [make_tile(TEA_TILE) for i in range(6)]

def get_tile_type(tile):
    """Gets the type of a tile"""
    return tile['type']

def get_tile_value(tile):
    """Gets the value of a tile"""
    return tile['value']

def get_num_merchants(tile):
    """Gets the number of merchants on a tile. If the tile does not have a 
    merchants field, this will raise an exception."""
    assert 'merchants' in tile
    return tile['merchants']

def take_merchants(tile):
    """If the tile has merchants, this method will return the number of 
    merchants then set the number of merchants on the tile to zero."""
    num = get_num_merchants(tile)
    tile['merchants'] = 0
    return num

def make_tile(type, value=0):
    """Tiles should be held by players in the game and are worth points.
    
    Tiles can be one of three types: Tower, Tea or Palace. Palace tiles are 
    awarded for building the largest of a building color. Tower tiles are 
    awarded for building a building connected to a wall from a tower. Tea tiles 
    are awarded for claiming purple buildings.
    
    If a tile is a tower tile, it will also hold merchants for the first player 
    who claims the tile.
    
    Tiles are saved as a dictionary of either two or three elements. 
    
    Attributes:
        type: Type of tile, Tea, Tower, or Palace.
        value: Point value of the tile.
        merchants: Only for Tower tiles, the number of merchants left on the 
            tile for players to pickup."""
    tile = dict()
    tile['type'] = type
    tile['value'] = value
    if type == TOWER_TILE:
        tile['merchants'] = 4 - value

