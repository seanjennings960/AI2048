from Board2048 import Board2048
from deprecated.NeuralNet import netParams, NeuralNet
import numpy as np

A = Board2048()
A.move('up')
A.move('left')
A.print()
net = NeuralNet(netParams)

#state vector test
stateVector = net.getStateVector(A)
print(net.forward(A))
print(stateVector[0:3])

#backpropagation test
num_iter = 100
alpha = 0.01
value = np.zeros(num_iter)
for i in range(num_iter):
    value[i] = net.forward(A)
    print('Value after iter %d is: %f'%(num_iter,value[i]))
    dThetas = net.backward(A,10)
    for j in range(len(net.thetas)):
        net.thetas[j] += dThetas[j]*alpha


##for i in range(len(dThetas)):
##    print('shape of original thetas: '+str(net.thetas[i].shape))
##    print('shape of new thetas: ' + str(dThetas[i].shape))
##    net.thetas[i] = dThetas[i]

print('net theta values are')
for i in range(net.params['hiddenLayers']+1):
    print('Theta layer %d is:'%i)
    print(net.thetas[i])
