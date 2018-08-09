import numpy as np
import time

from Board2048 import Board2048
from board import Board

BUFFER_SIZE = 100


def get_history_dtype(board_shape, board_dtype):
    return [('state', board_dtype, board_shape), ('action', int),
            ('after_state', board_dtype, board_shape), ('reward', int),
            ('return', int)]


def sum_cumulative_returns(move_history):
    returns_array = np.zeros(move_history.shape)
    cumulative_returns = 0
    for i in range(returns_array.shape[0] - 1, -1, -1):
        cumulative_returns += move_history[i]['reward']
        returns_array[i] = cumulative_returns

    return returns_array


class EpisodeGenerator:
    def __init__(self):
        self.history_dtype = get_history_dtype((4, 4), int)

    def play_policy(self, policy):
        """Play through and episode and return the move history"""
        board = Board2048()

        move_history = np.full((BUFFER_SIZE,), np.nan, dtype=self.history_dtype)
        move_num = 0

        action_times = []
        move_times = []
        gen_times = []

        while not board.gameOver():
            if move_num == move_history.shape[0]:
                move_history = np.r_[move_history, np.full((BUFFER_SIZE,), np.nan,
                                                           dtype=self.history_dtype)]
            t_start = time.time()
            action = policy.get_action(board)
            action_times.append(time.time() - t_start)
            move_history['state'][move_num] = board.tiles
            move_history['action'][move_num] = action.value

            # Perform move
            t_start = time.time()
            reward = board.move(action, afterState=True)
            move_times.append(time.time() - t_start)
            move_history['after_state'][move_num] = board.tiles
            move_history['reward'][move_num] = reward

            t_start = time.time()
            board.genNewTile()
            gen_times.append(time.time() - t_start)
            move_num += 1


        print('Getting action: ', np.mean(action_times))
        print('Performing move: ', np.mean(move_times))
        print('Generating new tile: ', np.mean(gen_times))
        # Slice out extra entries in buffer before calculating return
        move_history = move_history[:move_num]

        move_history['return'] = sum_cumulative_returns(move_history)

        return move_history

    def play_policy_multi(self, policy, num_episodes, verbose=False):
        """Play a single policy, num_episodes times.
        Returns single move_history vector."""
        move_history = np.zeros((0,), dtype=self.history_dtype)
        for num_episode in range(num_episodes):
            if verbose:
                print('Running episode: ', num_episode)
            # Play the policy and append to move history vector
            move_history = np.r_[move_history, self.play_policy(policy)]

        return move_history

class NewEpisodeGenerator:
    def __init__(self, board_size=4):
        board = Board(board_size)
        squares = board.squares
        self.history_dtype = get_history_dtype(squares.shape, squares.dtype)

    def play_policy(self, policy):
        board = Board()

        move_history = np.full((BUFFER_SIZE,), np.nan, dtype=self.history_dtype)
        move_num = 0

        action_times = []
        move_times = []
        gen_times = []

        while not board.game_over():
            if move_num == move_history.shape[0]:
                move_history = np.r_[move_history, np.full((BUFFER_SIZE,), np.nan,
                                                           dtype=self.history_dtype)]
            t_start = time.time()
            action = policy.get_action(board)
            action_times.append(time.time() - t_start)
            move_history['state'][move_num] = board.squares
            move_history['action'][move_num] = action.value

            # Perform move
            t_start = time.time()
            _, reward, _ = board.move(action, new_tile=False)
            move_times.append(time.time() - t_start)
            move_history['after_state'][move_num] = board.squares
            move_history['reward'][move_num] = reward

            t_start = time.time()
            board.gen_new_tile()
            gen_times.append(time.time() - t_start)
            move_num += 1


        print('Getting action: ', np.mean(action_times))
        print('Performing move: ', np.mean(move_times))
        print('Generating new tile: ', np.mean(gen_times))
        # Slice out extra entries in buffer before calculating return
        move_history = move_history[:move_num]

        move_history['return'] = sum_cumulative_returns(move_history)

        return move_history


    def play_policy_multi(self, policy, num_episodes, verbose=False):
        """Play a single policy, num_episodes times.
        Returns single move_history vector."""
        move_history = np.zeros((0,), dtype=self.history_dtype)
        for num_episode in range(num_episodes):
            if verbose:
                print('Running episode: ', num_episode)
            # Play the policy and append to move history vector
            move_history = np.r_[move_history, self.play_policy(policy)]

        return move_history
