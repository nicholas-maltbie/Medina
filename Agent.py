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
import Market
import Player
import Tower
import Building
import Tile
import Location
import GameConstants

TEA_COLOR = GameConstants.BUILDINGS_COLORS[1]

def get_all_possible_moves(player, board):
    """Gets all the differnt VALID moves that a player can be made in a board.
    If there are no valid moves, a move of NONE_POSSIBLE will be returned."""
    possible = []
    for color in GameConstants.BUILDINGS_COLORS:
        for loc in Board.get_building_piece_locations(board, color):
            if(Player.get_held_buildings_of_color(player, color) > 0):
                possible.append(Move.make_move(Player.get_player_name(player), Move.NORMAL, Move.BUILDING, loc, color))
        building = Board.get_active_building(board, color)
        has_claimed = False
        for building in Board.get_buildings_by_color(board, color):
            if Building.get_owner(building) == Player.get_player_name(player):
                has_claimed = True
        if not has_claimed and Board.get_active_building(board, color) != None and \
                not Building.has_owner(Board.get_active_building(board, color)):
            for loc in Building.get_building_locations(building):
                possible.append(Move.make_move(Player.get_player_name(player), Move.NORMAL, Move.ROOFTOP, loc, color))
    for loc in Board.get_stable_piece_location(board):
        if(Player.get_num_stables(player) > 0):
            possible.append(Move.make_move(Player.get_player_name(player), Move.NORMAL, Move.STABLE, loc, color))
    for loc in Board.get_merchant_place_locations(board):
        if(Player.get_held_merchants(player) > 0):
            possible.append(Move.make_move(Player.get_player_name(player), Move.NORMAL, Move.MERCHANT, loc))
    for loc in Tower.get_possible_wall_additions(Board.get_towers(board)):
        if(Player.get_held_walls(player) > 0):
            possible.append(Move.make_move(Player.get_player_name(player), Move.NORMAL, Move.WALL, loc))

    has_tea = False
    for tile in Player.get_tiles(player):
        if Tile.get_tile_type(tile) == Tile.TEA_TILE:
            has_tea = True
    if has_tea:
        possible.append(Move.make_move(Player.get_player_name(player), Move.PASS))

    if not possible:
        possible.append(Move.make_move(Player.get_player_name(player), Move.NONE_POSSIBLE))

    return possible

def apply_move(move, board, player_index, players):
    """Applys a given move to a board and returns a new board with the move
    applyed to it. The original board remains unchanged."""
    board = Board.clone_board(board)
    players = [Player.clone_player(player) for player in players]
    player = players[player_index]
    if Move.get_move_type(move) == Move.NONE_POSSIBLE:
        pass
    elif Move.get_move_type(move) == Move.PASS:
        Player.lose_tile(player, Tile.TEA_TILE, 0)
    else:
        piece = Move.get_piece(move)
        loc = Move.get_location(move)
        if piece == Move.BUILDING:
            color = Move.get_move_color(move)
            Player.play_building(player, color)
            if Board.get_active_building(board, color) == None:
                Board.start_new_building(board, loc, color)
            else:
                Building.attach_building_locations(Board.get_active_building(board, color), loc)
        elif piece == Move.STABLE:
            Player.play_stable(player)
            for building in Board.get_buildings(board):
                if loc in Building.get_building_peice_attach(building):
                    Building.attach_stable_location(building, loc)
        elif piece == Move.MERCHANT:
            Player.play_merchant(player)
            Market.add_merchant_to_market(Board.get_market(board), loc)
        elif piece == Move.ROOFTOP:
            color = Move.get_move_color(move)
            Player.play_rooftop(player)
            claimed_building = Board.get_active_building(board, color)
            Building.assign_owner(claimed_building, Player.get_player_name(player), Player.get_player_color(player), loc)
            Board.get_buildings_by_color(board, color)
            claimed = []
            size = len(Building.get_building_locations(claimed_building))
            is_largest = True
            for building in Board.get_buildings_by_color(board, color):
                if Building.has_owner(building) and Building.get_owner(building) != Building.NEUTRAL_OWNER:
                    claimed.append(Building.get_owner(building))
                if claimed_building != building and len(Building.get_building_locations(building)) >= size:
                    is_largest = False
            if len(claimed) == len(players):
                for player in players:
                    Player.remvoe_all_buildings_of_color(player, color)
            if is_largest:
                for other in players:
                    if other != player:
                        Player.lose_tile(other, Tile.PALACE_TILE, Tile.PALACE_VALUES[color])
                    else:
                        Player.give_tile(player, Tile.make_tile(Tile.PALACE_TILE, Tile.PALACE_VALUES[color]))

            if color == TEA_COLOR:
                num = len(Board.get_buildings_by_color(board, TEA_COLOR))
                for i in range(4 - num):
                    Player.give_tile(player, Tile.make_tile(Tile.TEA_TILE))

        elif piece == Move.WALL:
            towers = Board.get_towers(board)
            Player.play_wall(player)
            for num in range(1, 5):
                tower = Tower.get_tower(towers, num)
                if loc == (Tower.get_tower_addition_c(towers, num)):
                    Tower.add_tower_c(tower)
                elif loc == (Tower.get_tower_addition_r(towers, num)):
                    Tower.add_tower_r(tower)
    return board, players

def get_agent_moves(agent, board, current, num_moves=2, players=None):
    """Gets the moves made by an agent for his/her/it's turn."""
    return agent(board, current, num_moves, players)

def get_random_agent():
    """A random agent for testing the functionality of the agent."""
    import random
    def make_moves(board, player_index, num_moves, players):
        moves = []
        for i in range(num_moves):
            move = random.choice(get_all_possible_moves(players[player_index], board))
            board, players = apply_move(move, board, player_index, players)
            moves.append(move)
        return moves;
    return make_moves;
