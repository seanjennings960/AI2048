from Board2048 import Board2048
from NeuralNet import NeuralNet,netParams
from Policy import epGreedyPolicy
import numpy as np

board = Board2048()
net = NeuralNet(netParams)

for i in range(len(net.thetas)):
    theta = net.thetas[i]
    shape1,shape2 = theta.shape
    net.thetas[i] = 10*np.random.rand(shape1,shape2)

moves = ['up','down','left','right']
for move in moves:
    boardCopy = board.move(move,retCopy=True,afterState=True)
    print('move: ',move)
    print('value: ',net.forward(boardCopy))


numTrials = 1000
ep = .1
moveCounter = {}
for move in moves:
    moveCounter[move] = 0

for i in range(numTrials):
    move = epGreedyPolicy(board,net,ep)
    moveCounter[move] += 1

print('ep: ',ep)
for move in moveCounter:
    print('move: ',move)
    print('prob: ',moveCounter[move]/numTrials)
    
