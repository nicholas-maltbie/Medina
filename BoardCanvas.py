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
        self.can = tkinter.Canvas(width=(GRID_SIZE * (Board.get_columns(board) + 2) + GRID_GAP * (Board.get_columns(board) + 4)),
            height=(GRID_SIZE * (Board.get_rows(board) + 2) + GRID_GAP * (Board.get_rows(board) + 3)))

        self.drag_data = drag_data = {"x": 0, "y": 0, "item": None, "piece": None, "data": None}
        self.listeners = []
        self.moveable_items = {}
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
            WALL_IMAGES.append(img.subsample(img.width() // (GRID_SIZE + GRID_GAP + 1), img.height() // (GRID_SIZE)))
            img = tkinter.PhotoImage(file="Assets/Wall_South.gif")
            WALL_IMAGES.append(img.subsample(img.width() // (GRID_SIZE + GRID_GAP + 1), img.height() // (GRID_SIZE)))

            img = tkinter.PhotoImage(file="Assets/Wall_East.gif")
            WALL_IMAGES.append(img.subsample(img.width() // (GRID_SIZE), img.height() // (GRID_SIZE + GRID_GAP + 1)))
            img = tkinter.PhotoImage(file="Assets/Wall_West.gif")
            WALL_IMAGES.append(img.subsample(img.width() // (GRID_SIZE), img.height() // (GRID_SIZE + GRID_GAP + 1)))

        rows = Board.get_rows(self.board)
        columns = Board.get_columns(self.board)

        max_x = GRID_GAP * (columns) + GRID_SIZE * (columns + 1)
        max_y = GRID_GAP * (rows) + GRID_SIZE * (rows + 1)

        self.offx, self.offy = GRID_SIZE + GRID_GAP * 2, GRID_SIZE + GRID_GAP * 2

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

        self.update_board()

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
        for street in Board.get_market(self.board):
            for loc in street:
                current = self.check_placed_piece(loc)
                if current != None and current[0] != MERCHANT:
                    self.remove_piece(loc)
                    current = None
                if current == None:
                    self.add_merchant_to_grid(loc)

        for building in Board.get_buildings(self.board):
            color = Building.get_building_color(building)
            for loc in Building.get_building_locations(building):
                current = self.check_placed_piece(loc)
                if current != None and current [0] != BUILDING:
                    self.remove_piece(loc)
                    current = None
                if current == None:
                    self.add_building_to_grid(color, loc)
            for loc in Building.get_stable_locations(building):
                current = self.check_placed_piece(loc)
                if current != None and current[0] != STABLE:
                    self.remove_piece(loc)
                    current = None
                if current == None:
                    self.add_stable_to_grid(loc)

        towers = Board.get_towers(self.board)
        for num in range(4):
            #print(num, Tower.get_wall_locations_for_tower(towers, num))
            for loc in Tower.get_wall_locations_for_tower(towers, num):
                side_text = ""
                index = 0
                if Location.get_row(loc) == -1:
                    side_text = "N"
                    index = Location.get_column(loc)
                elif Location.get_row(loc) == self.rows:
                    side_text = "S"
                    index = Location.get_column(loc)
                elif Location.get_column(loc) == -1:
                    side_text = "W"
                    index = Location.get_row(loc)
                elif Location.get_column(loc) == self.columns:
                    side_text = "E"
                    index = Location.get_row(loc)
                current = self.check_placed_wall(side_text, index)
                if current == None:
                    self.add_wall_to_grid(side_text, index)

    def draw_grid_lines(self):
        """Draws lines for the different grid boxes on the screen"""
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
            x1,y1 = 0,0
            x2,y2 = 0,0
            if row == 0 or row == self.rows:
                x1, y1 = self.get_board_pixels(Location.make_location(row, -1))
                x1 += GRID_GAP
                x2, y2 = self.get_board_pixels(Location.make_location(row, self.columns + 1))
                x2 -= GRID_GAP
                x0, y0 = self.get_board_pixels(Location.make_location(row - 1, 0))
                x3, y3 = self.get_board_pixels(Location.make_location(row - 1, self.columns))
                y0 += GRID_GAP
                if row == self.rows:
                    x0, y0 = self.get_board_pixels(Location.make_location(row +  1, 0))
                    x3, y3 = self.get_board_pixels(Location.make_location(row + 1, self.columns))
                    y0 -= GRID_GAP
                self.can.create_line(x1 - (GRID_SIZE + GRID_GAP) // 2,
                    y0 - (GRID_SIZE + GRID_GAP) // 2, \
                    x0 - (GRID_SIZE + GRID_GAP) // 2, \
                    y0 - (GRID_SIZE + GRID_GAP) // 2)
                self.can.create_line(x3 - (GRID_SIZE + GRID_GAP) // 2,
                    y0 - (GRID_SIZE + GRID_GAP) // 2, \
                    x2 - (GRID_SIZE + GRID_GAP) // 2, \
                    y0 - (GRID_SIZE + GRID_GAP) // 2)
            else:
                x1, y1 = self.get_board_pixels(Location.make_location(row, 0))
                x1 -= WALL_WIDTH
                x2, y2 = self.get_board_pixels(Location.make_location(row, self.columns))
                x2 += WALL_WIDTH
            self.can.create_line(x1 - (GRID_SIZE + GRID_GAP) // 2 , \
                    y1 - (GRID_SIZE + GRID_GAP) // 2, \
                    x2 - (GRID_SIZE + GRID_GAP) // 2, \
                    y2 - (GRID_SIZE + GRID_GAP) // 2)

        for column in range(0, self.columns + 1):
            x1, y1 = 0,0
            x2, y2 = 0,0
            if column == 0 or column == self.columns:
                x1,y1 = self.get_board_pixels(Location.make_location(-1, column))
                y1 += GRID_GAP
                x2,y2 = self.get_board_pixels(Location.make_location(self.rows + 1, column))
                y2 -= GRID_GAP
                x0, y0 = self.get_board_pixels(Location.make_location(0, - 1))
                x3, y3 = self.get_board_pixels(Location.make_location(self.rows, - 1))
                x0 += GRID_GAP
                if column == self.columns:
                    x0, y0 = self.get_board_pixels(Location.make_location(0, self.columns + 1))
                    x3, y3 = self.get_board_pixels(Location.make_location(self.rows, column + 1))
                    x0 -= GRID_GAP
                self.can.create_line(x0 - (GRID_SIZE + GRID_GAP) // 2,
                    y0 - (GRID_SIZE + GRID_GAP) // 2, \
                    x0 - (GRID_SIZE + GRID_GAP) // 2, \
                    y1 - (GRID_SIZE + GRID_GAP) // 2)
                self.can.create_line(x0 - (GRID_SIZE + GRID_GAP) // 2,
                    y2 - (GRID_SIZE + GRID_GAP) // 2, \
                    x0 - (GRID_SIZE + GRID_GAP) // 2, \
                    y3 - (GRID_SIZE + GRID_GAP) // 2)
            else:
                x1,y1 = self.get_board_pixels(Location.make_location(0, column))
                y1 -= WALL_WIDTH
                x2,y2 = self.get_board_pixels(Location.make_location(self.rows, column))
                y2 += WALL_WIDTH
            self.can.create_line(x1 - (GRID_SIZE + GRID_GAP) // 2,y1 - (GRID_SIZE + GRID_GAP) // 2, \
                    x2 - (GRID_SIZE + GRID_GAP) // 2,y2 - (GRID_SIZE + GRID_GAP) // 2)

    def add_moveable_building(self, color, coords):
        """Adds a moveable building of a specified color at an x and y"""
        image_id = self.can.create_image(coords, image=BUILDING_IMAGES[color], tags="token")
        self.moveable_items[image_id] = (BUILDING, color)

    def remove_moveable_item(self, moveable_id):
        """Removes a moveable item with a given id"""
        del self.moveable_items[moveable_id]
        self.can.delete(moveable_id)

    def add_board_action_listener(self, listener):
        """Adds a boar action listener, this listener must have these methods,
        on_click(self, event, image_id, piece, data=None)
        on_drop(self, event, image_id, piece, data=None)
        on_move(self, event, image_id, piece, data=None)
        piece is a the string of the piece type as defined in the Move module.
        data is the data for the piece, it will be the color of the builidng,
        the direction of a wall.
        """
        self.listeners.append(listener)

    def remove_board_action_listener(self, listener):
        """Removes a listener from the board action listeners."""
        self.listeners.remove(listener)

    def OnTokenButtonPress(self, event):
        '''Being drag of an object'''
        # record the item and its location
        can = self.can
        image_id = can.find_closest(event.x, event.y)[0]
        self.drag_data["item"] = image_id
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        if image_id in self.moveable_items:
            piece, data = self.moveable_items[image_id]
            for listener in list(self.listeners):
                listener.on_click(event, image_id, piece, data)

    def OnTokenButtonRelease(self, event):
        '''End drag of an object'''
        # reset the drag information
        can = self.can
        image_id = self.drag_data["item"]
        self.drag_data["item"] = None
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0
        if image_id in self.moveable_items:
            piece, data = self.moveable_items[image_id]
            for listener in list(self.listeners):
                listener.on_drop(event, image_id, piece, data)

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
        image_id = self.drag_data["item"]
        if image_id in self.moveable_items:
            piece, data = self.moveable_items[image_id]
            for listener in list(self.listeners):
                listener.on_move(event, image_id, piece, data)

if __name__ == "__main__":
    import random
    import Building

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

    board = board_canvas.board;
    market = Board.get_market(board)
    street = Market.get_active_market_street(market)
    for i in range(5):
        poss = list(Board.get_merchant_place_locations(board))
        if poss:
            sel = random.choice(poss)
            Market.add_merchant(street, sel)
    import GameConstants
    for color in GameConstants.BUILDINGS_COLORS:
        poss = list(Board.get_building_piece_locations(board, color))
        sel = random.choice(poss)

        Board.start_new_building(board_canvas.board, sel, color)
        building = Board.get_active_building(board, color)
        for i in range(10):
            poss = list(Board.get_building_piece_locations(board, color))
            if poss:
                sel = random.choice(poss)
                Building.attach_building_locations(building, sel)
        for i in range(3):
            poss = list(Board.get_building_piece_locations(board, color))
            if poss:
                sel = random.choice(poss)
                Building.attach_stable_location(building, sel)
        for i in range(5):
            poss = list(Board.get_building_piece_locations(board, color))
            if poss:
                sel = random.choice(poss)
                Building.attach_building_locations(building, sel)

    street = Market.get_active_market_street(market)
    for i in range(25):
        poss = list(Board.get_merchant_place_locations(board))
        if poss:
            sel = random.choice(poss)
            Market.add_merchant(street, sel)

    towers = Board.get_towers(board_canvas.board)

    tower1 = Tower.get_tower(towers, 1)
    Tower.add_tower_c(tower1)
    Tower.add_tower_c(tower1)
    Tower.add_tower_r(tower1)

    tower2 = Tower.get_tower(towers, 2)
    Tower.add_tower_c(tower2)
    Tower.add_tower_r(tower2)
    Tower.add_tower_r(tower2)

    tower3 = Tower.get_tower(towers, 3)
    Tower.add_tower_c(tower3)
    Tower.add_tower_r(tower3)
    Tower.add_tower_r(tower3)

    tower4 = Tower.get_tower(towers, 4)
    Tower.add_tower_c(tower4)
    Tower.add_tower_c(tower4)
    Tower.add_tower_r(tower4)

    board_canvas.update_board()

    #board_canvas.add_moveable_building("Violet", (100, 100))
    """
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
        print(a)"""
    board_canvas.mainloop()
