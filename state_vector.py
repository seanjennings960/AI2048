"""File for conversions between the board and state vector"""
import numpy as np

def remove_board_zeros(boards):
    boards[boards==0] = 1
    return boards


def log_state_vector(boards, cutoff_values):
    """
    Returns a state vector array for an array of boards based on log function.

    k, nodes per square, is equal to the number of cutoff_values minus 1.
    Each state vector has shape, dim_state_vector = k * dim_square ** 2
    so the total returned state_vectors array has shape:
    (boards.shape, state_vector.shape)
    """
    remove_board_zeros(boards)
    dim_state_vector = len(cutoff_values) - 1
    output_size = boards.shape + (dim_state_vector,)

    log_cutoff_values = np.log2(cutoff_values)

    cutoff_lower_limit = np.full(output_size, log_cutoff_values[:-1])
    cutoff_upper_limit = np.full(output_size, log_cutoff_values[1:])
    cutoff_log_diff = np.full(output_size, np.diff(log_cutoff_values))

    state_vectors = np.zeros(output_size)

    tiles = np.full(output_size, np.log2(boards)[..., np.newaxis])

    state_vectors[tiles <= cutoff_lower_limit] = 0
    state_vectors[tiles >= cutoff_upper_limit] = 1
    between_limits = np.logical_and(tiles > cutoff_lower_limit,
                                    tiles < cutoff_upper_limit)
    state_vectors[between_limits] = (tiles[between_limits] - 
        cutoff_lower_limit[between_limits]) / cutoff_log_diff[between_limits]

    return state_vectors


if __name__ == '__main__':
    boards_shape = (3, 2)
    board_shape = (4, 4)
    cutoff_values = [1, 8, 128, 512, 2048]
    boards = np.exp2(np.arange(np.prod(board_shape))).reshape(board_shape)
    boards_array = np.full(boards.shape + board_shape, boards)

    print(boards.round())
    print(boards_array.shape)
    print(log_state_vector(boards_array, cutoff_values)[..., 3, 0, 3])
