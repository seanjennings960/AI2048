import numpy as np
from enum import Enum

NUM_STARTING_SQUARES = 2

def move_without_combine(board):
    tiles_per_row = np.sum(~np.isnan(board), axis=-1)
    # print('tiles_per_row', tiles_per_row)
    new_indices_flat = np.array([], dtype=int)
    for i in range(board.shape[0]):
        row_start = i * board.shape[-1]
        new_indices_flat = np.r_[new_indices_flat,
            np.arange(tiles_per_row[i]) + row_start]
    # print('new_indices_flat', new_indices_flat)

    board_temp = np.full(board.shape, np.nan)
    # print('Previous board values: ', board_out.flat[new_indices_flat])
    board_temp.flat[new_indices_flat] = board[~np.isnan(board)]
    board[:] = board_temp


def find_combine_tiles(board):
    next_true = np.zeros(board.shape, dtype=bool)
    is_next = np.zeros(board.shape, dtype=bool)

    for i in range(next_true.shape[-1] - 1):
        are_same = np.logical_and(board[:, i] == board[:, i + 1],
                                  ~np.isnan(board[:, i]))
        next_true[:, i] = np.logical_and(are_same, ~is_next[:, i])
        is_next[:, i + 1] = next_true[:, i]
    return next_true, is_next

def combine(board):
    next_true, is_next = find_combine_tiles(board)
    board[next_true] *= 2
    board[is_next] = np.nan
    return np.sum(board[next_true])


def move_left(board):
    move_without_combine(board)
    score = combine(board)
    move_without_combine(board)
    return score

def board_view(board, direction):
    if direction == Direction.LEFT:
        return board
    elif direction == Direction.RIGHT:
        return np.fliplr(board)
    elif direction == Direction.UP:
        return board.T
    elif direction == Direction.DOWN:
        return np.fliplr(board.T)


def check_termination(board):
    if np.sum(np.isnan(board)) != 0:
        return False

    for direction in Direction:
        oriented_board = board_view(board, direction)
        next_true, _ = find_combine_tiles(oriented_board)
        if np.any(next_true):
            return False
    return True

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Board:
    def __init__(self, board_size=4, fract_4=0.2):
        self.board_shape = (board_size, board_size)
        self.squares = np.full(self.board_shape, np.nan)
        self.fract_4 = fract_4
        self.score = 0
        for i in range(NUM_STARTING_SQUARES):
            self.gen_new_tile(self.squares, copy=False)

    def __str__(self):
        return str(self.squares)

    def gen_new_tile(self, board, copy=False):
        if copy:
            board = np.array(board)
        new_tile_val = self._new_tile_value()
        blank_tiles = np.isnan(board)
        num_blank = np.sum(blank_tiles)
        blank_index = np.random.choice(num_blank)
        board_index = np.flatnonzero(blank_tiles)[blank_index]
        board.flat[board_index] = new_tile_val
        return board

    def _new_tile_value(self):
        if np.random.random() < self.fract_4:
            return 4
        else:
            return 2

    def move(self, direction, new_tile=True, copy=False):
        board = np.array(self.squares)

        oriented_board = board_view(board, direction)
        move_score = move_left(oriented_board)

        # Nans comparison is always false, so also check if both squares are nan
        board_changed = ~np.all((board == self.squares) | (
            np.isnan(board) & np.isnan(self.squares)))
        print(board != self.squares)
        print(board_changed)
        if new_tile and board_changed:
            self.gen_new_tile(board)

        if not copy:
            self.squares[:] = board
            self.score += move_score

        return board, move_score


if __name__ == '__main__':
    board = Board(board_size=2)
    print(board)
    playing = True
    while playing:
        valid_input = False
        valid_inputs = ['u', 'd', 'l', 'r', 'h', 'q']
        input_map = {'u': Direction.UP, 'd': Direction.DOWN,
                     'l': Direction.LEFT, 'r': Direction.RIGHT}
        while not valid_input:
            user_input = input('Enter move (h for help):\t')
            user_input = user_input.lower()[0]
            valid_input = user_input in valid_inputs
        if user_input == 'h':
            print('u: move up\nd: move down\nl: move left\nr: move right\n'
                  'h: help\nq: quit')
            continue
        elif user_input == 'q':
            print('Quiting')
            break
        else:
            direction = input_map[user_input]
        _, move_score = board.move(direction)
        print('Move Score: ', move_score)
        print('Total Score: ', board.score)
        print(board)
        if check_termination(board.squares):
            print('Game Over!!')
            break
