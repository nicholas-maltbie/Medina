"""This module will determine player's score in a game given the board and 
player"""

from Location import *
from Board import *
from Player import *
from Tile import *
from Building import *
from TestGame import *

bonusLocations = get_double_orthogonal(well_location)
 
def get_score(board, player):
    """Score from tiles"""
    """Palace Tiles, Tower Tiles"""
    score = 0
    
    palaceTiles = get_tiles_of_type(player, PALACE_TILE)
    towerTiles = get_tiles_of_type(player, TOWER_TILE)
    for tile in palaceTiles + towerTiles:
        score += get_tile_value(tile)
        
    """Score from buildings"""
    """Stables, Well points, Walls, Merchants"""
    
    buildingsThePlayerOwns = get_buildings_claimed_by(board, get_player_name(player)) #gets a list of all the buildings the player has
    for building in buildingsThePlayerOwns: #for each building the player has
        locations = get_building_locations(building)
        for locations in building: #for each square of the building
            score += 1 #add one because its part of a building (counts stables)
            if location == wellSpecialLocation
                score += 4
        score += get_num_walls_adjacent_to_building(board, building)
        score += get_num_merchants_adjacent_to_building(board, building)
        

get_score(board, player)
    