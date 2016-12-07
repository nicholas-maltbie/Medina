"""A human agent manages its own board and displays a board and adds moveable
pieces so a human agent can play pieces on the board from his or her hand"""

import Agent
import Move
import queue
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
        self.drawn_things = {}
        self.board = board
        self.tile_supply = tile_supply
        self.board_canvas = board_canvas
        self.player = players[player_index]
        self.players = players
        self.player_index = player_index
        self.actions_queue = queue.Queue()
        self.is_turn = False

        self.draw_human_items(self.player)
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

        if piece == Tile.TEA_TILE and -1 <= Location.get_row(loc) <= Board.get_rows(self.board) and \
            -1 <= Location.get_column(loc) <= Board.get_columns(self.board):
            move = Move.make_move(Player.get_player_name(self.player), Move.PASS)

        valid = Agent.is_valid_move(move, self.board, self.player)

        if self.is_turn and valid:
            self.actions_queue.put((image_id, move))
        else:
            coords = self.board_canvas.can.coords(image_id)
            self.board_canvas.can.move(image_id, self.pos[0] - event.x, self.pos[1] - event.y)

    def on_move(self, event, image_id, piece, data=None):
        """To satify being a board action listener"""
        pass

    def draw_human_items(self, player):
        grid = self.grid
        gap = self.gap
        offy = gap * 3 + grid * 3 / 2
        """Draws a player's items on the screen"""
        def draw_things(offy, draw_method, values, piece_type, x_jump = grid + gap,
                y_jump = grid + gap, push_x = 0, push_y = 0):
            """Draws a number of things with a draw mehtod"""
            drawn = set()
            offy += push_y
            if values:
                offx = board_canvas.get_board_width() + gap + grid // 2 + push_x
                for index in range(len(values)):
                    val = values[index]
                    key = (piece_type, val)
                    drawn.add(key)
                    if key in self.drawn_things:
                        if self.drawn_things[key] not in self.board_canvas.moveable_items:
                            del self.drawn_things[key]
                            self.drawn_things[key] = draw_method(offx, offy, val)
                        else:
                            coords = self.board_canvas.can.coords(self.drawn_things[key])
                            if coords != (int(offx), int(offy)):
                                self.board_canvas.can.move(self.drawn_things[key], offx - coords[0], offy - coords[1])
                    else:
                        self.drawn_things[key] = draw_method(offx, offy, val)
                    offx += x_jump
                    if (index + 1) % 6 == 0 and index != len(values) - 1:
                        offx = board_canvas.get_board_width() + gap + grid // 2 + push_y
                        offy += y_jump
                offy += y_jump
            for key in list(self.drawn_things.keys()):
                if key[0] == piece_type and key not in drawn:
                    if self.drawn_things[key] in self.board_canvas.moveable_items:
                        self.board_canvas.remove_moveable_item(self.drawn_things[key])
                    del self.drawn_things[key]
            return offy

        offy = draw_things(offy, lambda x, y, val: board_canvas.add_moveable_rooftop((x, y), Player.get_player_color(self.player)),
                range(Player.get_held_rooftops(self.player)), Move.ROOFTOP)
        offy = draw_things(offy, lambda x, y, val: board_canvas.add_moveable_rooftop((x, y), "Neutral"),
                range(Player.get_extra_rooftops(self.player)), Move.NEUTRAL_ROOFTOP)
        for color in GameConstants.BUILDINGS_COLORS:
            offy = draw_things(offy, lambda x, y, val: board_canvas.add_moveable_building(color, (x,y)),
                    range(Player.get_held_buildings_of_color(self.player, color)), color)
        offy = draw_things(offy, lambda x, y, val: board_canvas.add_moveable_stable((x, y)),
                range(Player.get_num_stables(self.player)), Move.STABLE)
        offy = draw_things(offy, lambda x, y, val: board_canvas.add_moveable_merchant((x, y)),
                range(Player.get_held_merchants(self.player)), Move.MERCHANT)
        offy = draw_things(offy, lambda x, y, val: board_canvas.add_moveable_wall((x, y)),
                range(Player.get_held_walls(self.player)), Move.WALL, x_jump = grid + gap * 2)

        offy += grid / 2 + gap

        values = [Tile.get_tile_value(tile) for tile in Player.get_tiles_of_type(self.player, Tile.PALACE_TILE)]
        values.sort()
        offy = draw_things(offy, lambda x, y, n:self.board_canvas.add_moveable_image( \
                self.board_canvas.palace_images[Tile.PALACE_COLORS[n][0]], (x, y), Tile.PALACE_TILE, n), \
                values, Tile.PALACE_TILE, x_jump = grid * 3 / 2 + gap, y_jump = grid * 2 + gap, push_x = grid / 2)

        values = [Tile.get_tile_value(tile) for tile in Player.get_tiles_of_type(self.player, Tile.TOWER_TILE)]
        values.sort()
        offy = draw_things(offy, lambda x, y, n:self.board_canvas.add_moveable_image( \
                self.board_canvas.tower_images[n], (x, y), Tile.TOWER_TILE, n), \
                values, Tile.TOWER_TILE, x_jump = grid * 3 / 2 + gap, y_jump = grid * 2 + gap, push_x = grid / 2)


        values = range(len(Player.get_tiles_of_type(self.player, Tile.TEA_TILE)))
        offy = draw_things(offy, lambda x, y, n:self.board_canvas.add_moveable_image( \
                self.board_canvas.tea_image, (x, y), Tile.TEA_TILE, n), \
                values, Tile.TEA_TILE, x_jump = grid * 3 / 2 + gap, y_jump = grid * 2 + gap, push_x = grid / 2)

    def human_decision(self, board, player_index, players, tile_supply, num_moves):
        moves = []
        self.board = board
        self.players = players
        self.tile_supply = tile_supply
        self.player_index = player_index
        self.player = players[player_index]

        self.board_canvas.board = self.board
        self.board_canvas.tile_supply = self.tile_supply
        self.board_canvas.player = self.players[self.player_index]
        self.player = self.players[self.player_index]
        self.board_canvas.update_board()
        self.draw_human_items(self.player)
        self.is_turn = True
        while len(moves) < num_moves:
            print("getting next human move")
            if not Agent.can_make_move(board, players[player_index]):
                print("no possible moves found")
                moves.append(Move.make_move(Player.get_player_name(players[player_index]), Move.NONE_POSSIBLE))
            print("waiting for player input")
            image_id, move = self.actions_queue.get()
            moves.append(move)
            self.board_canvas.remove_moveable_item(image_id)
            self.board, self.players, self.tile_supply = Agent.apply_move(move,
                    self.board, self.tile_supply, self.player_index, self.players)
            self.board_canvas.board = self.board
            self.board_canvas.tile_supply = self.tile_supply
            self.board_canvas.player = self.players[self.player_index]
            self.player = self.players[self.player_index]
            self.board_canvas.update_board()
            self.draw_human_items(self.player)
        self.is_turn = False
        return moves

