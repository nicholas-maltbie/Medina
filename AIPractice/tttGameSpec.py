from ttt import *

class TicTacToeGameSpec(BaseGameSpec):
    def __init__(self):
        pass

    def new_board(self):
        return make_board()

    def apply_move(self, board_state, move):
        return apply_move(board_state, move);

    def available_moves(self, board_state, side):
        return get_possible_moves(side)

    def board_dimensions(self):
        return 3, 3

    def has_winner(self, board_state):
        return check_winner(board_state) != None

    def play_game(self, plus_player_func, minus_player_func, log=False, board_state=None):
        """Run a single game of until the end, using the provided function args to determine the moves for each
        player.

        Args:
            plus_player_func ((board_state(3 by 3 tuple of int), side(int)) -> move((int, int))): Function that takes the
                current board_state and side this player is playing, and returns the move the player wants to play.
            minus_player_func ((board_state(3 by 3 tuple of int), side(int)) -> move((int, int))): Function that takes the
                current board_state and side this player is playing, and returns the move the player wants to play.
            log (bool): If True progress is logged to console, defaults to False
            board_state: Optionally have the game start from this position, rather than from a new board

        Returns:
            int: 1 if the plus_player_func won, -1 if the minus_player_func won and 0 for a draw
        """
        board_state = board_state or self.new_board()
        player_turn = 1

        while True:
            winner = check_winner(board_state)

            if winner == 'cat':
                # draw
                if log:
                    print("Game ended in a draw")
                return 0.
            if player_turn > 0:
                move = plus_player_func(board_state, 1)
            else:
                move = minus_player_func(board_state, -1)

            if move not in get_possible_moves(board_state, player_turn):
                # if a player makes an invalid move the other player wins
                if log:
                    print("illegal move ", move)
                return -player_turn

            board_state = self.apply_move(board_state, move)
            if log:
                print_board(board_state)

            winner = check_winner(board_state)
            if winner == 'cat':
                # draw
                if log:
                    print("Game ended in a draw")
                return 0.
            if winner != None:
                if log:
                    print("we have a winner, side: %s" % player_turn)
                return winner
            player_turn = -player_turn

    def get_random_player_func(self):
        return make_random_agent()

    def flat_move_to_tuple(self, move_index, side):
        return make_move(move_index // 3, move_index % 3, side)

    def tuple_move_to_flat(self, tuple_move):
        return get_move_row(tuple_move) * 3 + get_move_col()

if __name__ == '__main__':
    # example of playing a game
    TicTacToeGameSpec().play_game(make_random_agent(), make_random_agent(), log=True)
