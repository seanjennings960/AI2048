import numpy as np

from board import Direction

class Policy:
    def __init__(self):
        raise NotImplementedError

    def get_action(self, board):
        raise NotImplementedError


class NewRandomPolicy:
    def __init__(self):
        pass

    def get_action(self, board):
        valid_moves = [i for i in Direction]
        found_valid_move = False
        while not found_valid_move:
            try:
                direction = np.random.choice(valid_moves)
            except ValueError:
                raise ValueError('Policy could not find any valid moves for board')

            _, _, found_valid_move = board.move(direction, copy=True)
            valid_moves.remove(direction)
        return direction