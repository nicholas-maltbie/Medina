"""An agent is responbible for making a move decision based on a board. Players
will make two moves (unless it is the first turn, in which case only one move
is allowed)

This module will have support for getting all possible moves (or ranges for
all types of moves as there are many similar moves of the same type such as
placing buildings or stables).

A agent only needs to be the following function:
make_decision(board, current, players, tile_supply, num_moves)
    - board is the game board
    - current is the player making the move (index)
    - players are the players in the game
    - tile_supply the game's tile supply
    - num_moves is the number of moves the agent can make

This function must return a list of moves that the player makes."""

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

def can_make_move(move, board, player):
    """Checks if a player can make a move"""
    for color in GameConstants.BUILDINGS_COLORS:
        for loc in Board.get_building_piece_locations(board, color):
            if(Player.get_held_buildings_of_color(player, color) > 0):
                return True
        building = Board.get_active_building(board, color)
        has_claimed = False
        for building in Board.get_buildings_by_color(board, color):
            if Building.get_owner(building) == Player.get_player_name(player):
                has_claimed = True
        if not has_claimed and Board.get_active_building(board, color) != None and \
                not Building.has_owner(Board.get_active_building(board, color)):
            for loc in Building.get_building_locations(building):
                return True
    for loc in Board.get_stable_piece_location(board):
        if(Player.get_num_stables(player) > 0):
            return True
    for loc in Board.get_merchant_place_locations(board):
        if(Player.get_held_merchants(player) > 0):
            return True
    for loc in Tower.get_possible_wall_additions(Board.get_towers(board)):
        if(Player.get_held_walls(player) > 0):
            return True

    has_tea = False
    for tile in Player.get_tiles(player):
        if Tile.get_tile_type(tile) == Tile.TEA_TILE:
            has_tea = True
    if has_tea:
        return True
    return False

def is_valid_move(move, board, player):
    """Checks if a move is valid for a given player"""
    move_type = Move.get_move_type(move)
    if move_type == Move.NONE_POSSIBLE:
        return not can_make_move(board, player)
    if move_type == Move.PASS:
        return Player.get_tiles_of_type(player, Tile.TEA_TILE) > 0
    else:
        piece = Move.get_piece(move)
        move_loc = Move.get_location(move)
        if piece == Move.BUILDING:
            move_color = Move.get_move_color(move)
            return Player.get_held_buildings_of_color(player, move_color) <= 0 and
                    move_loc in Board.get_building_piece_locations(board) and
                    move_loc in Building.get_building_piece_attach(Board.get_active_building(board, move_color))
        elif piece == Move.STABLE:
            return Player.get_num_stables(player) > 0 and
                    move_loc in Board.get_stable_piece_location(board)
        elif piece == Move.MERCHANT:
            return Player.get_held_merchants(player) > 0 and
                    move_loc in Board.get_merchant_place_locations(board)
        elif piece == Move.ROOFTOP:
            if Plyaer.get_held_rooftops(player) <= 0:
                return Falses
            move_color = Move.get_move_color(move)
            claimed_building = Board.get_active_building(board, color)
            if move_loc not in Building.get_building_locations(claimed_building):
                return False
            for building in Board.get_buildings_by_color(board, move_color):
                if Building.get_owner(building) == Player.get_player_name(player):
                    return False
            return True
        elif piece == Move.WALL:
            return Player.get_held_walls(player) > 0 and move_loc in Tower.get_possible_wall_additions
        return False

