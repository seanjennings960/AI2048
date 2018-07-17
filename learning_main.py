from Board2048 import Board2048
from deprecated.NeuralNet import NeuralNet,netParams
from policies import epGreedyPolicy as policy

board = Board2048()
net = NeuralNet(netParams)
numEpisodes = 100





for epNum in numEpisodes:
    for theta in net.thetas:
        z = np.zeros(theta.shape)
    board.reset()
    while not board.gameOver():
        
