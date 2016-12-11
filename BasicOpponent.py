"""This module will contain the code to run a basic opponent that is not
difficult to defeat, but will hopefully pose more of a challenge than a
random AI"""

import Board
import Location
import GameConstants
import Building
import Tower

def evaluate_move(move, board, current, players, tile_supply):
    """This will evaluate a move and return a float of the
    value that this move is considered to have.
    place a rooftop - this should only be done if there is a building of
        at least value 4 or greater (unless if there is no other option).
        If a building has a lot of competition, this will favor more
        buildings with a high value.
    place a stable - this should preferably only be done to buildings that
        are owned by this player. This can be used if it would enhance
        the value of a building by connecting it to a wall or merchants.
        There should be no planning ahead for moves on future turns.
    place a merchant - this should be done if it gets points for the
        player or if there is no other option. If there is no other option
        and the opponent has to place a merchant, this will survey the
        current locations that a merchant can be placed an select the
        one that scores highest on a comparison of distance from the
        objective versus size of buildings that it would be close to. This
        does not take into account the presence of other players' buildings.
    place a wall - this will only be done to get points for the current
        player or merchants. this will follow a similar method as the
        place a merchant protocol
    place a building - this will be divided into two categories,
        adding to a building
        starting a new building
        - adding is rated more highly if the player does not yet own that
        building color. when adding to a building, if the player does not
        yet own it will value good locations (near the merchants/walls/well)
        higher than lower value loations. If the player already owns a
        building of that color, it will invert the placement rules.
        - starting a building works the same as adding to a building but it
        will additionally include the potentail for grown and competition.
        These rules will be inverted when the player already owns a building
        of that color.
    using a tea tile - If the player can use a tea tile, it will be
        kept as a static option and only used if there is a building that
        is valued below a threshold.
    """


def make_basic_decision(board, current, players, tile_supply, num_moves, mutate,
    evaluate=evaluate_move):
    """This is the agent for a basic agent. It has no memory of previous moves
    and only looks at the board and makes an educated guess at what action
    it should take. This will evaluate the benefit of each differnt 'good'
    (good means both valid and a optoin that benefits the player)
    option it has, throw these options into a heap and select the best move that
    it thinks it should make. Depending on the best move it selected first, it
    may select a different best second move hence the need for a heap. After
    the possible moves are evaluated, they will be sorted and the best will
    be selected.

    Some threshold values are used to make these decisions and could be tuned
    using a genetic algorithm.
    """

    #pre calculated values for use in the evaluation:
    #bonus locations of value 1
    bonus_locations = set()
    for street in Board.get_market(board):
        for merchant in street:
            bonus_locations.add(merchant)
    for tower_num in range(1, 5):
        for wall in Tower.get_wall_locations_for_tower(Board.get_towers(board, tower_num)):
            bonus_locations.add(wall)
    #bonus locations from well (value 4)
    well_location = Board.get_well(board)
    well_locs = set(Location.get_double_orthogonal(well_location))

    def get_building_score(building):
        """This will get the score of a building based on the pre calculated
        well locations and bonus locations for the board"""
        points = len(Building.get_building_and_stables(building))
        points += len(bonus_locations.intersection(Building.get_building_stable_orthogonal(building)))
        points += 4 * len(well_locs.intersection(Building.get_building_and_stables(building)))
        return points

    #Considered is the list of moves versus their value stored in a tuple.
    #   The first index if the move, the second is the value. A higher
    #   value signifies a better move. The valeus idealy will stay between
    #   0 and 1 as flaots.
    considered = []

    #This is the score in which a building is judged to be worth claiming
    #   100% of the time. This will allow moves to be worth more than 1
    score_threshold = 10
    #This is the minimum value of a building that is found worth claiming
    min_score_threshold = 4

    rooftop_moves = []
    for color in GameConstants.BUILDINGS_COLORS:
