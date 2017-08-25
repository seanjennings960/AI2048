from random import choice
from random import random
import copy


class Board2048:
    def __init__(self):
        self.tiles = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.combined = [[False,False,False,False],[False,False,False,False],[False,False,False,False],[False,False,False,False]]
        #whether each tile has combined with another tile on the current move
        self.genNewTile()
        self.genNewTile()
        self.score = 0

    def __getitem__(self,pos):
        i,j=pos
        return self.getTile(i,j)

    def genNewTile(self):
        # generates new tile (either 2 or 4) in empty tile (val=0) returns True
        # if there are no empty tiles, returns False
        emptyList = []
        for i in range(4):
            for j in range(4):
                tileKey = 4*i+j
                if self.isTileEmpty(i,j):
                    emptyList.append(tileKey)
        if len(emptyList)==0:
            return False
        newTileKey = choice(emptyList)
        iNew = newTileKey//4
        jNew = newTileKey%4
        if random()>0.8:
            self.tiles[iNew][jNew]=4
        else:
            self.tiles[iNew][jNew]=2
        return True

    def resetCombined(self):
        for i in range(4):
            for j in range(4):
                self.combined[i][j] = False

    def getCombined(self,i,j):
        return self.combined[i][j]

    def setCombined(self,i,j):
        self.combined[i][j] = True

    def emptyTile(self,i,j):
        self.tiles[i][j]=0

    def setTile(self,i,j,val):
        self.tiles[i][j] = val

    def getTile(self,i,j):
        val = self.tiles[i][j]
        return val

    def isTileEmpty(self,i,j):
        return self.tiles[i][j]==0

    def slideTile(self,i,j,direct):
        #slides tile[i,j] in given direction until it hits another tile or the wall
        #if it hits another tile that's the same, they combine
        tile = self.getTile(i,j)
        if direct=='up':                        # if the direction is up
            iRange = list(range(i-1,-1,-1))     # list the squares above i,j
            jRange = [j]*len(iRange)            # in iRange,jRange
        elif direct=='down':                    
            iRange = list(range(i+1,4))
            jRange = [j]*len(iRange)
        elif direct=='left':
            jRange = list(range(j-1,-1,-1))
            iRange = [i]*len(jRange)
        else:
            jRange = list(range(j+1,4))
            iRange = [i]*len(jRange)

        for k in range(len(iRange)):   # for each tile in the range above, below, to the left or right    
            nextTile = self.getTile(iRange[k],jRange[k])
            nextTileCombined = self.getCombined(iRange[k],jRange[k])
            if nextTile!=0:    #if the next tile isn't empty
                if nextTile==tile and not nextTileCombined:      #and it's the same as the original tile and the next tile hasn't already been combined
                    totalVal = tile*2
                    self.setTile(iRange[k],jRange[k],totalVal)  #combine the tiles in the place of the hit tile
                    self.setCombined(iRange[k],jRange[k])       #mark that next Tile has combined
                    self.emptyTile(i,j)                #and empty the original
                    return totalVal
                elif k==0:              #if the tiles are different and it's the first tile
                    return 0             #do nothing
                else:                   #if they are different and it's after the first tile to check
                    #move tile to place before next
                    self.emptyTile(i,j)
                    self.setTile(iRange[k-1],jRange[k-1],tile)  #set the space before the nonempty tile to the current
                return 0
            elif k==len(iRange)-1:        #if it has gone through all squares and they were all empty
                self.setTile(iRange[k],jRange[k],tile)
                self.emptyTile(i,j)
                return 0

    def print(self):
        for line in self.tiles:
            for square in line:
                print(square,end='   ')
            print()

    def moveUp(self):
        self.resetCombined()
        reward = 0
        for j in range(4):
            #for each column
            for i in range(1,4):
                #for each of the bottom three grid spaces
                # see if there are tiles to be moved
                #j=0 doesn't need to be moved regardless of if there is a tile
                if not self.isTileEmpty(i,j):         #if the original tile is not empty
                    rewardPart = self.slideTile(i,j,'up')
                    reward += rewardPart
        return reward

    def moveDown(self):
        self.resetCombined()
        reward = 0
        for j in range(4):
            for i in range(2,-1,-1):
                #for each of the top three spaces in each column
                #must start at the second to bottom and go up
                if not self.isTileEmpty(i,j):
                    rewardPart = self.slideTile(i,j,'down')
                    reward += rewardPart
        return reward


    def moveRight(self):
        self.resetCombined()
        reward = 0
        for i in range(4):
            for j in range(2,-1,-1):
                if not self.isTileEmpty(i,j):
                    rewardPart = self.slideTile(i,j,'right')
                    reward += rewardPart
        return reward

    
    def moveLeft(self):
        self.resetCombined()
        reward = 0
        for i in range(4):
            for j in range(1,4):
                if not self.isTileEmpty(i,j):
                    rewardPart = self.slideTile(i,j,'left')
                    reward += rewardPart
        return reward

    def checkValidMove(self,move):
        #input the move as a string ('up','down','left','right')
        #returns true if move results in different position than the start position
        #also completes the move
        boardCopy = copy.deepcopy(self)
        tilesChange = False
        if move == 'up':
            boardCopy.moveUp()
        elif move == 'down':
            boardCopy.moveDown()
        elif move == 'left':
            boardCopy.moveLeft()
        elif move == 'right':
            boardCopy.moveRight()
        else:
            raise ValueError('Invalid Move was input')
        
        for i in range(4):
            for j in range(4):
                if boardCopy.getTile(i,j) != self.getTile(i,j):
                    tilesChange = True
        del(boardCopy)
        return tilesChange


    def move(self,direct,afterState=False):
        if self.checkValidMove(direct):
            if direct == 'up':
                reward = self.moveUp()
            elif direct == 'down':
                reward = self.moveDown()
            elif direct == 'right':
                reward = self.moveRight()
            else:
                reward = self.moveLeft()
            self.score += reward
            if not afterState:
                self.genNewTile()
        return reward

    def gameOver(self):
        moves = ['up','down','left','right']
        for move in moves:
            if self.checkValidMove(move):
                return False #if there is a valid move, it is not game over
        return True #if there are no valid moves, game over is True
        
def move(board,direct,afterState=False):
    boardCopy = copy.deepcopy(board)
    boardCopy.move(direct,afterState)
    return boardCopy


##    def up(self):
##        if self.checkValidMove('up'):
##            self.
##            self.genNewTile()
##
##    def down(self):
##        if self.checkValidMove('down'):
##            self.genNewTile()
##
##    def right(self):
##        if self.checkValidMove('right'):
##            self.genNewTile()
##
##    def left(self):
##        if self.checkValidMove('left'):
##            self.genNewTile()


