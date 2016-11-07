"""An agent is responbible for making a move decision based on a board. Players 
will make two moves (unless it is the first turn, in which case only one move 
is allowed)

This module will have support for getting all possible moves (or ranges for 
all types of moves as there are many similar moves of the same type such as 
placing buildings or stables).

A agent only needs to be the following function:
make_decision(board, current, num_moves, players)
    - board is the game board
    - current is the player making the move
    - num_moves is the number of moves the agent can make
    - players are the players in the game

This function must return a list of moves that the player makes.

If players in None, it represents a limited decision. If players is the list 
of all players in the game, it represents a normal decision.

The difference between a normal decision and a limited decision is a limited 
decision is made without knowledge of the other players' hands (as the game is 
normally played) while make_decision allows the AI to cheat (or act like a 
person who has very good memory)."""

import Move
import Board
import Player

def get_all_possible_moves(player, board):
    """Gets all the differnt VALID moves that a player can be made in a board.
    If there are no valid moves, a move of NONE_POSSIBLE will be returned."""
    pass

def is_move_valid(move, board):
    """Checks if a move is valid"""
    pass

def apply_move(move, board):
    """Applys a given move to a board and returns a new board with the move 
    applyed to it. The original board remains unchanged."""
    pass

def get_agent_moves(agent, board, current, num_moves=2, players=None):
    """Gets the moves made by an agent for his/her/it's turn."""
    return agent(board, current, num_moves, players)

def get_random_agent()
    """A random agent for testing the functionality of the agent."""
    import random
    def make_moves(board, current, num_moves, players):
        moves = []
        for i in range(num_moves):
            move = random.choice(get_all_possible_moves(current, board))
            board = apply_move(move, board)
            moves.append(move)
        return moves;
    return make_moves;