def apply_move(move, board, tile_supply, player_index, players):
    """Applys a given move to a board and returns a new board with the move
    applyed to it. The original board remains unchanged."""
    def get_tile_from_supply(tile_supply, tile_type, value=0):
        """Gets a tile from the supply"""
        for i in range(len(tile_supply)):
            tile = tile_supply[i]
            if Tile.get_tile_value(tile) == value and Tile.get_tile_type(tile) == tile_type:
                return tile_supply.pop(i)
        return None

    def get_tile_from_all(players, tile_type, value=0):
        """Gets a tile from any of the players, returns the first tile found"""
        for other in players:
            taken = Player.take_tile(other, tile_type, value)
            if taken != None:
                return taken
        return None

    def get_tile_from_others(players, player_index, tile_type, value=0):
        """Gets a tile from other players, player_index is the current player"""
        for other in players:
            if other != players[player_index]:
                taken = Player.take_tile(other, tile_type, value)
                if taken != None:
                    return taken
        return None

    def get_buildings_adjacent_to_tower(towers, num, board):
        """Gets all the buildings adjacent to the tower's walls"""
        walls = set(Tower.get_wall_locations_for_tower(towers, num - 1))
        def is_building_adj(building):
            """Checks if a building is adjacent to the tower"""
            for loc in Building.get_building_stable_orthogonal(building):
                if loc in walls:
                    return True
            return False
        adj = []
        for building in Board.get_buildings(board):
            if is_building_adj(building):
                adj.append(building)
        return adj

    def get_player_with_name(players, name):
        """Gets a player with a given name and returns none if there are no
        players with the given name."""
        for player in players:
            if Player.get_player_name(player) == name:
                return player
        return None

    def get_adj_towers_to_building(towers, building):
        """Gets all the towers adjacent to the building. Returns the tower
        numbers of the adjacent towers as a list."""
        building_adj = set(Building.get_building_stable_orthogonal(building))
        def is_adj_to_tower(num):
            """Checks if a given building is adjacent to the tower of number
            tower_num from towers"""
            tower_adj = Tower.get_wall_locations_for_tower(towers, num - 1)
            for wall in tower_adj:
                if wall in building_adj:
                    return True
            return False
        connected = []
        for num in range(1, 5):
            if is_adj_to_tower(num):
                connected.append(num)
        return connected

    board = Board.clone_board(board)
    tile_supply = [Tile.clone_tile(tile) for tile in tile_supply]
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
                    before_adj = get_adj_towers_to_building(Board.get_towers(board), building)
                    Building.attach_stable_location(building, loc)
                    after_adj = get_adj_towers_to_building(Board.get_towers(board), building)
                    new_towers = []
                    for t in after_adj:
                        if t not in before_adj:
                            new_towers.append(t)
                    if Building.has_owner(building):
                        new_owner = Building.get_owner(building)
                        for num in set(new_towers):
                            #we have a new owner
                            tile = get_tile_from_supply(tile_supply, Tile.TOWER_TILE, num)
                            if tile == None:
                                tile = get_tile_from_all(players, Tile.TOWER_TILE, num)
                            if new_owner == Building.NEUTRAL_OWNER:
                                tile_supply.append(tile)
                            else:
                                new_owner = get_player_with_name(players, new_owner)
                                Player.give_tile(new_owner, tile)

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
                from_supply = get_tile_from_supply(tile_supply, Tile.PALACE_TILE, Tile.PALACE_VALUES[color])
                if from_supply != None:
                    Player.give_tile(player, from_supply)
                else:
                    from_others = get_tile_from_others(players, player_index, Tile.PALACE_TILE, Tile.PALACE_VALUES[color])
                    Player.give_tile(player, from_others)

            if color == TEA_COLOR:
                num = len(Board.get_buildings_by_color(board, TEA_COLOR))
                for i in range(4 - num):
                    Player.give_tile(player, get_tile_from_supply(tile_supply, Tile.TEA_TILE))

            adj = set(get_adj_towers_to_building(Board.get_towers(board), claimed_building))
            for tower_num in adj:
                tile = get_tile_from_supply(tile_supply, Tile.TOWER_TILE, tower_num)
                if tile == None:
                    tile = get_tile_from_all(players, Tile.TOWER_TILE, tower_num)
                Player.give_tile(player, tile)

        elif piece == Move.WALL:
            towers = Board.get_towers(board)
            Player.play_wall(player)
            for num in range(1, 5):
                tower = Tower.get_tower(towers, num)
                added = False
                before_adj = set()
                if loc == (Tower.get_tower_addition_c(towers, num)):
                    before_adj = get_buildings_adjacent_to_tower(Board.get_towers(board), num, board)
                    Tower.add_tower_c(tower)
                    added = True
                elif loc == (Tower.get_tower_addition_r(towers, num)):
                    before_adj = get_buildings_adjacent_to_tower(Board.get_towers(board), num, board)
                    Tower.add_tower_r(tower)
                    added = True

                if added:
                    buildings = get_buildings_adjacent_to_tower(Board.get_towers(board), num, board)
                    new_buildings = []
                    for b in buildings:
                        if b not in before_adj:
                            new_buildings.append(b)
                    if len(new_buildings) > 0:
                        #we have a new owner
                        new_building = new_buildings[0]
                        if Building.has_owner(new_building):
                            new_owner = Building.get_owner(new_building)
                            tile = get_tile_from_supply(tile_supply, Tile.TOWER_TILE, num)
                            if tile == None:
                                tile = get_tile_from_all(players, Tile.TOWER_TILE, num)
                            if new_owner == Building.NEUTRAL_OWNER:
                                tile_supply.append(tile)
                            else:
                                new_owner = get_player_with_name(players, new_owner)
                                Player.give_tile(new_owner, tile)

    return board, players, tile_supply

def get_agent_moves(agent, board, current, tile_supply, players, num_moves=2):
    """Gets the moves made by an agent for his/her/it's turn."""
    return agent(board, current, players, tile_supply, num_moves)

def get_random_agent():
    """A random agent for testing the functionality of the agent."""
    import random
    def make_moves(board, player_index, players, tile_supply, num_moves):
        moves = []
        for i in range(num_moves):
            move = random.choice(get_all_possible_moves(players[player_index], board))
            board, players, tile_supply = apply_move(move, board, tile_supply, player_index, players)
            moves.append(move)
        return moves;
    return make_moves;
