"""A human agent manages its own board and displays a board and adds moveable
pieces so a human agent can play pieces on the board from his or her hand"""

import Agent
import Move
import Board
import BoardCanvas
import Player
import Building
import Tile
import Location
import GameConstants
import threading

class HumanAgent:

    def __init__(self, board_canvas, board, tile_supply, player_index, players):
        """Makes a human agent based off a player who plays on the given board"""
        self.grid = BoardCanvas.GRID_SIZE
        self.gap = BoardCanvas.GRID_GAP
        self.draw_human_items(player)
        self.board = board
        self.tile_supply = tile_supply
        self.board_canvas = board_canvas
        self.player = players[player_index]
        self.players = players
        self.player_index = player_index
        board_canvas.add_board_action_listener(self)

    def on_click(self, event, image_id, piece, data=None):
        """To satify being a board action listener"""
        self.pos = (event.x, event.y)

    def on_drop(self, event, image_id, piece, data=None):
        """To satify being a board action listener"""
        x, y = event.x, event.y
        x -= self.board_canvas.offx
        y -= self.board_canvas.offy
        row = round((y - (self.grid) / 2) / (self.grid + self.gap))
        col = round((x - (self.grid + self.gap) / 2) / (self.grid + self.gap))
        loc = Location.make_location(row, col)
        if piece == Move.ROOFTOP:
            for color in GameConstants.BUILDINGS_COLORS:
                building = Board.get_active_building(self.board, color)
                if building != None and loc in Building.get_building_locations(building):
                    data = color

        move = Move.make_move(Player.get_player_name(self.player), Move.NORMAL, piece, loc, data)
        valid = Agent.is_valid_move(move, self.board, self.player)

        if valid:
            self.board_canvas.remove_moveable_item(image_id)
            self.board, self.players, self.tile_supply = Agent.apply_move(move,
                    self.board, self.tile_supply, self.player_index, self.players)
            self.board_canvas.board = self.board
            self.board_canvas.tile_supply = self.tile_supply
            self.board_canvas.player = self.players[self.player_index]
            self.player = self.players[self.player_index]
            self.board_canvas.update_board()
            #coords = self.board_canvas.get_board_pixels(loc)
            #self.board_canvas.can.move(image_id,
            #        coords[0] - self.board_canvas.can.coords(image_id)[0],
            #        coords[1] - self.board_canvas.can.coords(image_id)[1])
        else:
            self.board_canvas.can.move(image_id, self.pos[0] - event.x, self.pos[1] - event.y)

    def on_move(self, event, image_id, piece, data=None):
        """To satify being a board action listener"""
        pass

    def draw_human_items(self, player):
        grid = self.grid
        gap = self.gap
        offy = gap * 3 + grid * 5 / 2
        """Draws a player's items on the screen"""
        def draw_things(offy, draw_method, num_things, piece_type, x_jump = grid + gap):
            """Draws a number of things with a draw mehtod"""
            if num_things > 0:
                offx = board_canvas.get_board_width() + gap + grid // 2
                for i in range(num_things):
                    draw_method(offx, offy)
                    offx += x_jump
                    if (i + 1) % 6 == 0 and i != num_things - 1:
                        offx = board_canvas.get_board_width() + gap + grid // 2
                        offy += grid + gap

                offy += grid + gap
            return offy

        offy = draw_things(offy, lambda x, y: board_canvas.add_moveable_rooftop((x, y), Player.get_player_color(player)),
                Player.get_held_rooftops(player), Move.ROOFTOP)
        offy = draw_things(offy, lambda x, y: board_canvas.add_moveable_rooftop((x, y), "Neutral"),
                Player.get_extra_rooftops(player), Move.NEUTRAL_ROOFTOP)
        for color in GameConstants.BUILDINGS_COLORS:
            offy = draw_things(offy, lambda x, y: board_canvas.add_moveable_building(color, (x,y)),
                    Player.get_held_buildings_of_color(player, color), color)
        offy = draw_things(offy, lambda x, y: board_canvas.add_moveable_stable((x, y)),
                Player.get_num_stables(player), Move.STABLE)
        offy = draw_things(offy, lambda x, y: board_canvas.add_moveable_merchant((x, y)),
                Player.get_held_merchants(player), Move.MERCHANT)
        offy = draw_things(offy, lambda x, y: board_canvas.add_moveable_wall((x, y)),
                Player.get_held_walls(player), Move.WALL, x_jump = grid + gap * 2)

    def human_decision(self, board, player_index, num_moves, players):
        pass

if __name__ == "__main__":

    colors = ['Blue', 'Green', 'Yellow', 'Red']
    names = ['Nick', 'Zach', 'Brian', 'Aaron']
    players = [Player.make_player(names[i], 4, colors[i]) for i in range(4)]

    board = Board.make_board(11, 16)
    tile_supply = Tile.get_all_tiles()
    player = players[0]
    player_index = 0

    grid = BoardCanvas.GRID_SIZE
    gap = BoardCanvas.GRID_GAP

    board_canvas = None

    board_canvas = BoardCanvas.BoardCanvas(board, tile_supply, additional_x= grid * 10)
    board_canvas.setup()

    def test_game():
        human_agent = HumanAgent(board_canvas, board, tile_supply, player_index, players)


    thread = threading.Thread(target = test_game)
    thread.start()

    board_canvas.mainloop()
    #print(Player.get_player_color(nick))
    #print(nick)
