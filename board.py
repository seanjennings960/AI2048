import numpy as np
from enum import Enum
import time
from minimal_board import move_left_minimal

NUM_STARTING_SQUARES = 2

def move_without_combine(board):
    ts = []
    ts.append(time.time())
    tiles_per_row = np.sum(~np.isnan(board), axis=-1)
    # print('tiles_per_row', tiles_per_row)
    ts.append(time.time())
    new_indices_flat = np.zeros(np.sum(tiles_per_row), dtype=int)
    # Keeps track of which index in new_indices_flat we are at.
    j = 0
    for i in range(board.shape[0]):
        row_start = i * board.shape[-1]
        next_j = j + tiles_per_row[i]
        new_indices_flat[j:next_j] = np.arange(tiles_per_row[i]) + row_start
        j = next_j
    # print('new_indices_flat', new_indices_flat)
    ts.append(time.time())

    board_temp = np.full(board.shape, np.nan)
    # print('Previous board values: ', board_out.flat[new_indices_flat])
    board_temp.flat[new_indices_flat] = board[~np.isnan(board)]
    board[:] = board_temp
    ts.append(time.time())
    return ts

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
    ts = []
    ts.append(time.time())
    next_true, is_next = find_combine_tiles(board)
    ts.append(time.time())
    board[next_true] *= 2
    ts.append(time.time())
    board[is_next] = np.nan
    ts.append(time.time())
    return np.sum(board[next_true]), ts


def move_left(board):
    ts = []
    ts.append(time.time())
    ts1 = move_without_combine(board)
    ts.append(time.time())
    score, ts2 = combine(board)
    ts.append(time.time())
    ts3 = move_without_combine(board)
    ts.append(time.time())
    # print_ts(ts, 'Move time')
    # print_ts(ts1, '1st mwc')
    # print_ts(ts2, 'combine')
    # print_ts(ts3, '2nd mwc')

    return score

def print_ts(ts, name):
    print('{}: '.format(name), (1000*np.diff(ts)).round(3))
    print('Total: ', 1000*(ts[-1] - ts[0]))

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

def gen_new_tile(board, fract_4):
    def _new_tile_value(fract_4):
        if np.random.random() < fract_4:
            return 4
        else:
            return 2

    new_tile_val = _new_tile_value(fract_4)
    blank_tiles = np.isnan(board)
    num_blank = np.sum(blank_tiles)
    blank_index = np.random.choice(num_blank)
    board_index = np.flatnonzero(blank_tiles)[blank_index]
    board.flat[board_index] = new_tile_val


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

LOW_LEVEL_MAP = {
    'vector': move_left,
    'minimal': move_left_minimal,
}

class Board:
    def __init__(self, board_size=4, fract_4=0.2, low_level='vector'):
        self.board_shape = (board_size, board_size)
        self.squares = np.full(self.board_shape, np.nan)
        self.fract_4 = fract_4
        self.score = 0
        self.move_left = LOW_LEVEL_MAP[low_level]
        for i in range(NUM_STARTING_SQUARES):
            self.gen_new_tile(copy=False)

    def __str__(self):
        return str(self.squares)

    def gen_new_tile(self, copy=False):
        if copy:
            board = np.array(self.squares)
        else:
            board = self.squares
        gen_new_tile(board, self.fract_4)
        return board


    def move(self, direction, new_tile=True, copy=False):
        board = np.array(self.squares)

        oriented_board = board_view(board, direction)
        move_score = self.move_left(oriented_board)

        # Nans comparison is always false, so also check if both squares are nan
        board_changed = ~np.all((board == self.squares) | (
            np.isnan(board) & np.isnan(self.squares)))
        if new_tile and board_changed:
            gen_new_tile(board, self.fract_4)

        if not copy:
            self.squares[:] = board
            self.score += move_score

        return board, move_score, board_changed

    def game_over(self):
        return check_termination(self.squares)

if __name__ == '__main__':
    board = Board(board_size=4)
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
        _, move_score, _ = board.move(direction)
        print('Move Score: ', move_score)
        print('Total Score: ', board.score)
        print(board)
        if check_termination(board.squares):
            print('Game Over!!')
            break
