import numpy as np
import tensorflow as tf
import functools
import collections
import os
import random
from ttt import print_board

from network_helpers import create_network, load_network, save_network, \
    get_deterministic_network_move, get_stochastic_network_move
from tttGameSpec import TicTacToeGameSpec
from ttt import make_human_agent
import random

game_spec = TicTacToeGameSpec()

HIDDEN_NODES = (100, 100, 100)
BATCH_SIZE = 100  # every how many games to do a parameter update?
LEARN_RATE = 1e-6
PRINT_RESULTS_EVERY_X = 1000  # every how many games to print the results
NETWORK_FILE_PATH = 'AIPractice/current_network.p'  # path to save the network to
NUMBER_OF_GAMES_TO_RUN = 3


def train_policy_gradients(game_spec,
                           create_network,
                           network_file_path,
                           save_network_file_path=None,
                           opponent_func=None,
                           number_of_games=10000,
                           print_results_every=1000,
                           learn_rate=1e-4,
                           batch_size=100,
                           randomize_first_player=True):
    """Train a network using policy gradients

    Args:
        save_network_file_path (str): Optionally specifiy a path to use for saving the network, if unset then
            the network_file_path param is used.
        opponent_func (board_state, side) -> move: Function for the opponent, if unset we use an opponent playing
            randomly
        randomize_first_player (bool): If True we alternate between being the first and second player
        game_spec (games.base_game_spec.BaseGameSpec): The game we are playing
        create_network (->(input_layer : tf.placeholder, output_layer : tf.placeholder, variables : [tf.Variable])):
            Method that creates the network we will train.
        network_file_path (str): path to the file with weights we want to load for this network
        number_of_games (int): number of games to play before stopping
        print_results_every (int): Prints results to std out every x games, also saves the network
        learn_rate (float):
        batch_size (int):

    Returns:
        (variables used in the final network : list, win rate: float)
    """
    total = 0
    losses = 0
    save_network_file_path = save_network_file_path or network_file_path
    opponent_func = make_human_agent() #opponent_func or game_spec.get_random_player_func()
    reward_placeholder = tf.placeholder("float", shape=(None,))
    actual_move_placeholder = tf.placeholder("float", shape=(None, game_spec.outputs()))

    input_layer, output_layer, variables = create_network()

    policy_gradient = tf.log(
        tf.reduce_sum(tf.mul(actual_move_placeholder, output_layer), reduction_indices=1)) * reward_placeholder
    train_step = tf.train.AdamOptimizer(learn_rate).minimize(-policy_gradient)

    with tf.Session() as session:
        session.run(tf.initialize_all_variables())

        if network_file_path and os.path.isfile(network_file_path):
            print("loading pre-existing network")
            load_network(session, variables, network_file_path)

        mini_batch_board_states, mini_batch_moves, mini_batch_rewards = [], [], []
        results = collections.deque(maxlen=print_results_every)

        def make_training_move(board_state, side):
            mini_batch_board_states.append(np.ravel(board_state) * side)
            move = get_stochastic_network_move(session, input_layer, output_layer, board_state, side, game_spec=game_spec, valid_only =True)
            #print_board(board_state)
            #print(game_spec.flat_move_to_tuple(move.argmax(), side))
            mini_batch_moves.append(move)
            return game_spec.flat_move_to_tuple(move.argmax(), side)

        for episode_number in range(1, number_of_games):
            # randomize if going first or second
            if random.getrandbits(1):
                reward = game_spec.play_game(make_training_move, opponent_func)
            else:
                reward = -game_spec.play_game(opponent_func, make_training_move)

            if reward == -1:
                losses += 1
            total += 1

            print("lost", losses, "of", total, "games")

        if network_file_path:
            save_network(session, variables, save_network_file_path)

    return variables, _win_rate(print_results_every, results)


def _win_rate(print_results_every, results):
    return 0.5 + sum(results) / (print_results_every * 2.)


if __name__ == "__main__":
    create_network_func = functools.partial(create_network, game_spec.board_squares(), (300, 200, 100, 100))

    train_policy_gradients(game_spec, create_network_func, NETWORK_FILE_PATH,
                           number_of_games=NUMBER_OF_GAMES_TO_RUN,
                           batch_size=BATCH_SIZE,
                           learn_rate=LEARN_RATE,
                           print_results_every=PRINT_RESULTS_EVERY_X)
