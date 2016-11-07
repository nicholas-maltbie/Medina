"""The intelligent AI is a computer agent that intelligently makes decisions.

There will need to be a high level basis for an agent to process and submit 
moves. This module is used to make decicons and use the formation (which will be
created later).

The AI will look at at all moves and select the best moves (this is where the 
AI and machine learning is important). From these moves, the agent will randomly 
select moves and only evaulate those few moves. Then the AI will assume moves 
for the opponent and repeat this process on the results. After a few generations 
of this process, the agent will evaulate the state of the results and select 
the move that has the best result. 

tree thingy
x = number of selected moves per generation

          *start                (1 state, gen 1)
(select moves from possible)
     /      |      \
    *       *       *           (x^2 states, gen 2)
 [assume opponent moves]
    |       |       |
(repeat process from start)
                                (x^3 states, gen 3)
           ...

(x^n, n is number of generations)
evaulate the final moves and relate them back to the first generation.
Whichever first generation had the best moves as results will be selected 
as the current move. New states will be serached for in a breadth first search 
so they can all be evaluated compared to each other.
"""

import Player
import Board

def get_pratical_moves(board, current, num_moves, num_results):
    """Gets the pratical move combinations for the agent to consider.
    
    This should return a list of sets of moves at most num_results long"""
    pass

def get_monte_carlo_agent(moves_per_branch, num_generations):
    def make_moves(board, current, num_moves, players):
        #build a queue for search.
        
        #search possiblity tree:
        #   Get all pratical moves
        #   Select a few of these pratical moves
        #   Evaulate the results of each of these moves and put them in the queue
        #   Read back from the queue num_generations times
        
        #evaulate the final board states
        
        #select initial move with best results
        
        #touch the blessed monkey idol for good luck
        
        #return initial move set
        pass
    return make_moves

