"""This module will determine player's score in a game given the board and 
player"""

from Location import *
from Board import *
from Player import *
from Tile import *
from Building import *
import tkinter


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
    
def displayScore():
    root = tkinter.Tk()
    root.title("Final Scores")
    root.geometry("300x300")
    root.configure(background = "#0781ba")

    app = tkinter.Frame(root)
    app.grid()
    app.configure(background = "#0781ba")

    def secondWindow(name):
        root2 = tkinter.Tk()
        root2.title("Scores of " + name)
        root2.geometry("300x300")
        root2.configure(background = "#0781ba")
        
        app2 = tkinter.Frame(root2)
        app2.grid()
        app2.configure(background = "#0781ba")
        
        buttonExit = tkinter.Button(app2, text = " Exit " , command=exit)
        buttonExit.grid(row=2, sticky="W", padx = XPAD, pady = YPAD)
        root2.mainloop()
        
    name1 = "Nick and all of his friends"
    XPAD = 10
    YPAD = 5

    button1 = tkinter.Button(app, text = " Reveal Scores of " + name1, background = "#ccaa00", command=lambda: secondWindow(name1))
    button1.grid(row=1, sticky="W", padx = XPAD, pady = YPAD)

    buttonExit = tkinter.Button(app, text = " Exit " , command=exit)
    buttonExit.grid(row=2, sticky="W", padx = XPAD, pady = YPAD)

    root.mainloop()

if __name__ == "__main__": #test function only executed if Score.py is main
    board = make_board(11, 16)
    player = make_player("Nick", 4, "Green")
    give_tile(player, make_tile(PALACE_TILE, 4))
    get_score = get_score_function(board)
    score = get_score(player)
    print(score)