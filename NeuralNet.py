import numpy as np
import copy
import random

netParams = {
    'alpha': 0.01,
    'gamma': 1,
    'lamb': 0.8,
    'hiddenLayers': 1,
    'hiddenLayerSizes': [40],
    'nodesPerSquare': 3,
    'cutoffVals': [1,8,64,2048], #Values up to and including cutoffVal[i+1] are included in node i
                        #len(cutoffVals) = nodesPerSquare+1
    'boardToStateConv': 'log' #type of conversion from board to state
}

def sigmoid(x):
    return 1/(1+np.exp(o-x))


class NeuralNet():
    def __init__(self,netParams):
        self.params = netParams
        self.thetas = list()
        self.a = list() # the activation values of the hidden layers
        self.delta = list()
        
        for i in range(self.params['hiddenLayers']+1): #theta matrices 
            if i == 0:
                size = (self.params['hiddenLayerSizes'][i],16*self.params['nodesPerSquare'])
                self.a.append(np.zeros(self.params['hiddenLayerSizes'][i]))
                self.delta.append(np.zeros(self.params['hiddenLayerSizes'][i]))
            elif i == self.params['hiddenLayers']: #for 
                size = (1,self.params['hiddenLayerSizes'][i-1])
                self.delta.append(0)
            else:
                size = (self.params['hiddenLayerSizes'][i],self.params['hiddenLayerSizes'][i-1])
                self.a.append(np.zeros(self.params['hiddenLayerSizes'][i]))
                self.delta.append(np.zeros(self.params['hiddenLayerSizes'][i]))
            self.thetas.append(np.zeros(size))

        
        

    def forward(self,board):
        #forward propogation to return the value of the current position of the board
        state = self.getStateVector(board)
        self.a[0] = sigmoid(self.thetas[0].dot(state))
        for i in range(self.params['hiddenLayers']-1):
            #TODO: add bias unit
            self.a[i+1] = sigmoid(self.thetas[i+1].dot(self.a[i]))

        return self.thetas[self.params['hiddenLayers']].dot(self.a[self.params['hiddenLayers']-1])

    def getStateVectorLog(self,board):
        state = np.zeros(16*self.params['nodesPerSquare'])
        for i in range(4):
            for j in range(4):
                val = board.getTile(i,j)
                for k in range(self.params['nodesPerSquare']-1):
                    if val<=self.params['cutoffVals'][k]:
                        stateVal = 0
                    elif val<self.params['cutoffVals'][k+1]:
                        stateVal = (np.log(val)-np.log(self.params['cutoffVals'][k]))/np.log(2)
                        lowerLogVal = np.log(self.params['cutoffVals'][k])/np.log(2)
                        upperLogVal = np.log(self.params['cutoffVals'][k+1])/np.log(2)
                        stateVal = stateVal/(upperLogVal-lowerLogVal) #normalize values to range (0,1)
                    else:
                        stateVal = 1
                    state[self.params['nodesPerSquare']*(4*i+j)+k] = stateVal
        return state



    def getStateVector(self,board):
        if self.params['boardToStateConv'] == 'log':
            return self.getStateVectorLog(board)
        else:
            raise ValueError('boardToStateConv is not valid')

    def backward(self,board,estTrueVal):
        #calculates the gradient of the value function in the direction of the minimum error between
        # the approximated neural net value and the true value (estimated by the reward and value of the next state)

        value = self.forward(board)
        self.delta[self.params['hiddenLayers']] = estTrueVal - value # error of output of net
        dThetas = list() #initialize the gradient of the theta
        
        for i in range(self.params['hiddenLayers']-1,-1,-1):
            self.delta[i] = self.thetas[i+1].T.dot(self.delta[i+1])*self.a[i]*(1-self.a[i])


        for i in range(self.params['hiddenLayers']+1):
            if i == 0:
                state = self.getStateVector(board)
                dThetai = np.c_[self.delta[0]].dot(np.atleast_2d(state)) #first dTheta matrix uses state instead of of hidden layer
            else:
                dThetai = np.c_[self.delta[i]].dot(np.atleast_2d(self.a[i-1]))
            dThetas.append(dThetai)
        return dThetas

    
