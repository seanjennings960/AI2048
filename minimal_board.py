import numpy as np

def move_row(row):
    """pt1 is the target square and pt2 is the square to move"""
    pt1 = 0
    score = 0
    for pt2 in range(1, row.shape[0]):
        # Case 1: pt2 is none. Nothing to do
        if np.isnan(row[pt2]):
            continue
        # Case 2: They are equal. combine and increment pt1
        elif row[pt1] == row[pt2]:
            row[pt1] *= 2
            score += row[pt1]
            row[pt2] = np.nan
            pt1 += 1
        # Case 3: pt1 is none. Move pt2 -> pt1
        elif np.isnan(row[pt1]):
            row[pt1] = row[pt2]
            row[pt2] = np.nan
        # Case 4: They are different and non-null. Move pt2 -> pt1 + 1
        else:
            # Unless it's already there.
            if not pt2 == pt1 + 1:
                row[pt1 + 1] = row[pt2]
                row[pt2] = np.nan
            pt1 += 1
    return score


def move_left_minimal(board):
    score = 0
    for i in range(board.shape[0]):
        score += move_row(board[i, :])
    return score

if __name__ == '__main__':
    row = np.array([2, 2, 2, 8], dtype=float)
    print(row)
    score = move_row(row)
    print(score)
    print(row)

    board = np.array([[2, 4, 8, 2],
                      [2, np.nan, np.nan, 2],
                      [4, 4, 4, 4],
                      [4, np.nan, 4, 2]], dtype=float)
    print(board)
    score = move_left_minimal(board)
    print(score)
    print(board)