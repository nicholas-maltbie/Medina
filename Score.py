"""This module will determine player's score in a game given the board and
player"""

from Location import *
from Board import *
from Player import *
from Tile import *
from Building import *
import tkinter
from tkinter import messagebox

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
            score += get_num_walls_adjacent_to_building(board, building) #walls
            score += get_num_merchants_adjacent_to_building(board, building) #merchants

        return score

    return get_score

def displaySimpleScore(scores):
    """Creates a simple message dialog to diplay the score of players, scores
    is a dictionary of the player names : player scores"""
    scores_list = [(name, scores[name]) for name in scores]
    scores_list.sort(key=lambda a: -a[1])
    result = scores_list[0][0] + " has won the game" + "\n"
    for i in range(len(scores_list)):
        score = scores_list[i]
        result += str(i + 1) + ") " + score[0] + " " + str(score[1]) + "\n"
    tkinter.messagebox.showinfo(scores_list[0][0] + " Won", result)


def displayScores(players, board): #funtion that is called to display scores

    name = [None] * len(players) #name is a list that will hold player names
    for i in range(len(players)):
        name[i] = get_player_name(players[i])

    XPAD = 10 #x and y padding for the buttons
    YPAD = 5
    BUTTON_COLOR = "#07ba37"
    EXIT_COLOR = "white"
    BACK_COLOR = "white"

    root = tkinter.Tk() #root is the whole window
    root.title("Final Scores")
    root.geometry("300x200")
    root.configure(background = "#0781ba")

    app = tkinter.Frame(root) #app is the space the buttons go
    app.grid()
    app.configure(background = "#0781ba")



    def secondWindow(player): #second window opened to display specific scores

        def close_window(): #this function when called closes the extra window
            root2.destroy()

        root2 = tkinter.Tk()
        root2.title("Scores of " + get_player_name(player))
        root2.geometry("300x300")
        root2.configure(background = "#0781ba")

        app2 = tkinter.Frame(root2)
        app2.grid()
        app2.configure(background = "#0781ba")

        get_score = get_score_function(board)
        score = get_score(player)
        label1 = tkinter.Label(app2, text = str(score))
        label1.grid(row=1, sticky="W", padx = XPAD, pady = YPAD)

        buttonBack = tkinter.Button(app2, text = " Back to All Scores ", background = BACK_COLOR, command=close_window)
        buttonBack.grid(row=10, sticky="W", padx = XPAD, pady = YPAD)
        root2.mainloop()

    #These are the buttons on the main window that when clicked reveal each persons score
    button0 = tkinter.Button(app, text = " Reveal Scores of " + name[0], background = BUTTON_COLOR, command=lambda: secondWindow(players[0]))
    button0.grid(row=1, sticky="W", padx = XPAD, pady = YPAD)

    button1 = tkinter.Button(app, text = " Reveal Scores of " + name[1], background = BUTTON_COLOR, command=lambda: secondWindow(players[1]))
    button1.grid(row=2, sticky="W", padx = XPAD, pady = YPAD)

    button2 = tkinter.Button(app, text = " Reveal Scores of " + name[2], background = BUTTON_COLOR, command=lambda: secondWindow(players[2]))
    button2.grid(row=3, sticky="W", padx = XPAD, pady = YPAD)

    button3 = tkinter.Button(app, text = " Reveal Scores of " + name[3], background = BUTTON_COLOR, command=lambda: secondWindow(players[3]))
    button3.grid(row=4, sticky="W", padx = XPAD, pady = YPAD)

    buttonExit = tkinter.Button(app, text = " Exit ", background = EXIT_COLOR, command=exit)
    buttonExit.grid(row=5, sticky="W", padx = XPAD, pady = YPAD)

    root.mainloop()

if __name__ == "__main__": #test function only executed if Score.py is main
    board = make_board(11, 16)
    player = make_player("Nick", 4, "Green")
    give_tile(player, make_tile(PALACE_TILE, 4))
    get_score = get_score_function(board)
    score = get_score(player)
    print(score)
