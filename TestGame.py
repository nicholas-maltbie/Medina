"""This will run a test game with random AIs displaying on a board canvas"""

import Board
import BoardCanvas
import Building
import Agent
import Player
import GameConstants
import threading
import Move

board = Board.make_board(11,16)
board_canvas = BoardCanvas.BoardCanvas(board)
board_canvas.setup()

def play_game(board, board_canvas):
    import time
    time.sleep(1)
    colors = ['Blue', 'Green', 'Yellow', 'Red']
    names = ['Nick', 'Zach', 'Brian', 'Aaron']
    players = [Player.make_player(names[i], 4, colors[i]) for i in range(4)]
    random_agent = Agent.get_random_agent()
    agents = [random_agent for _ in range(4)]

    def game_over(board, players):
        all_names = set([Player.get_player_name(player) for player in players])
        for color in GameConstants.BUILDINGS_COLORS:
            claimed = set()
            for building in Board.get_buildings_by_color(board, color):
                if Building.has_owner(building) and Building.get_owner(building) != Building.NEUTRAL_OWNER:
                    claimed.add(Building.get_owner(building))
            if claimed != all_names:
                return False
        return True

    def turn_moves():
        i = 0
        while True:
            if i < 2:
                yield 1
                i += 1
            else:
                yield 2

    current_player = 0
    moves_per_turn = turn_moves()
    no_moves = 0
    while True:
        #def get_agent_moves(agent, board, current, num_moves=2, players=None):
        moves = next(moves_per_turn)
        #print(moves)
        selected = Agent.get_agent_moves(agents[current_player], board, current_player, moves, players)
        #print(selected)
        all_pass = True
        for move in selected:
            if Move.get_move_type(move) != Move.NONE_POSSIBLE:
                all_pass = False
            print(move)
            board, players = Agent.apply_move(move, board, current_player, players)
            board_canvas.board = board
            board_canvas.check_well
            board_canvas.update_board()
            #time.sleep(0.5)
        if  all_pass:
            no_moves += 1
        else:
            no_moves == 0

        if no_moves == len(players) or game_over(board, players):
            board_canvas.update_board()
            time.sleep(3)
            board = Board.make_board(11,16)
            thread = threading.Thread(target = play_game, args=[board, board_canvas])
            board_canvas.board = board
            board_canvas.clear_board()
            board_canvas.check_well()
            board_canvas.update_board()
            thread.start()
            return
        current_player = (current_player + 1) % len(players)
        #time.sleep(0.1)
        #print(board)

thread = threading.Thread(target = play_game, args=[board, board_canvas])
thread.start()
#play_game(board, board_canvas)
board_canvas.mainloop()
