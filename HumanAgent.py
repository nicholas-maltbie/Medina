"""A human agent manages its own board and displays a board and adds moveable
pieces so a human agent can play pieces on the board from his or her hand"""

import Move
import Board
import BoardCanvas
import Player
import Tile
import GameConstants
import threading

def make_human_agent(board_canvas, player):
    """Makes a human agent based off a player who plays on the given board"""
    grid = BoardCanvas.GRID_SIZE
    gap = BoardCanvas.GRID_GAP
    drawn = {}

    def draw_human_items(player):
        offy = gap * 3 + grid * 5 / 2
        """Draws a player's items on the screen"""
        def draw_things(offy, draw_method, num_things, piece_type, x_jump = grid + gap):
            """Draws a number of things with a draw mehtod"""
            if num_things > 0:
                offx = board_canvas.get_board_width() + gap + grid // 2
                for i in range(num_things):
                    drawn[(piece_type, i)] = draw_method(offx, offy)
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

    def human_decision(board, player_index, num_moves, players):
        pass

    draw_human_items(player)
    return human_decision

if __name__ == "__main__":
    board = Board.make_board(11, 16)
    tile_supply = Tile.get_all_tiles()
    player = Player.make_player("Nick", 4, "Green")

    grid = BoardCanvas.GRID_SIZE
    gap = BoardCanvas.GRID_GAP

    board_canvas = None

    board_canvas = BoardCanvas.BoardCanvas(board, tile_supply, additional_x= grid * 10)
    board_canvas.setup()

    def test_game():
        human_agent = make_human_agent(board_canvas, player)

    thread = threading.Thread(target = test_game)
    thread.start()

    board_canvas.mainloop()
    #print(Player.get_player_color(nick))
    #print(nick)
