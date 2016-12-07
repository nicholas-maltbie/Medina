"""This module will determine player's score in a game given the board and 
player"""

from Location import *
from Board import *
from Player import *
from Tile import *
from Building import *


def get_score_function(board):
    well_location = get_well(board)
    bonusLocations = set(get_double_orthogonal(well_location))
    def get_score(player):
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
            locations = get_building_and_stables(building)
            for loc in locations: #for each square of the building
                score += 1 #add one because its part of a building (counts stables)
                if loc in bonusLocations:
                    score += 4
            score += get_num_walls_adjacent_to_building(board, building)
            score += get_num_merchants_adjacent_to_building(board, building)
            
        return score
    
    return get_score

if __name__ == "__main__": #test function only executed if Score.py is main
    board = make_board(11, 16)
    player = make_player("Nick", 4, "Green")
    give_tile(player, make_tile(PALACE_TILE, 4))
    get_score = get_score_function(board)
    score = get_score(player)
    print(score)