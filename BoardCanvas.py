"""This class is responsible for making and managing a board canvas that
will draw an interactive board and allow players to move elements onto the
board. """

import tkinter
import Board
import Location
import Market
import Tower
from Move import *
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
            WALL_IMAGES.append(img.subsample(img.width() // (GRID_SIZE + GRID_GAP + 1), img.height() // (WALL_WIDTH)))
            img = tkinter.PhotoImage(file="Assets/Wall_South.gif")
            WALL_IMAGES.append(img.subsample(img.width() // (GRID_SIZE + GRID_GAP + 1), img.height() // (WALL_WIDTH)))

            img = tkinter.PhotoImage(file="Assets/Wall_East.gif")
            WALL_IMAGES.append(img.subsample(img.width() // (WALL_WIDTH), img.height() // (GRID_SIZE + GRID_GAP + 1)))
            img = tkinter.PhotoImage(file="Assets/Wall_West.gif")
            WALL_IMAGES.append(img.subsample(img.width() // (WALL_WIDTH), img.height() // (GRID_SIZE + GRID_GAP + 1)))

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

        self.placed = [None] * rows;
        for row in range(rows):
            self.placed[row] = [None] * columns

        self.placed_walls = [
            [None] * columns,   #North wall
            [None] * columns,   #South wall
            [None] * rows,      #East wall
            [None] * rows       #West wall
        ]

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
        self.place_piece(well, "WELL", self.well)
        self.add_merchant_to_grid(Market.get_active_market_street(Board.get_market(self.board))[0])

        self.stable_image = tkinter.PhotoImage(file = "Assets/Stable.gif")
        self.stable_image = self.stable_image.subsample(self.stable_image.width() // GRID_SIZE, self.stable_image.height() // GRID_SIZE)

    def place_wall(self, side, index, image_id):
        """Places a wall to the save grid, 'N' is North, 'E' is East, 'S' is
        South, 'W' is West"""
        side_index = 0
        if side == 'S':
            side_index = 1
        elif side == 'E':
            side_index = 2
        elif side == 'W':
            side_index = 3

        self.placed_walls[side_index][index] = (WALL, image_id)

    def check_placed_wall(self, side, index):
        """Checks if there is a wall placed in a given location, this will return
        either a tuple of (WALL, image_id). 'N' is North, 'E' is East, 'S' is
        South, 'W' is West"""
        side_index = 0
        if side == 'S':
            side_index = 1
        elif side == 'E':
            side_index = 2
        elif side == 'W':
            side_index = 3

        return self.placed_walls[side_index][index]

    def place_piece(self, location, piece, image_id):
        """Places a piece in the saved grid"""
        self.placed[Location.get_row(location)][Location.get_column(location)] = (piece, image_id)

    def check_placed_piece(self, location):
        """Returns what is placed in a specific location. None means the location
        is empty. The pieces are the same as the names define in Move. This
        will return a tuple of the (name of the piece, image_id)"""
        return self.placed[Location.get_row(location)][Location.get_column(location)]

    def add_merchant_to_grid(self, location):
        """Adds a merchant to a specified location on the grid"""
        image_id = self.can.create_image(self.get_board_pixels(location), image= self.merchant_image);
        self.place_piece(location, MERCHANT, image_id);
        return image_id

    def add_wall_to_grid(self, side, index):
        """Adds a static wall to the grid. Wall is the wall, wall 'N' is
        the north wall, wall 'W' is the west wall, wall 'E' is east wall, wall
        'S' is the south wall. index is the index of the wall, 0 is either top
        or leftmost wall."""
        image_id = -1;
        if side == 'N':
            image_id = self.can.create_image(self.get_wall_pixels(side, index), image=WALL_IMAGES[0])
        elif side == 'S':
            image_id = self.can.create_image(self.get_wall_pixels(side, index), image=WALL_IMAGES[1])
        elif side == 'E':
            image_id = self.can.create_image(self.get_wall_pixels(side, index), image=WALL_IMAGES[2])
        elif side == 'W':
            image_id = self.can.create_image(self.get_wall_pixels(side, index), image=WALL_IMAGES[3])
        else:
            return;
        self.place_wall(side, index, image_id)
        return image_id;

    def get_board_pixels(self, location):
        """Gets the center of an grid square for a specific Location for the
        board returned as (x, y)"""
        col = Location.get_column(location)
        row = Location.get_row(location)
        return self.offx + col * (GRID_SIZE + 2) + (col + 1) * GRID_GAP, \
                self.offy + row * (GRID_SIZE  + 2) + (row + 1) * GRID_GAP

    def add_building_to_grid(self, color, location):
        """Adds a bulding graphic to the board at a specified location"""
        image_id = self.can.create_image(self.get_board_pixels(location), image=BUILDING_IMAGES[color]);
        self.place_piece(location, BUILDING, image_id)
        return image_id

    def add_stable_to_grid(self, location):
        """Adds a stable graphic to the board at the specific location"""
        image_id = self.can.create_image(self.get_board_pixels(location), image=self.stable_image)
        self.place_piece(location, STABLE, image_id)
        return image_id



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

    def remove_piece(self, location):
        """Removes a piece from the graphical board"""
        item = self.check_placed_piece(location);
        if item != None:
            self.can.delete(item[1])
            self.placed[Location.get_row(location)][Location.get_column(location)] = None

    def remove_wall(self, side, index):
        """Removes a wall from the graphical board"""
        item = self.check_placed_wall(side, index)
        if item != None:
            side_index = 0
            if side == 'S':
                side_index = 1
            elif side == 'E':
                side_index = 2
            elif side == 'W':
                side_index = 3
            self.can.delete(item[1])
            return self.placed_walls[side_index][index] == None

    def update_board(self):
        """Updates the displayed board based on self.board"""
        for row in range(self.rows):
            for col in range(self.columns):
                loc = Location.make_location(row, col);
                board_piece = Board.get_piece(self.board, loc)
                current = self.check_placed_piece(loc)
                if board_piece == None and current == None:
                    pass
                elif board_piece == None and current != None:
                    self.remove_piece(loc)
                elif board_piece != None:
                    if current != None and current[0] != board_piece:
                        self.remove_piece(loc)

                    if board_piece == STABLE:
                        self.add_stable_to_grid(loc)
                    elif board_piece == MERCHANT:
                        self.add_merchant_to_grid(loc)
                    elif board_piece == BUILDING:
                        color = ""
                        for building in get_buildings(board):
                            if Building.building_contains_location(loc):
                                color = Building.get_building_color(building)
                        self.add_building_to_grid(color, loc)

        walls = Tower.get_wall_locations(Board.get_towers(self.board))
        for side in [-1, self.rows]:
            for index in range(self.columns):
                side_text = ['N', 'S']
                if side == -1:
                    side_text = 'N'
                else:
                    side_text = 'S'
                loc = Location.make_location(side, index)
                wall_piece = loc in walls
                current = self.check_placed_wall(side_text, index)
                if wall_piece and current == None:
                    self.place_wall(side_text, index)
                elif not wall_piece and current != None:
                    self.remove_wall(side_text, index)

        for side in [-1, self.columns]:
            for index in range(self.rows):
                side_text = ['E', 'W']
                if side == -1:
                    side_text = 'E'
                else:
                    side_text = 'W'
                loc = Location.make_location(side, index)
                wall_piece = loc in walls
                current = self.check_placed_wall(side_text, index)
                if wall_piece and current == None:
                    self.place_wall(side_text, index)
                elif not wall_piece and current != None:
                    self.remove_wall(side_text, index)

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
    """(board_canvas.add_building_to_grid(BUILDINGS_COLORS[0], Location.make_location(0,0)))
    (board_canvas.add_building_to_grid(BUILDINGS_COLORS[0], Location.make_location(0,1)))
    (board_canvas.add_building_to_grid(BUILDINGS_COLORS[0], Location.make_location(1,0)))
    (board_canvas.add_building_to_grid(BUILDINGS_COLORS[3], Location.make_location(10,15)))
    (board_canvas.add_wall_to_grid('S', 0))
    (board_canvas.add_wall_to_grid('S', 1))
    (board_canvas.add_wall_to_grid('S', 2))
    (board_canvas.add_wall_to_grid('S', 3))
    (board_canvas.add_wall_to_grid('W', 9))
    (board_canvas.add_wall_to_grid('W', 10))
    (board_canvas.add_wall_to_grid('N', 15))
    (board_canvas.add_wall_to_grid('E', 10))
    board_canvas.add_stable_to_grid(Location.make_location(1, 1))"""

    print(Board.get_market(board_canvas.board))

    board_canvas.update_board()

    #board_canvas.add_moveable_building("Violet", (100, 100))

    for row in range(11):
        thingy = ""
        for col in range(16):
            thingy += str(board_canvas.check_placed_piece(Location.make_location(row, col))) + " "

        print(thingy)

    print()

    for side in ['N', 'S']:
        a = ""
        for index in range(16):
            a += str(board_canvas.check_placed_wall(side, index)) + " "
        print(a)

    for side in ['E', 'W']:
        a = ""
        for index in range(11):
            a += str(board_canvas.check_placed_wall(side, index)) + " "
        print(a)
    board_canvas.mainloop()
