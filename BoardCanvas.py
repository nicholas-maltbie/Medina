"""This class is responsible for making and managing a board canvas that
will draw an interactive board and allow players to move elements onto the
board. """

import tkinter
import Board
import Location
import Market
from GameConstants import *

"""Size for the wall and tower locations"""
TOWER_SIZE = 50
WALL_WIDTH = 30
"""Width of each grid square in pixels"""
GRID_WIDTH = 50
"""Height of each grid squrae in pixels"""
GRID_HEIGHT = 50
"""Size of the gap between grid locations"""
GRID_GAP = 5

#Load different images
BUILDING_IMAGES = {}
WALL_IMAGES = []

class BoardCanvas(tkinter.Tk):
    def __init__(self, board):
        tkinter.Tk.__init__(self)
        self.can = tkinter.Canvas(width=(TOWER_SIZE * 2 + GRID_WIDTH * Board.get_columns(board) + GRID_GAP * (Board.get_columns(board) + 2)),
            height=(TOWER_SIZE * 2 + GRID_HEIGHT * Board.get_rows(board) + GRID_GAP * (Board.get_rows(board) + 2)))

        self.drag_data = drag_data = {"x": 0, "y": 0, "item": None}
        self.board = board
        self.can.pack()

        self.tower_image = tkinter.PhotoImage(file="Assets/Tower.gif")
        self.tower_image = self.tower_image.subsample(self.tower_image.width() // TOWER_SIZE, self.tower_image.height() // TOWER_SIZE)
        self.well_image = tkinter.PhotoImage(file = "Assets/Well.gif")
        self.well_image = self.well_image.subsample(self.well_image.width() // GRID_WIDTH, self.well_image.height() // GRID_HEIGHT)
        self.merchant_image = None

        if BUILDING_IMAGES == {}:
            for color in BUILDINGS_COLORS:
                img = tkinter.PhotoImage(file="Assets/Building_" + color[0] + ".gif")
                BUILDING_IMAGES[color] = img.subsample(img.width() // GRID_WIDTH, img.height() // GRID_HEIGHT)
            img = tkinter.PhotoImage(file="Assets/Wall_H.gif")
            WALL_IMAGES.append(img.subsample(img.width() // (GRID_WIDTH + GRID_GAP // 2), img.height() // WALL_WIDTH))
            img = tkinter.PhotoImage(file="Assets/Wall_V.gif")
            WALL_IMAGES.append(img.subsample(img.width() // WALL_WIDTH, img.height() // (GRID_HEIGHT + GRID_GAP // 2)))

        rows = Board.get_rows(self.board)
        columns = Board.get_columns(self.board)

        max_x = GRID_GAP * (columns) + GRID_WIDTH * (columns + 1) - WALL_WIDTH
        max_y = GRID_GAP * (rows) + GRID_HEIGHT * (rows + 1) - WALL_WIDTH

        self.offset_values = [(TOWER_SIZE, TOWER_SIZE), (max_x + GRID_GAP + GRID_WIDTH // 2 + TOWER_SIZE, TOWER_SIZE),
                (TOWER_SIZE, max_y + GRID_GAP + GRID_HEIGHT // 2 + TOWER_SIZE),
                (max_x + GRID_GAP + GRID_WIDTH // 2 + TOWER_SIZE, max_y + GRID_GAP + GRID_HEIGHT // 2 + TOWER_SIZE)]

        self.draw_grid_lines()

        self.can.tag_bind("token", "<ButtonPress-1>", self.OnTokenButtonPress)
        self.can.tag_bind("token", "<ButtonRelease-1>", self.OnTokenButtonRelease)
        self.can.tag_bind("token", "<B1-Motion>", self.OnTokenMotion)

    def setup(self):
        if self.merchant_image == None:
            self.merchant_image = tkinter.PhotoImage(file = "Assets/Merchant.gif")
            self.merchant_image = self.merchant_image.subsample(self.merchant_image.width() // GRID_WIDTH, self.merchant_image.height() // GRID_HEIGHT)

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
        if side == 'N' or side == 'S':
            return self.can.create_image(self.get_wall_pixels(side, index), image=WALL_IMAGES[0])
        if side == 'W' or side == 'E':
            return self.can.create_image(self.get_wall_pixels(side, index), image=WALL_IMAGES[1])

    def get_board_pixels(self, location):
        """Gets the center of an grid square for a specific Location for the
        board returned as (x, y)"""
        rows = Board.get_rows(self.board)
        columns = Board.get_columns(self.board)
        row = Location.get_row(location)
        column =  Location.get_column(location)
        return (TOWER_SIZE + GRID_GAP * (column + 1) + GRID_WIDTH * (column) + (GRID_WIDTH + GRID_GAP) // 2,
                TOWER_SIZE + GRID_GAP * (row + 1) + GRID_HEIGHT * (row) + (GRID_HEIGHT + GRID_GAP) // 2)

    def add_building_to_grid(self, color, location):
        """Adds a bulding graphic to the board at a specified location"""
        return self.can.create_image(self.get_board_pixels(location), image=BUILDING_IMAGES[color])

    def get_wall_pixels(self, wall, index):
        """Gets the cetner of a wall location. Wall is the wall, wall 'N' is
        the north wall, wall 'W' is the west wall, wall 'E' is east wall, wall
        'S' is the south wall. index is the index of the wall, 0 is either top
        or leftmost wall."""
        wall_size = (0,0)
        starting = (0,0)
        if wall == 'N':
            wall_size = (GRID_WIDTH + GRID_GAP, 0)
            starting = (self.offset_values[0][0] + GRID_GAP + (GRID_WIDTH + GRID_GAP) // 2,
                    self.offset_values[0][1] + GRID_GAP - WALL_WIDTH // 2)
        elif wall == 'S':
            wall_size = (GRID_WIDTH + GRID_GAP, 0)
            starting = (self.offset_values[2][0] + GRID_GAP + (GRID_WIDTH + GRID_GAP) // 2,
                    self.offset_values[2][1] + GRID_GAP - WALL_WIDTH)
        elif wall == 'W':
            wall_size = (0, GRID_HEIGHT + GRID_GAP)
            starting = (self.offset_values[0][0] + GRID_GAP - WALL_WIDTH // 2,
                    self.offset_values[0][1] + GRID_GAP + (GRID_HEIGHT + GRID_GAP) // 2)
        elif wall == 'E':
            wall_size = (0, GRID_HEIGHT + GRID_GAP)
            starting = (self.offset_values[1][0] + GRID_GAP - WALL_WIDTH,
                    self.offset_values[1][1] + GRID_GAP + (GRID_HEIGHT + GRID_GAP) // 2)
        return (starting[0] + wall_size[0] * index, starting[1] + wall_size[1] * index)

    def get_tower_pixels(self, tower_number):
        """Gets the center of a tower given the tower number"""
        offset = [val - TOWER_SIZE  for val in self.offset_values[tower_number - 1]]
        return (offset[0] + GRID_GAP + TOWER_SIZE // 2, offset[1] + GRID_GAP + TOWER_SIZE // 2)

    def draw_grid_lines(self):
        """Draws lines for the different grid boxes on the screen"""
        rows = Board.get_rows(self.board)
        columns = Board.get_columns(self.board)

        max_x = GRID_GAP * (columns + 1) + GRID_WIDTH * columns
        max_y = GRID_GAP * (rows + 1) + GRID_HEIGHT * rows

        for tower in range(1, 5):
            #Draw box for towers
            x, y = self.get_tower_pixels(tower)
            self.can.create_line(x - TOWER_SIZE // 2, y - TOWER_SIZE // 2,
                    x + TOWER_SIZE // 2, y - TOWER_SIZE // 2)
            self.can.create_line(x - TOWER_SIZE // 2, y - TOWER_SIZE // 2,
                    x - TOWER_SIZE // 2, y + TOWER_SIZE // 2)
            self.can.create_line(x + TOWER_SIZE // 2, y - TOWER_SIZE // 2,
                    x + TOWER_SIZE // 2, y + TOWER_SIZE // 2)
            self.can.create_line(x - TOWER_SIZE // 2, y + TOWER_SIZE // 2,
                    x + TOWER_SIZE // 2, y + TOWER_SIZE // 2)

        #Horizontal walls
        self.can.create_line(TOWER_SIZE + GRID_GAP, TOWER_SIZE + GRID_GAP - WALL_WIDTH,
                TOWER_SIZE + max_x, TOWER_SIZE + GRID_GAP - WALL_WIDTH)
        self.can.create_line(TOWER_SIZE + GRID_GAP, TOWER_SIZE + WALL_WIDTH + max_y,
                TOWER_SIZE + max_x, TOWER_SIZE + WALL_WIDTH + max_y)
        #Vertical walls
        self.can.create_line(TOWER_SIZE + GRID_GAP - WALL_WIDTH, TOWER_SIZE + GRID_GAP,
                TOWER_SIZE + GRID_GAP - WALL_WIDTH, TOWER_SIZE + max_y)
        self.can.create_line(TOWER_SIZE + WALL_WIDTH + max_x, TOWER_SIZE + GRID_GAP,
                TOWER_SIZE + WALL_WIDTH + max_x, TOWER_SIZE + max_y)

        for row in range(0, rows + 1):
            y = GRID_GAP * (row + 1) + GRID_HEIGHT * row
            self.can.create_line(TOWER_SIZE + GRID_GAP - WALL_WIDTH, TOWER_SIZE + y, TOWER_SIZE + max_x + WALL_WIDTH, TOWER_SIZE + y)
        for column in range(0, columns + 1):
            x =  GRID_GAP * (column + 1) + GRID_WIDTH * column
            self.can.create_line(TOWER_SIZE + x, TOWER_SIZE + GRID_GAP - WALL_WIDTH, TOWER_SIZE + x, TOWER_SIZE + max_y + WALL_WIDTH)

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
