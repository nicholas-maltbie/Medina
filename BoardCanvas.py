"""This class is responsible for making and managing a board canvas that
will draw an interactive board and allow players to move elements onto the
board. """

import tkinter
import Board
import Building
import Location
import Market
import Tile
import Tower
from Move import *
from GameConstants import *

"""Size for the wall locations"""
WALL_WIDTH = 20
"""Size of each grid square in pixels"""
GRID_SIZE = 34
"""Size of the gap between grid locations"""
GRID_GAP = 8
"""Size of walls in terms of grid_sizes"""
wallSize = 1

def make_edge(loc1, loc2):
    """Makes and edge data type"""
    return (loc1, loc2)

def get_first_point(edge):
    """Gets the first point of an edge"""
    return edge[0]

def get_second_point(edge):
    """Gets the second point of an edge"""
    return edge[1]

class BoardCanvas(tkinter.Tk):
    #Load different images
    BUILDING_IMAGES = {}
    TOWER_IMAGES = {}
    PALACE_IMAGES = {}
    ROOFTOP_IMAGES = {}
    WALL_IMAGES = []
    STABLE_IMAGE = None
    TOWER_IMAGE = None
    TEA_IMAGE = None
    WELL_IMAGE = None
    MERCHANT_IMAGE = None

    def get_board_width(self):
        """Gets the width of the board from tower to tower"""
        return self.board_width

    def get_board_height(self):
        """Gets the height of the board from tower to tower"""
        return self.board_height

    def __init__(self, board, tile_supply, additional_x=0, additional_y=0):
        tkinter.Tk.__init__(self)

        self.BUILDING_IMAGES = {}
        self.PALACE_IMAGES = {}
        self.TOWER_IMAGES = {}
        self.ROOFTOP_IMAGES = {}
        self.WALL_IMAGES = []
        self.STABLE_IMAGE = None
        self.TOWER_IMAGE = None
        self.TEA_IMAGE = None
        self.WELL_IMAGE = None
        self.MERCHANT_IMAGE = None

        self.board_width = GRID_SIZE * (Board.get_columns(board) + 2*wallSize + 6) + GRID_GAP * (Board.get_columns(board) + 2*wallSize + 5)
        self.board_height = GRID_SIZE * (Board.get_rows(board) + 2*wallSize + 6) + GRID_GAP * (Board.get_rows(board) + 2*wallSize + 4)
        self.can = tkinter.Canvas(width=self.board_width + additional_x, height=self.board_height + additional_y)

        self.drag_data = drag_data = {"x": 0, "y": 0, "item": None, "piece": None, "data": None}
        self.listeners = []
        self.moveable_items = {}
        self.board = board
        self.tile_supply = tile_supply
        self.can.pack()
        self.drawn_edges = {}
        self.drawn_rooftops = {}
        self.drawn_tower_tiles = {}
        self.drawn_tower_merchants = {}
        self.drawn_palace_tiles = {}
        self.drawn_tea_tiles = {}

        if self.TOWER_IMAGE == None:
            self.TOWER_IMAGE = tkinter.PhotoImage(file="Assets/Tower.gif")
            self.TOWER_IMAGE = self.TOWER_IMAGE.subsample(self.TOWER_IMAGE.width() // GRID_SIZE, self.TOWER_IMAGE.height() // GRID_SIZE)
        if self.WELL_IMAGE == None:
            self.WELL_IMAGE = tkinter.PhotoImage(file = "Assets/Well.gif")
            self.WELL_IMAGE = self.WELL_IMAGE.subsample(self.WELL_IMAGE.width() // GRID_SIZE, self.WELL_IMAGE.height() // GRID_SIZE)

        if self.BUILDING_IMAGES == {}:
            for color in BUILDINGS_COLORS:
                img = tkinter.PhotoImage(file="Assets/Building_" + color[0] + ".gif")
                self.BUILDING_IMAGES[color] = img.subsample(img.width() // GRID_SIZE, img.height() // GRID_SIZE)
            img = tkinter.PhotoImage(file="Assets/Wall_North.gif")
            self.WALL_IMAGES.append(img.subsample(img.width() // (GRID_SIZE + GRID_GAP + 1), img.height() // (WALL_WIDTH)))
            img = tkinter.PhotoImage(file="Assets/Wall_South.gif")
            self.WALL_IMAGES.append(img.subsample(img.width() // (GRID_SIZE + GRID_GAP + 1), img.height() // (WALL_WIDTH)))

            img = tkinter.PhotoImage(file="Assets/Wall_East.gif")
            self.WALL_IMAGES.append(img.subsample(img.width() // (WALL_WIDTH), img.height() // (GRID_SIZE + GRID_GAP + 1)))
            img = tkinter.PhotoImage(file="Assets/Wall_West.gif")
            self.WALL_IMAGES.append(img.subsample(img.width() // (WALL_WIDTH), img.height() // (GRID_SIZE + GRID_GAP + 1)))

        rows = Board.get_rows(self.board)
        columns = Board.get_columns(self.board)

        max_x = GRID_GAP * (columns) + GRID_SIZE * (columns + 1)
        max_y = GRID_GAP * (rows) + GRID_SIZE * (rows + 1)

        self.offx, self.offy = GRID_SIZE * 4 + GRID_GAP * 3, GRID_SIZE * 4 + GRID_GAP * 3

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
        self.tower_locs = [(Location.make_location(-4, -4), Location.make_location(-1, -1)),
                (Location.make_location(-4, self.columns), Location.make_location(-1, self.columns + 3)),
                (Location.make_location(self.rows, -4), Location.make_location(self.rows + 3, -1)),
                (Location.make_location(self.rows, self.columns), Location.make_location(self.rows + 3, self.columns + 3))]

        board = self.board
        if self.MERCHANT_IMAGE == None:
            self.MERCHANT_IMAGE = tkinter.PhotoImage(file = "Assets/Merchant.gif")
            self.MERCHANT_IMAGE = self.MERCHANT_IMAGE.subsample(self.MERCHANT_IMAGE.width() // GRID_SIZE, self.MERCHANT_IMAGE.height() // GRID_SIZE)

        board = self.board
        self.elements = [[None] * Board.get_columns(board)] * Board.get_rows(board);

        self.towers = []
        for i in range(1, 5):
            self.can.create_image(self.get_tower_pixels(i), image = self.TOWER_IMAGE)
        well = Board.get_well(self.board)
        self.well = self.can.create_image(self.get_board_pixels(well), image = self.WELL_IMAGE)
        self.place_piece(well, "WELL", self.well)
        self.add_merchant_to_grid(Market.get_active_market_street(Board.get_market(self.board))[0])

        if self.STABLE_IMAGE == None:
            self.STABLE_IMAGE = tkinter.PhotoImage(file = "Assets/Stable.gif")
            self.STABLE_IMAGE = self.STABLE_IMAGE.subsample(self.STABLE_IMAGE.width() // GRID_SIZE, self.STABLE_IMAGE.height() // GRID_SIZE)

        if self.ROOFTOP_IMAGES == {}:
            for color in PLAYER_COLORS:
                self.ROOFTOP_IMAGES[color[0]] = tkinter.PhotoImage(file = "Assets/Rooftop_" + color[0] + ".gif")
                self.ROOFTOP_IMAGES[color[0]] = self.ROOFTOP_IMAGES[color[0]].subsample( \
                        self.ROOFTOP_IMAGES[color[0]].width() // GRID_SIZE, self.ROOFTOP_IMAGES[color[0]].height() // GRID_SIZE)

        if self.PALACE_IMAGES == {}:
            for color in BUILDINGS_COLORS:
                self.PALACE_IMAGES[color[0]] = tkinter.PhotoImage(file = "Assets/Palace_Tile_" + color[0]  + ".gif")
                self.PALACE_IMAGES[color[0]] = self.PALACE_IMAGES[color[0]].subsample( \
                        self.PALACE_IMAGES[color[0]].width() // (GRID_SIZE * 2), self.PALACE_IMAGES[color[0]].height() // (GRID_SIZE * 2))

        if self.TOWER_IMAGES == {}:
            for num in range(1, 5):
                self.TOWER_IMAGES[num] = tkinter.PhotoImage(file = "Assets/Tower_Tile_" + str(num)  + ".gif")
                self.TOWER_IMAGES[num] = self.TOWER_IMAGES[num].subsample( \
                        self.TOWER_IMAGES[num].width() // (GRID_SIZE * 2), self.TOWER_IMAGES[num].height() // (GRID_SIZE * 2))

        if self.TEA_IMAGE == None:
            self.TEA_IMAGE = tkinter.PhotoImage(file = "Assets/Tea_Tile.gif")
            self.TEA_IMAGE = self.TEA_IMAGE.subsample(self.TEA_IMAGE.width() // (GRID_SIZE * 2), self.TEA_IMAGE.height() // (GRID_SIZE * 2))

        self.update_board()

    def draw_rooftop(self, loc, color):
        """Draws a roofotp and returns the image ID"""
        return self.can.create_image(self.get_board_pixels(loc), image=self.ROOFTOP_IMAGES[color])

    def draw_edge(self, edge, color):
        """Draws an edge and returns the image ID"""
        loc1 = get_first_point(edge)
        loc2 = get_second_point(edge)
        r1, c1 = loc1
        r2, c2 = loc2
        x1, y1 = self.get_board_pixels(loc1)
        x2, y2 = self.get_board_pixels(loc2)
        image_id = -1
        if r1 == r2:
            yabove = (y1 + self.get_board_pixels(Location.make_location(r1 - 1, c1))[1]) / 2
            ybelow = (y1 + self.get_board_pixels(Location.make_location(r1 + 1, c1))[1]) / 2
            image_id = self.can.create_line((x1 + x2) // 2, \
                    yabove, \
                    (x1 + x2) // 2, \
                    ybelow, \
                    width=GRID_GAP//4)
        else:
            xleft = (x1 + self.get_board_pixels(Location.make_location(r1, c1 - 1))[0]) / 2
            xright = (x1 + self.get_board_pixels(Location.make_location(r1, c1 + 1))[0]) / 2
            image_id = self.can.create_line(xleft, \
                    (y1 + y2) // 2, \
                    xright, \
                    (y1 + y2) // 2,
                    width=GRID_GAP//4)
        self.can.itemconfig(image_id, fill=color)
        return image_id

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
        image_id = self.can.create_image(self.get_board_pixels(location), image= self.MERCHANT_IMAGE);
        self.place_piece(location, MERCHANT, image_id);
        return image_id

    def add_wall_to_grid(self, side, index):
        """Adds a static wall to the grid. Wall is the wall, wall 'N' is
        the north wall, wall 'W' is the west wall, wall 'E' is east wall, wall
        'S' is the south wall. index is the index of the wall, 0 is either top
        or leftmost wall."""
        image_id = -1;
        if side == 'N':
            image_id = self.can.create_image(self.get_wall_pixels(side, index), image=self.WALL_IMAGES[0])
        elif side == 'S':
            image_id = self.can.create_image(self.get_wall_pixels(side, index), image=self.WALL_IMAGES[1])
        elif side == 'E':
            image_id = self.can.create_image(self.get_wall_pixels(side, index), image=self.WALL_IMAGES[2])
        elif side == 'W':
            image_id = self.can.create_image(self.get_wall_pixels(side, index), image=self.WALL_IMAGES[3])
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
        image_id = self.can.create_image(self.get_board_pixels(location), image=self.BUILDING_IMAGES[color]);
        self.place_piece(location, BUILDING, image_id)
        return image_id

    def add_stable_to_grid(self, location):
        """Adds a stable graphic to the board at the specific location"""
        image_id = self.can.create_image(self.get_board_pixels(location), image=self.STABLE_IMAGE)
        self.place_piece(location, STABLE, image_id)
        return image_id

    def get_wall_pixels(self, wall, index):
        """Gets the center of a wall location. Wall is the wall, wall 'N' is
        the north wall, wall 'W' is the west wall, wall 'E' is east wall, wall
        'S' is the south wall. index is the index of the wall, 0 is either top
        or leftmost wall."""
        if wall == 'N':
            x, y = self.get_board_pixels(Location.make_location(-1, index));
            return x, y + (GRID_GAP+GRID_SIZE)/2 - WALL_WIDTH/2
        if wall == 'E':
            x, y = self.get_board_pixels(Location.make_location(index, self.columns));
            return x - (GRID_GAP+GRID_SIZE)/2 + WALL_WIDTH/2, y
        if wall == 'S':
            x, y = self.get_board_pixels(Location.make_location(self.rows, index));
            return x, y-(GRID_GAP+GRID_SIZE)/2 + WALL_WIDTH/2
        if wall == 'W':
            x, y = self.get_board_pixels(Location.make_location(index, -1));
            return x + (GRID_GAP+GRID_SIZE)/2 - WALL_WIDTH/2, y

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
            self.placed_walls[side_index][index] = None

    def clear_board(self):
        """Removes all currently drawn elements form the board"""
        for row in range(self.rows):
            for col in range(self.columns):
                self.remove_piece(Location.make_location(row, col))
        for col in range(self.columns):
            self.remove_wall('N', col)
            self.remove_wall('S', col)
        for row in range(self.rows):
            self.remove_wall('E', row)
            self.remove_wall('W', row)
        for key in list(self.drawn_edges.keys()):
            self.can.delete(self.drawn_edges[key])
            del self.drawn_edges[key]
        for key in list(self.drawn_rooftops.keys()):
            self.can.delete(self.drawn_rooftops[key])
            del self.drawn_rooftops[key]

    def check_well(self):
        """Checks if the well is placed in the correct spot"""
        well = Board.get_well(self.board)
        self.well = self.can.create_image(self.get_board_pixels(well), image = self.WELL_IMAGE)
        self.place_piece(well, "WELL", self.well)

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
        edges = []
        edge_colors = {}
        rooftops = []
        rooftop_colors = {}
        tower_tiles = {}
        palace_tiles = {}
        tea_tiles = {}
        tower_merchants = []

        temp_tiles = [tile for tile in self.tile_supply if Tile.get_tile_type(tile) == Tile.TOWER_TILE]
        for t in temp_tiles:
            tower_tiles[Tile.get_tile_value(t)] = t
            tower_merchants.extend([(Tile.get_tile_value(t), m) for m in range(Tile.get_num_merchants(t))])
        #print(tower_merchants)
        for key in list(self.drawn_tower_tiles.keys()):
            if key not in tower_tiles:
                self.can.delete(self.drawn_tower_tiles[key])
                del self.drawn_tower_tiles[key]
        for t in temp_tiles:
            if Tile.get_tile_value(t) not in self.drawn_tower_tiles:
                self.drawn_tower_tiles[Tile.get_tile_value(t)] = self.draw_tower_tile(Tile.get_tile_value(t))
        for key in list(self.drawn_tower_merchants.keys()):
            if key not in tower_merchants:
                self.can.delete(self.drawn_tower_merchants[key])
                del self.drawn_tower_merchants[key]
        for merchant in tower_merchants:
            if merchant not in self.drawn_tower_merchants:
                self.drawn_tower_merchants[merchant] = self.draw_tower_tile_merchant(merchant[0], merchant[1])

        temp_tiles = [tile for tile in self.tile_supply if Tile.get_tile_type(tile) == Tile.PALACE_TILE]
        for t in temp_tiles:
            palace_tiles[Tile.get_tile_value(t)] = t
        for key in list(self.drawn_palace_tiles.keys()):
            if key not in palace_tiles:
                self.can.delete(self.drawn_palace_tiles[key])
                del self.drawn_palace_tiles[key]
        for t in temp_tiles:
            if Tile.get_tile_value(t) not in self.drawn_palace_tiles:
                self.drawn_palace_tiles[Tile.get_tile_value(t)] = self.draw_palace_tile(Tile.get_tile_value(t))

        temp_tiles = [tile for tile in self.tile_supply if Tile.get_tile_type(tile) == Tile.TEA_TILE]
        for i in range(len(temp_tiles)):
            tea_tiles[i] = temp_tiles[i]
        for key in list(self.drawn_tea_tiles.keys()):
            if key not in tea_tiles:
                self.can.delete(self.drawn_tea_tiles[key])
                del self.drawn_tea_tiles[key]
        for i in range(len(temp_tiles)):
            if i not in self.drawn_tea_tiles:
                self.drawn_tea_tiles[i] = self.draw_tea_tile(i)

        for building in Board.get_buildings(self.board):
            color = Building.get_building_color(building)
            all_locs = Building.get_building_and_stables(building)
            stables = Building.get_stable_locations(building)
            for loc in Building.get_building_locations(building):
                current = self.check_placed_piece(loc)
                if loc not in stables and current != None and current [0] != BUILDING:
                    self.remove_piece(loc)
                    current = None
                if current == None:
                    self.add_building_to_grid(color, loc)
                if Building.has_owner(building):
                    for adj in Location.get_orthogonal(loc):
                        edge = make_edge(loc, adj)
                        if adj not in all_locs:
                            edges.append(edge)
                            edge_colors[edge] = Building.get_owner_color(building)

            for loc in Building.get_stable_locations(building):
                current = self.check_placed_piece(loc)
                if current != None and current[0] != STABLE:
                    self.remove_piece(loc)
                    current = None
                if current == None:
                    self.add_stable_to_grid(loc)
                if Building.has_owner(building):
                    for adj in Location.get_orthogonal(loc):
                        edge = make_edge(loc, adj)
                        if adj not in all_locs:
                            edges.append(edge)
                            edge_colors[edge] = Building.get_owner_color(building)

            if Building.has_owner(building):
                rooftops.append(Building.get_rooftop_location(building))
                rooftop_colors[Building.get_rooftop_location(building)] = Building.get_owner_color(building)[0]


        for key in list(self.drawn_rooftops.keys()):
            if key not in rooftops:
                self.can.delete(self.drawn_rooftops[key])
                del self.drawn_rooftops[key]
        for rooftop in rooftops:
            if rooftop not in self.drawn_rooftops:
                self.drawn_rooftops[rooftop] = self.draw_rooftop(rooftop, rooftop_colors[rooftop])

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

        for key in list(self.drawn_edges.keys()):
            if key not in edges:
                self.can.delete(self.drawn_edges[key])
                del self.drawn_edges[key]
            else:
                self.can.tag_raise(self.drawn_edges[key])
        for edge in edges:
            if edge not in self.drawn_edges:
                self.drawn_edges[edge] = self.draw_edge(edge, PLAYER_COLORS_HEX[edge_colors[edge]])

        if self.drag_data["item"] != None:
            self.can.tag_raise(self.drag_data["item"])

    def draw_tea_tile(self, tea_num):
        """Draws a tea tile and returns the image id"""
        loc1, loc2 = (Location.make_location(-1, -4), Location.make_location(2, -1))
        x1, y1 = self.get_board_pixels(loc1)
        x2, y2 = self.get_board_pixels(loc2)
        x_center = (x1 + x2) / 2
        y_center = (y1 + y2) / 2 + GRID_GAP * (tea_num + 1) + GRID_SIZE * tea_num
        return self.can.create_image((x_center, y_center), image= self.TEA_IMAGE)

    def draw_palace_tile(self, palace_num):
        """Draws a palace tile and returns the image id"""
        half = self.get_board_width() // 2
        x1, x2 = half - (GRID_GAP * 5 + GRID_SIZE * 4), half + (GRID_GAP * 5 + GRID_SIZE * 4)
        x_temp, y1 = self.get_board_pixels(Location.make_location(-4, 0))
        x_temp, y2 = self.get_board_pixels(Location.make_location(-1, 0))
        x_center = x1 + GRID_SIZE * 2 * (palace_num - 1) + GRID_SIZE * 3 / 2 + GRID_GAP * (palace_num)
        y_center = (y1 + y2) / 2
        return self.can.create_image((x_center, y_center), image = self.PALACE_IMAGES[Tile.PALACE_COLORS[palace_num][0]])

    def draw_tower_tile(self, tower_num):
        """Draws a tower tile and returns the image id"""
        return self.can.create_image(self.get_tower_tile_center(tower_num),
                image = self.TOWER_IMAGES[tower_num])

    def draw_tower_tile_merchant(self, tower_num, merchant_num):
        """Draws merchants for a tower tile"""
        x, y = self.get_tower_tile_center(tower_num)
        if merchant_num % 2 == 0:
            x -= (GRID_SIZE + GRID_GAP) / 2
        else:
            x += (GRID_SIZE + GRID_GAP) / 2
        if merchant_num < 2:
            y -= (GRID_SIZE + GRID_GAP) / 2
        else:
            y += (GRID_SIZE + GRID_GAP) / 2
        return self.can.create_image((x, y), image = self.MERCHANT_IMAGE)

    def get_tower_tile_center(self, tower_num):
        """Gets the center of a tower tile location"""
        (x1, y1), (x2, y2) = [self.get_board_pixels(loc) for loc in self.tower_locs[tower_num - 1]]
        return (x1 + x2) // 2, (y1 + y2) // 2

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

        for loc1, loc2 in [(Location.make_location(-3, -3), Location.make_location(-1, -1)),
                    (Location.make_location(-3, self.columns + 1), Location.make_location(-1, self.columns + 3)),
                    (Location.make_location(self.rows + 1, -3), Location.make_location(self.rows + 3, -1)),
                    (Location.make_location(self.rows + 1, self.columns + 1), Location.make_location(self.rows + 3, self.columns + 3)),
                    (Location.make_location(0, -3), Location.make_location(7, -1))]:
            x1,y1 = self.get_board_pixels(loc1)
            x2,y2 = self.get_board_pixels(loc2)
            self.can.create_line(x1 - (GRID_SIZE + GRID_GAP) // 2, \
                    y1 - (GRID_SIZE + GRID_GAP) // 2, \
                    x2 - (GRID_SIZE + GRID_GAP) // 2, \
                    y1 - (GRID_SIZE + GRID_GAP) // 2)
            self.can.create_line(x1 - (GRID_SIZE + GRID_GAP) // 2, \
                    y2 - (GRID_SIZE + GRID_GAP) // 2, \
                    x2 - (GRID_SIZE + GRID_GAP) // 2, \
                    y2 - (GRID_SIZE + GRID_GAP) // 2)
            self.can.create_line(x1 - (GRID_SIZE + GRID_GAP) // 2, \
                    y1 - (GRID_SIZE + GRID_GAP) // 2, \
                    x1 - (GRID_SIZE + GRID_GAP) // 2, \
                    y2 - (GRID_SIZE + GRID_GAP) // 2)
            self.can.create_line(x2 - (GRID_SIZE + GRID_GAP) // 2, \
                    y1 - (GRID_SIZE + GRID_GAP) // 2, \
                    x2 - (GRID_SIZE + GRID_GAP) // 2, \
                    y2 - (GRID_SIZE + GRID_GAP) // 2)
        half = self.get_board_width() // 2
        x1, x2 = half - (GRID_GAP * 5 + GRID_SIZE * 4), half + (GRID_GAP * 5 + GRID_SIZE * 4)
        x_temp, y1 = self.get_board_pixels(Location.make_location(-3, 0))
        x_temp, y2 = self.get_board_pixels(Location.make_location(-1, 0))
        self.can.create_line(x1, \
                y1 - (GRID_SIZE + GRID_GAP) // 2, \
                x2, \
                y1 - (GRID_SIZE + GRID_GAP) // 2)
        self.can.create_line(x1, \
                y2 - (GRID_SIZE + GRID_GAP) // 2, \
                x2, \
                y2 - (GRID_SIZE + GRID_GAP) // 2)
        self.can.create_line(x1, \
                y1 - (GRID_SIZE + GRID_GAP) // 2, \
                x1, \
                y2 - (GRID_SIZE + GRID_GAP) // 2)
        self.can.create_line(x2, \
                y1 - (GRID_SIZE + GRID_GAP) // 2, \
                x2, \
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

    def add_moveable_image(self, image, coords, item_type, data=None):
        """Adds a moveable image to the screen"""
        image_id = self.can.create_image(coords, image = image, tags = "token")
        self.moveable_items[image_id] = (item_type, data)
        return image_id

    def add_moveable_building(self, color, coords):
        """Adds a moveable building of a specified color at an x and y"""
        image_id = self.can.create_image(coords, image=self.BUILDING_IMAGES[color], tags="token")
        self.moveable_items[image_id] = (BUILDING, color)
        return image_id

    def add_moveable_stable(self, coords):
        """Adds a moveable stable at an x and y"""
        image_id = self.can.create_image(coords, image=self.STABLE_IMAGE, tags="token")
        self.moveable_items[image_id] = (STABLE, None)
        return image_id

    def add_moveable_wall(self, coords):
        """Adds a moveable wall at an x and y"""
        image_id = self.can.create_image(coords, image=self.WALL_IMAGES[0], tags="token")
        self.moveable_items[image_id] = (WALL, 'N')
        return image_id

    def add_moveable_merchant(self, coords):
        """Adds a moveable merchant to an x and y"""
        image_id = self.can.create_image(coords, image=self.MERCHANT_IMAGE, tags="token")
        self.moveable_items[image_id] = (MERCHANT, None)
        return image_id

    def add_moveable_rooftop(self, coords, color):
        """Adds a moveable rooftop to the board"""
        image_id = self.can.create_image(coords, image=self.ROOFTOP_IMAGES[color[0]], tags="token")
        self.moveable_items[image_id] = (ROOFTOP, color)
        return image_id

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
        self.can.tag_raise(self.drag_data["item"])
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

    import GameConstants
    for color in GameConstants.BUILDINGS_COLORS:
        poss = list(Board.get_building_piece_locations(board, color))
        sel = random.choice(poss)

        Board.start_new_building(board_canvas.board, sel, color)
        building = Board.get_active_building(board, color)
        for i in range(3):
            poss = list(Board.get_building_piece_locations(board, color))
            if poss:
                sel = random.choice(poss)
                Building.attach_building_locations(building, sel)
        for i in range(1):
            poss = list(Board.get_building_piece_locations(board, color))
            if poss:
                sel = random.choice(poss)
                Building.attach_stable_location(building, sel)
        for i in range(5):
            poss = list(Board.get_building_piece_locations(board, color))
            if poss:
                sel = random.choice(poss)
                Building.attach_building_locations(building, sel)

    for i in range(15):
        poss = list(Board.get_merchant_place_locations(board))
        if poss:
            sel = random.choice(poss)
            Market.add_merchant_to_market(market, sel)

    #print(Board.get_well(board_canvas.board))
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

    orange = Board.get_active_building(board, 'Orange')
    Building.assign_owner(orange, 'Nick', 'Red')

    board_canvas.update_board()

    import time, threading

    def foo():
        poss = list(Board.get_building_piece_locations(board, 'Orange'))
        if poss:
            sel = random.choice(poss)
            if Board.get_active_building(board, 'Orange') == None:
                Board.start_new_building(board, sel, 'Orange')
            else:
                Building.attach_building_locations(Board.get_active_building(board, 'Orange'), sel)
        board_canvas.update_board()
        threading.Timer(3, foo).start()

    threading.Timer(3, foo).start()

    #board_canvas.draw_edge(make_edge(Location.make_location(1,1), Location.make_location(1, 0)), "red")
    #board_canvas.draw_edge(make_edge(Location.make_location(0, 1), Location.make_location(1, 1)), "red")

    board_canvas.add_moveable_building("Violet", (100, 100))
    board_canvas.add_moveable_building("Orange", (100, 150))
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
