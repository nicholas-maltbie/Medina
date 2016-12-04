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
import GameConstants

def get_all_possible_moves(player, board):
    """Gets all the differnt VALID moves that a player can be made in a board.
    If there are no valid moves, a move of NONE_POSSIBLE will be returned."""
    possible = []
    for color in GameConstants.BUILDINGS_COLORS:
        for loc in Board.get_building_piece_locations(board, color):
            if(Player.get_held_buildings_of_color(player, color) > 0):
                possible.append(Move.make_move(Player.get_player_name(player), Move.NORMAL, Move.BUILDING, loc, color))
            if(Player.get_num_stables(player) > 0):
                possible.append(Move.make_move(Player.get_player_name(player), Move.NORMAL, Move.STABLE, loc, color))
        building = Board.get_active_building(board, color)
        has_claimed = False
        for building in Board.get_buildings_by_color(board, color):
            if Building.get_owner(building) == Player.get_player_name(player):
                has_claimed = True
        if not has_claimed and building != None:
            for loc in Building.get_building_locations(building):
                possible.append(Move.make_move(Player.get_player_name(player), Move.NORMAL, Move.ROOFTOP, loc, color))
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
            Building.assign_owner(Board.get_active_building(board, color), Player.get_player_color(player), loc)
            Board.get_buildings_by_color(board, color)
            claimed = []
            for building in Board.get_buildings_by_color(board, color):
                if Building.has_owner(building) and Building.get_owner(building) != Building.NEUTRAL_OWNER:
                    claimed.append(building.get_owner(building))
            if len(claimed) == len(players):
                for player in players:
                    Player.remvoe_all_buildings_of_color(player, color)
        elif piece == Move.WALL:
            for num in range(1, 5):
                tower = Tower.get_tower(Board.get_towers(board), num)
                h_mod = -1
                v_mod = -1
                if num == 0 or num == 2:
                    h_mod = 1
                if num == 0 or num == 1:
                    v_mod = 1
                start = make_location(-1, -1)
                if num == 1:
                    start = make_location(-1, get_columns(towers))
                elif num == 2:
                    start = make_location(get_rows(towers), -1)
                elif num == 3:
                    start = make_location(get_rows(towers), get_columns(towers))
                tower = get_tower(towers, num + 1)

                if loc == (get_translate(start, 0, h_mod * (get_columns(tower) + 1))):
                    Tower.add_tower_c(tower)
                elif loc == (get_translate(start, v_mod * (get_rows(tower) + 1), 0)):
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
