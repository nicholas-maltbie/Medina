"""This class is responsible for making and managing a board canvas that 
will draw an interactive board and allow players to move elements onto the 
board. """

import tkinter
import Board
from GameConstants import *

GRID_WIDTH = 50
GRID_HEIGHT = 60
GRID_GAP = 10

#Load different images

BUILDING_IMAGES = {}
drag_data = {"x": 0, "y": 0, "item": None}

class BoardCanvas(tkinter.Tk):
    def __init__(self, board):
        tkinter.Tk.__init__(self)
        self.can = tkinter.Canvas(width=400, height=400)
        self.board = board
        self.can.pack()

        if BUILDING_IMAGES == {}:
            for color in BUILDINGS_COLORS:
                img = tkinter.PhotoImage(file="Assets/Building_" + color[0] + ".gif")
                BUILDING_IMAGES[color] = img.subsample(img.width() // GRID_WIDTH, img.height() // GRID_HEIGHT)
        
        self.can.tag_bind("token", "<ButtonPress-1>", self.OnTokenButtonPress)
        self.can.tag_bind("token", "<ButtonRelease-1>", self.OnTokenButtonRelease)
        self.can.tag_bind("token", "<B1-Motion>", self.OnTokenMotion)
        
    def add_moveable_building(self, color, coords):
        return self.can.create_image(coords, image=BUILDING_IMAGES[color], tags="token")

        
        
    def OnTokenButtonPress(self, event):
        '''Being drag of an object'''
        # record the item and its location
        can = self.can
        drag_data["item"] = can.find_closest(event.x, event.y)[0]
        drag_data["x"] = event.x
        drag_data["y"] = event.y

    def OnTokenButtonRelease(self, event):
        '''End drag of an object'''
        # reset the drag information
        can = self.can
        drag_data["item"] = None
        drag_data["x"] = 0
        drag_data["y"] = 0

    def OnTokenMotion(self, event):
        '''Handle dragging of an object'''
        # compute how much this object has moved
        can = self.can
        delta_x = event.x - drag_data["x"]
        delta_y = event.y - drag_data["y"]
        # move the object the appropriate amount
        can.move(drag_data["item"], delta_x, delta_y)
        # record the new position
        drag_data["x"] = event.x
        drag_data["y"] = event.y

if __name__ == "__main__":
    board_canvas = BoardCanvas(Board.make_board(10,10))
    board_canvas.add_moveable_building(BUILDINGS_COLORS[0], (50, 50))
    board_canvas.add_moveable_building(BUILDINGS_COLORS[1], (110, 50))
    board_canvas.add_moveable_building(BUILDINGS_COLORS[2], (170, 50))
    board_canvas.add_moveable_building(BUILDINGS_COLORS[3], (230, 50))
    board_canvas.mainloop()

