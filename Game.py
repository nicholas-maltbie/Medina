"""This module is responsible for running a game"""
import random
import Board
import BoardCanvas
import Building
import Tile
import Agent
import Player
import GameConstants
import threading
import Move
import Score

def game_over(board, players):
    """This method determines if a game is over"""
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
    """This generator will generate the number of moves per turn for any turn.
    The pattern is 1 move for the first two turns, then two moves for every turn
    after that"""
    i = 0
    while True:
        if i < 2:
            yield 1
            i += 1
        else:
            yield 2

def play_game(board_canvas, board, players, tile_supply, agents,
    start_player = -1):
    """This will play a game to completion based on a given setup and then
    will return a dictionary of {playername:score for player in players}"""
    current_player = random.randrange(len(players))
    if start_player >= 0:
        current_player = start_player
    moves_per_turn = turn_moves()
    no_moves = 0
    while True:
        num_moves = next(moves_per_turn)
        selected = Agent.get_agent_moves(agents[current_player], board, current_player, tile_supply, players, num_moves)
        all_pass = True
        for move in selected:
            if Move.get_move_type(move) != Move.NONE_POSSIBLE:
                all_pass = False
            board, players, tile_supply = Agent.apply_move(move, board, tile_supply, current_player, players)
            board_canvas.board = board
            board_canvas.tile_supply = tile_supply
            board_canvas.check_well
            board_canvas.update_board()

        if  all_pass:
            no_moves += 1
        else:
            no_moves == 0

        if no_moves == len(players) or game_over(board, players):
            board_canvas.update_board()

            get_score = Score.get_score_function(board)
            return {Player.get_player_name(player):get_score(player) for player in players}
        current_player = (current_player + 1) % len(players)

if __name__ == "__main__":
    board = Board.make_board(11,16)
    tile_supply = Tile.get_all_tiles()
    board_canvas = BoardCanvas.BoardCanvas(board, tile_supply)
    board_canvas.setup()

    def test_game():
        colors = ['Blue', 'Green', 'Yellow', 'Red']
        names = ['Nick', 'Zach', 'Brian', 'Aaron']
        players = [Player.make_player(names[i], 4, colors[i]) for i in range(4)]
        random_agent = Agent.get_random_agent()
        agents = [random_agent for _ in range(4)]
        scores = play_game(board_canvas, board, players, tile_supply, agents)
        scores_list = [(name, scores[name]) for name in scores]
        scores_list.sort(key=lambda a: -a[1])
        for i in range(len(scores_list)):
            score = scores_list[i]
            print(str(i + 1) + ")", score[0], score[1])

    thread = threading.Thread(target = test_game)
    thread.start()
    board_canvas.mainloop()
