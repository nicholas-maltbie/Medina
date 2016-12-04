from Tile import *

"""A Player needs to be able to hold pieces and have a name.

    A player plays games in medina and is responsible to hold pieces and be
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
        rooftops: Number of rooftops the player has.
        extra_rooftops: Number of extra rooftops given.
        merchants: Number of merchants the player has.
        walls: The number of walls the player has.
        tiles: Tiles the player has acquired."""

BUILDINGS_GIVEN = {2:8,3:6,4:5}
#Buildings given to each player depending on game size))
ROOFTOPS_GIVEN = {2:4,3:4,4:4}
#Rooftops given to each player
EXTRA_ROOFTOPS_GIVEN = {2:2, 3:1, 4:0}
#Neutral rooftops given to players
STABLES_GIVEN = {2:4, 3:4, 4:3}
#Number of stables given to players
MERCHANTS_GIVEN = {2:12, 3:8, 4:6}
#Number of merchants given to players
WALLS_GIVEN = {2:15, 3:12, 4:9}
#Number of walls given to players

def make_player(name, num_players, player_color='Blue'):
    """This method will make a player for a given game size

    Args:
        name: Name of the player.
        num_players: Number of players in the game."""

    buildings = {};
    for color in BUILDINGS_COLORS:
        buildings[color] = BUILDINGS_GIVEN[num_players]
    return {'name':name, 'buildings':buildings, 'stables':STABLES_GIVEN[num_players],
        'rooftops':ROOFTOPS_GIVEN[num_players], 'extra':EXTRA_ROOFTOPS_GIVEN[num_players],
        'merchants':MERCHANTS_GIVEN[num_players], 'walls':WALLS_GIVEN[num_players],
        'tiles':[], 'color':player_color}

def clone_player(player):
    """Clones a player"""
    return {'name':get_player_name(player),'buildings':get_buildings(player).copy(),
            'stables':get_num_stables(player), 'rooftops':get_held_rooftops(player),
            'merchants':get_held_merchants(player),'walls': get_held_walls(player),
            'color':get_player_color(player),
            'tiles':[Tile.clone_tile(tile) for tile in get_tiles(player)]}

def get_num_stables(player):
    """Gets the number of stables a player has"""
    return player['stables']

def get_player_color(player):
    """Gets the color of a player"""
    return player['color']

def play_stable(player):
    """Plays a stable on the board"""
    players['stables'] -= 1

def get_player_name(player):
    """Gets the name of a player"""
    return player['name']

def get_held_buildings(player):
    """Gets the buildings held by a player"""
    return player['buildings']

def remvoe_all_buildings_of_color(player, color):
    """Removes all the buildings that a player has of a color"""
    get_held_buildings(player)[color] = 0

def play_building(player, color):
    """Decrements the number of buildings a player is holding of a specific
    color. If the player does not have any buildings of this color, an
    exception will be thrown."""
    assert get_held_buildings_of_color(player, color) > 0
    get_held_buildings(player)[color] -= 1

def get_held_buildings_of_color(player, color):
    """Gets the number buildings held by a player of a specific color"""
    return get_held_buildings(player)[color]

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
