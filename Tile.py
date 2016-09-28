"""Tiles should be held by players in the game and are worth points.

Tiles can be one of three types: Tower, Tea or Palace. Palace tiles are 
awarded for building the largest of a building color. Tower tiles are 
awarded for building a building connected to a wall from a tower. Tea tiles 
are awarded for claiming purple buildings.

If a tile is a tower tile, it will also hold merchants for the first player 
who claims the tile.

Tiles are saved as a dictionary of either two or three elements. 

type: Type of tile, Tea, Tower, or Palace.
value: Point value of the tile.
merchants: Only for Tower tiles, the number of merchants left on the 
    tile for players to pickup."""



BUILDINGS_COLORS = ['Grey', 'Violet', 'Brown', 'Orange']
"""Colors for different buildings: Grey, Violet, Brown, Orange""" 
BUILDINGS_COLORS_HEX = {'Grey': 'E2E2E2', 
                        'Violet': 'A70BAC',
                        'Brown': '4E2E03',
                        'Orange': 'FFD500'}
"""Colors of the buildings in HEX color codes, RRGGBB"""

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

def get_palace_tile_color(tile):
    """If a tile is a palace tile, this will get the string corresponding to 
    the name of the color as defined in BUILDINGS_COLORS."""
    assert get_tile_type(tile) == PALACE_TILE
    return BUILDINGS_COLORS[get_tile_value(tile) - 1]

def take_merchants(tile):
    """If the tile has merchants, this method will return the number of 
    merchants then set the number of merchants on the tile to zero."""
    num = get_num_merchants(tile)
    tile['merchants'] = 0
    return num

def make_tile(type, value=0):
    tile = dict()
    tile['type'] = type
    tile['value'] = value
    if type == TOWER_TILE:
        tile['merchants'] = 4 - value
    return tile
