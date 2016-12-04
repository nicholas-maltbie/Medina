"""This will run a test game with random AIs displaying on a board canvas"""

import Board
import BoardCanvas
import Agent
import Player
import GameConstants
import threading

board = Board.make_board(11,16)
board_canvas = BoardCanvas.BoardCanvas(board)
board_canvas.setup()

def play_game(board, board_canvas):
    import time
    time.sleep(5)
    players = [Player.make_player("Steve", 4, color) for color in ['Blue', 'Green', 'Yellow', 'Red']]
    random_agent = Agent.get_random_agent()
    agents = [random_agent for _ in range(4)]

    def turn_moves():
        i = 0
        while True:
            if i < 2:
                yield 1
            else:
                yield 2
            i += 1
    current_player = 0
    while True:
        #def get_agent_moves(agent, board, current, num_moves=2, players=None):
        moves_per_turn = turn_moves()
        moves = next(moves_per_turn)

        selected = Agent.get_agent_moves(agents[current_player], board, current_player, moves, players)

        for move in selected:
            board, players = Agent.apply_move(move, board, current_player, players)
        board_canvas.board = board
        board_canvas.update_board()
        current_player = (current_player + 1) % len(players)
        time.sleep(5)
        print(board)

thread = threading.Thread(target = play_game, args=[board, board_canvas])
thread.start()
#play_game(board, board_canvas)
board_canvas.mainloop()