if __name__ == "__main__":
    import Game
    colors = ['Blue', 'Green', 'Yellow', 'Red']
    names = ['Nick', 'Zach', 'Brian', 'Aaron']
    players = [Player.make_player(names[i], 4, colors[i]) for i in range(4)]
    board = Board.make_board(11, 16)
    tile_supply = Tile.get_all_tiles()

    grid = BoardCanvas.GRID_SIZE
    gap = BoardCanvas.GRID_GAP
    board = Board.make_board(11, 16)
    board_canvas = BoardCanvas.BoardCanvas(board, tile_supply, additional_x= grid * 10)
    board_canvas.setup()

    def test_game():
        colors = ['Blue', 'Green', 'Yellow', 'Red']
        names = ['Nick', 'Zach', 'Brian', 'Aaron']
        players = [Player.make_player(names[i], 4, colors[i]) for i in range(4)]
        random_agent = Agent.get_random_agent()
        human_agent = HumanAgent(board_canvas, board, tile_supply, 0, players)
        agents = [human_agent.human_decision] + [random_agent] * 3
        scores = Game.play_game(board_canvas, board, players, tile_supply, agents)
        scores_list = [(name, scores[name]) for name in scores]
        scores_list.sort(key=lambda a: -a[1])
        for i in range(len(scores_list)):
            score = scores_list[i]
            print(str(i + 1) + ")", score[0], score[1])

    thread = threading.Thread(target = test_game)
    thread.start()

    board_canvas.mainloop()
