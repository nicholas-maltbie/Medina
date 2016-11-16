"""This class is responsible for making and managing a board canvas that
will draw an interactive board and allow players to move elements onto the
board. """

import tkinter
import Board
import Location
import Market
from GameConstants import *

"""Size for the wall locations"""
WALL_WIDTH = 30
"""Size of each grid square in pixels"""
GRID_SIZE = 40
"""Size of the gap between grid locations"""
GRID_GAP = 10

#Load different images
BUILDING_IMAGES = {}
WALL_IMAGES = []

class BoardCanvas(tkinter.Tk):
    def __init__(self, board):
        tkinter.Tk.__init__(self)
        self.can = tkinter.Canvas(width=(GRID_SIZE * 3 + GRID_SIZE * Board.get_columns(board) + GRID_GAP * (Board.get_columns(board) + 2)),
            height=(GRID_SIZE * 3 + GRID_SIZE * Board.get_rows(board) + GRID_GAP * (Board.get_rows(board) + 2)))

        self.drag_data = drag_data = {"x": 0, "y": 0, "item": None}
        self.board = board
        self.can.pack()

        self.tower_image = tkinter.PhotoImage(file="Assets/Tower.gif")
        self.tower_image = self.tower_image.subsample(self.tower_image.width() // GRID_SIZE, self.tower_image.height() // GRID_SIZE)
        self.well_image = tkinter.PhotoImage(file = "Assets/Well.gif")
        self.well_image = self.well_image.subsample(self.well_image.width() // GRID_SIZE, self.well_image.height() // GRID_SIZE)
        self.merchant_image = None

        if BUILDING_IMAGES == {}:
            for color in BUILDINGS_COLORS:
                img = tkinter.PhotoImage(file="Assets/Building_" + color[0] + ".gif")
                BUILDING_IMAGES[color] = img.subsample(img.width() // GRID_SIZE, img.height() // GRID_SIZE)
            img = tkinter.PhotoImage(file="Assets/Wall_North.gif")
            WALL_IMAGES.append(img.subsample(img.width() // (GRID_SIZE + GRID_GAP + 2), img.height() // (WALL_WIDTH)))
            img = tkinter.PhotoImage(file="Assets/Wall_South.gif")
            WALL_IMAGES.append(img.subsample(img.width() // (GRID_SIZE + GRID_GAP + 2), img.height() // (WALL_WIDTH)))
            
            img = tkinter.PhotoImage(file="Assets/Wall_East.gif")
            WALL_IMAGES.append(img.subsample(img.width() // (WALL_WIDTH), img.height() // (GRID_SIZE + GRID_GAP + 2)))
            img = tkinter.PhotoImage(file="Assets/Wall_West.gif")
            WALL_IMAGES.append(img.subsample(img.width() // (WALL_WIDTH), img.height() // (GRID_SIZE + GRID_GAP + 2)))

        rows = Board.get_rows(self.board)
        columns = Board.get_columns(self.board)

        max_x = GRID_GAP * (columns) + GRID_SIZE * (columns + 1)
        max_y = GRID_GAP * (rows) + GRID_SIZE * (rows + 1)

        self.offx, self.offy = GRID_SIZE + GRID_GAP * 2, GRID_SIZE * 2 + GRID_GAP

        self.columns = Board.get_columns(board)
        self.rows = Board.get_rows(board)

        self.draw_grid_lines()

        self.can.tag_bind("token", "<ButtonPress-1>", self.OnTokenButtonPress)
        self.can.tag_bind("token", "<ButtonRelease-1>", self.OnTokenButtonRelease)
        self.can.tag_bind("token", "<B1-Motion>", self.OnTokenMotion)

    def setup(self):
        board = self.board
        if self.merchant_image == None:
            self.merchant_image = tkinter.PhotoImage(file = "Assets/Merchant.gif")
            self.merchant_image = self.merchant_image.subsample(self.merchant_image.width() // GRID_SIZE, self.merchant_image.height() // GRID_SIZE)

        board = self.board
        self.elements = [[None] * Board.get_columns(board)] * Board.get_rows(board);

        self.towers = []
        for i in range(1, 5):
            self.can.create_image(self.get_tower_pixels(i), image = self.tower_image)
        well = Board.get_well(self.board)
        self.well = self.can.create_image(self.get_board_pixels(well), image = self.well_image)
        self.add_merchant_to_grid(Market.get_active_market_street(Board.get_market(self.board))[0])

    def add_merchant_to_grid(self, location):
        """Adds a merchant to a specified location on the grid"""
        print(location)
        return self.can.create_image(self.get_board_pixels(location), image= self.merchant_image)

    def add_wall_to_grid(self, side, index):
        """Adds a static wall to the grid. Wall is the wall, wall 'N' is
        the north wall, wall 'W' is the west wall, wall 'E' is east wall, wall
        'S' is the south wall. index is the index of the wall, 0 is either top
        or leftmost wall."""
        if side == 'N':
            return self.can.create_image(self.get_wall_pixels(side, index), image=WALL_IMAGES[0])
        elif side == 'S':
            return self.can.create_image(self.get_wall_pixels(side, index), image=WALL_IMAGES[1])
        elif side == 'E':
            return self.can.create_image(self.get_wall_pixels(side, index), image=WALL_IMAGES[2])
        elif side == 'W':
            return self.can.create_image(self.get_wall_pixels(side, index), image=WALL_IMAGES[3])

    def get_board_pixels(self, location):
        """Gets the center of an grid square for a specific Location for the
        board returned as (x, y)"""
        col = Location.get_column(location)
        row = Location.get_row(location)
        return self.offx + col * (GRID_SIZE + 2) + (col + 1) * GRID_GAP, \
                self.offy + row * (GRID_SIZE  + 2) + (row + 1) * GRID_GAP

    def add_building_to_grid(self, color, location):
        """Adds a bulding graphic to the board at a specified location"""
        return self.can.create_image(self.get_board_pixels(location), image=BUILDING_IMAGES[color])

    def get_wall_pixels(self, wall, index):
        """Gets the center of a wall location. Wall is the wall, wall 'N' is
        the north wall, wall 'W' is the west wall, wall 'E' is east wall, wall
        'S' is the south wall. index is the index of the wall, 0 is either top
        or leftmost wall."""
        if wall == 'N':
            x, y = self.get_board_pixels(Location.make_location(-1, index));
            return x, y
        if wall == 'E':
            x, y = self.get_board_pixels(Location.make_location(index, self.columns));
            return x, y
        if wall == 'S':
            x, y = self.get_board_pixels(Location.make_location(self.rows, index));
            return x, y
        if wall == 'W':
            x, y = self.get_board_pixels(Location.make_location(index, -1));
            return x, y

    def get_tower_pixels(self, tower_number):
        """Gets the center of a tower given the tower number"""
        if tower_number == 1:
            x, y = self.get_board_pixels(Location.make_location(-1,-1))
            return x + (GRID_GAP) // 2, y + (GRID_GAP) // 2
        if tower_number == 2:
            x, y = self.get_board_pixels(Location.make_location(-1,self.columns))
            return x - (GRID_GAP) // 2, y + (GRID_GAP) // 2
        if tower_number == 3:
            x, y = self.get_board_pixels(Location.make_location(self.rows,-1))
            return x + (GRID_GAP) // 2, y - (GRID_GAP) // 2
        if tower_number == 4:
            x, y = self.get_board_pixels(Location.make_location(self.rows,self.columns))
            return x - (GRID_GAP) // 2, y - (GRID_GAP) // 2

    def draw_grid_lines(self):
        """Draws lines for the different grid boxes on the screen"""
        for tower in range(1, 5):
            #Draw box for towers
            x, y = self.get_tower_pixels(tower)
            self.can.create_line(x - GRID_SIZE // 2, y - GRID_SIZE // 2,
                    x + GRID_SIZE // 2, y - GRID_SIZE // 2)
            self.can.create_line(x - GRID_SIZE // 2, y - GRID_SIZE // 2,
                    x - GRID_SIZE // 2, y + GRID_SIZE // 2)
            self.can.create_line(x + GRID_SIZE // 2, y - GRID_SIZE // 2,
                    x + GRID_SIZE // 2, y + GRID_SIZE // 2)
            self.can.create_line(x - GRID_SIZE // 2, y + GRID_SIZE // 2,
                    x + GRID_SIZE // 2, y + GRID_SIZE // 2)


        x1,y1 = self.get_board_pixels(Location.make_location(0,0))
        x2,y2 = self.get_board_pixels(Location.make_location(self.rows, self.columns))
        self.can.create_line(x1 - (GRID_SIZE + GRID_GAP) // 2, \
                y1 - (GRID_SIZE + GRID_GAP) // 2 - WALL_WIDTH, \
                x2 - (GRID_SIZE + GRID_GAP) // 2, \
                y1 - (GRID_SIZE + GRID_GAP) // 2 - WALL_WIDTH)
        self.can.create_line(x1 - (GRID_SIZE + GRID_GAP) // 2, \
                y2 - (GRID_SIZE + GRID_GAP) // 2 + WALL_WIDTH, \
                x2 - (GRID_SIZE + GRID_GAP) // 2, \
                y2 - (GRID_SIZE + GRID_GAP) // 2 + WALL_WIDTH)
        self.can.create_line(x1 - (GRID_SIZE + GRID_GAP) // 2 - WALL_WIDTH, \
                y1 - (GRID_SIZE + GRID_GAP) // 2, \
                x1 - (GRID_SIZE + GRID_GAP) // 2 - WALL_WIDTH, \
                y2 - (GRID_SIZE + GRID_GAP) // 2)
        self.can.create_line(x2 - (GRID_SIZE + GRID_GAP) // 2 + WALL_WIDTH, \
                y1 - (GRID_SIZE + GRID_GAP) // 2, \
                x2 - (GRID_SIZE + GRID_GAP) // 2 + WALL_WIDTH, \
                y2 - (GRID_SIZE + GRID_GAP) // 2)

        for row in range(0, self.rows + 1):
            x1,y1 = self.get_board_pixels(Location.make_location(row, 0))
            x2,y2 = self.get_board_pixels(Location.make_location(row, self.columns))
            self.can.create_line(x1 - (GRID_SIZE + GRID_GAP) // 2 - WALL_WIDTH,y1 - (GRID_SIZE + GRID_GAP) // 2, \
                    x2 - (GRID_SIZE + GRID_GAP) // 2 + WALL_WIDTH,y2 - (GRID_SIZE + GRID_GAP) // 2)
        for column in range(0, self.columns + 1):
            x1,y1 = self.get_board_pixels(Location.make_location(0, column))
            x2,y2 = self.get_board_pixels(Location.make_location(self.rows, column))
            self.can.create_line(x1 - (GRID_SIZE + GRID_GAP) // 2,y1 - (GRID_SIZE + GRID_GAP) // 2 - WALL_WIDTH, \
                    x2 - (GRID_SIZE + GRID_GAP) // 2,y2 - (GRID_SIZE + GRID_GAP) // 2 + WALL_WIDTH)

    def add_moveable_building(self, color, coords):
        """Adds a moveable building of a specified color at an x and y"""
        return self.can.create_image(coords, image=BUILDING_IMAGES[color], tags="token")

    def OnTokenButtonPress(self, event):
        '''Being drag of an object'''
        # record the item and its location
        can = self.can
        self.drag_data["item"] = can.find_closest(event.x, event.y)[0]
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def OnTokenButtonRelease(self, event):
        '''End drag of an object'''
        # reset the drag information
        can = self.can
        self.drag_data["item"] = None
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0

    def OnTokenMotion(self, event):
        '''Handle dragging of an object'''
        # compute how much this object has moved
        can = self.can
        delta_x = event.x - self.drag_data["x"]
        delta_y = event.y - self.drag_data["y"]
        # move the object the appropriate amount
        can.move(self.drag_data["item"], delta_x, delta_y)
        # record the new position
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

if __name__ == "__main__":
    board_canvas = BoardCanvas(Board.make_board(11,16))
    board_canvas.setup()
    built = []
    built.append(board_canvas.add_building_to_grid(BUILDINGS_COLORS[0], Location.make_location(0,0)))
    built.append(board_canvas.add_building_to_grid(BUILDINGS_COLORS[0], Location.make_location(0,1)))
    built.append(board_canvas.add_building_to_grid(BUILDINGS_COLORS[0], Location.make_location(1,0)))
    built.append(board_canvas.add_building_to_grid(BUILDINGS_COLORS[3], Location.make_location(10,15)))
    built.append(board_canvas.add_wall_to_grid('S', 0))
    built.append(board_canvas.add_wall_to_grid('S', 1))
    built.append(board_canvas.add_wall_to_grid('S', 2))
    built.append(board_canvas.add_wall_to_grid('S', 3))
    built.append(board_canvas.add_wall_to_grid('W', 9))
    built.append(board_canvas.add_wall_to_grid('W', 10))
    built.append(board_canvas.add_wall_to_grid('N', 15))
    built.append(board_canvas.add_wall_to_grid('E', 10))
    print(built)
    board_canvas.mainloop()
