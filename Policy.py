import copy
from random import random, choice
import numpy as np

import Board2048
from Board2048 import Move

# TODO: better define the interface with the policy
# Policy should take in a state and give out an action
# The programming of it currently is very functional
# Net and board should be built into the policy

def epGreedyPolicy(board, net, ep):
    """
    Given a board and a neural net, returns a move based on an ep greedy
    policy. Returns move with highest predicted value 1-ep of the time
    Otherwise, ep of the time, the policy explores and randomly picks
    one of the suboptimal values
    """
    moves = ['up','down','right','left']
    validMoves = []
    for move in moves:
        if board.checkValidMove(move):
            validMoves.append(move)

    #find the values of all after states to determine best
    maxAfterValue = float('-inf')
    for move in validMoves:
        boardCopy = Board2048.move(board, move, afterState=True)
        afterValue = net.forward(boardCopy)
        if afterValue>maxAfterValue:
            maxAfterValue = afterValue
            bestMove = move

    r = random()
    if r>ep: # 1-ep probability of best move
        return bestMove
    else:
        # If there's only one move then pick still pick the best. There
        # should always be at least one valid move or else game would be over
        if len(validMoves) == 0:
            raise ValueError('No valid moves. Policy cannot determine action.')
        if len(validMoves)==1:
            return bestMove
        else:
            validMoves.pop(validMoves.index(bestMove))  # remove best move
            return choice(validMoves)                   # even chance of the rest


class Policy:
    def __init__(self):
        raise NotImplementedError

    def get_action(self, board):
        raise NotImplementedError


class RandomPolicy(Policy):
    def __init__(self):
        pass

    def get_action(self, board):
        valid_moves = board.get_valid_moves()
        return np.random.choice(valid_moves)

class EpGreedyPolicy(Policy):
    def __init__(self, model, epsilon=0.75):
        self.model = model
        self.epsilon = epsilon

    def get_action(self, board):
        valid_moves = board.get_valid_moves()

        # FIXME!! Write new things here.
        #find the values of all after states to determine best
        maxAfterValue = float('-inf')
        for move in validMoves:
            boardCopy = Board2048.move(board, move, afterState=True)
            afterValue = net.forward(boardCopy)
            if afterValue>maxAfterValue:
                maxAfterValue = afterValue
                bestMove = move
