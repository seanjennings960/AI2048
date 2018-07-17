import numpy as np

from Board2048 import Board2048

BUFFER_SIZE = 100
HISTORY_DTYPE = [('state', int, (4, 4)), ('action', int),
                 ('after_state', int, (4, 4)), ('reward', int)]


class EpisodeGenerator:
    def __init__(self):
        pass

    def play_policy(self, policy):
        """Play through and episode and return the move history"""
        board = Board2048()

        move_history = np.full((BUFFER_SIZE,), np.nan, dtype=HISTORY_DTYPE)
        move_num = 0

        while not board.gameOver():
            if move_num == move_history.shape[0]:
                move_history = np.r_[move_history, np.full((BUFFER_SIZE,), np.nan,
                                                           dtype=HISTORY_DTYPE)]
            action = policy.get_action(board)
            move_history['state'][move_num] = board.tiles
            move_history['action'][move_num] = action.value

            # Perform move
            reward = board.move(action, afterState=True)
            move_history['after_state'][move_num] = board.tiles
            move_history['reward'][move_num] = reward

            board.genNewTile()
            print(move_num)
            move_num += 1

        return move_history[:move_num]
