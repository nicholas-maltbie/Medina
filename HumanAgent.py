"""A human agent manages its own board and displays a board and adds moveable
pieces so a human agent can play pieces on the board from his or her hand"""

import Board
import BoardCanvas
import Player
import GameConstants
import threading

def make_human_agent(board_canvas, player):
    """Makes a human agent based off a player who plays on the given board"""

    def human_decision(board, player_index, num_moves, players):
        pass

    print(board_canvas)
    return human_decision

if __name__ == "__main__":
    board = Board.make_board(11, 16)
    player = Player.make_player("Nick", 4, "Green")

    grid = BoardCanvas.GRID_SIZE
    gap = BoardCanvas.GRID_GAP
    board_canvas = None

    board_canvas = BoardCanvas.BoardCanvas(board, additional_x= grid * 10)
    board_canvas.setup()

    offy = gap + grid // 2
    offx = board_canvas.get_board_width() + gap + grid // 2
    xnew = offx
    for color in GameConstants.BUILDINGS_COLORS:
        for i in range(Player.get_held_buildings_of_color(player, color)):
            board_canvas.add_moveable_building(color, (offx, offy))
            offx += grid + gap
            #offy += gap
            xnew = offx
        offx = board_canvas.get_board_width() + gap + grid // 2
        offy += grid + gap

    offx = board_canvas.get_board_width() + gap + grid // 2
    for i in range(Player.get_num_stables(player)):
        board_canvas.add_moveable_stable((offx, offy))
        offx += grid + gap
        #offy += gap

    offy += grid + gap
    offx = board_canvas.get_board_width() + gap + grid // 2
    for i in range(Player.get_held_rooftops(player)):
        #print(Player.get_player_color(player))
        board_canvas.add_moveable_rooftop((offx, offy), Player.get_player_color(player))
        offx += grid + gap
        if i != 0 and i % 5 == 0:
            offx = board_canvas.get_board_width() + gap + grid // 2
            offy += grid + gap

    offy += grid + gap
    offx = board_canvas.get_board_width() + gap + grid // 2
    for i in range(1, Player.get_held_walls(player) + 1):
        board_canvas.add_moveable_wall((offx, offy))
        offx += grid + gap * 2
        if i % 6 == 0:
            offx = board_canvas.get_board_width() + gap + grid // 2
            offy

    offy += grid + gap
    offx = board_canvas.get_board_width() + gap + grid // 2
    for i in range(Player.get_extra_rooftops(player)):
        #print(Player.get_player_color(player))
        board_canvas.add_moveable_rooftop((offx, offy), "Neutral")
        offx += grid + gap

    def test_game():
        human_agent = make_human_agent(board, player)

    thread = threading.Thread(target = test_game)
    thread.start()

    board_canvas.mainloop()
    #print(Player.get_player_color(nick))
    #print(nick)
