"""The objective of this module is to take a board and to be able to determine 
its value to a specific player. This will be used to evaluate board states for 
an AI player."""

import Board
import Player

def get_player_score(board, player):
    """Gets the player's score for a specific game"""
    def get_building_score(board, building):
        """Gets the score of a building"""
        pass
    
    return 0

def get_game_value(board, players, current):
    """Determine the value of a game for the current player out of players 
    given a specific board. This will return an integer of the game value, 
    higher numbers means this is a better state for the given player."""
    return 0



