from random import choice
from random import random
import copy

# Probability that a new tile that is generated is a 2 (instead of 4)
PROB_2 = 0.8

class Board2048:
    def __init__(self):
        self.tiles = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0]]
        self.combined = [[False, False, False, False],
                         [False, False, False, False],
                         [False, False, False, False],
                         [False, False, False, False]]
        # Whether each tile has combined with another tile on the current move
        self.genNewTile()
        self.genNewTile()
        self.score = 0

    def __getitem__(self,pos):
        i,j=pos
        return self.getTile(i,j)

    def genNewTile(self):
        """
        Generates new tile (either 2 or 4) in empty tile (val=0) returns True
        if there are no empty tiles, returns False
        """
        # Find which tiles are empty
        emptyList = []
        for i in range(4):
            for j in range(4):
                tileKey = 4*i + j
                if self.isTileEmpty(i, j):
                    emptyList.append(tileKey)

        # If there's no empty tiles, return false
        if len(emptyList) == 0:
            return False

        # Choose tile from empty tiles and fill in 2 or 4.
        newTileKey = choice(emptyList)
        iNew = newTileKey//4
        jNew = newTileKey%4
        if random() > PROB_2:
            self.tiles[iNew][jNew] = 4
        else:
            self.tiles[iNew][jNew] = 2
        return True

    def resetCombined(self):
        for i in range(4):
            for j in range(4):
                self.combined[i][j] = False

    def getCombined(self, i, j):
        return self.combined[i][j]

    def setCombined(self, i, j):
        self.combined[i][j] = True

    def emptyTile(self, i, j):
        self.tiles[i][j]=0

    def setTile(self, i, j, val):
        self.tiles[i][j] = val

    def getTile(self, i, j):
        val = self.tiles[i][j]
        return val

    def isTileEmpty(self, i, j):
        return self.tiles[i][j]==0

    def slideTile(self, i, j, direct):
        """
        Slides tile[i,j] in given direction until it hits another tile or the wall
        if it hits another tile theat's the same, they combine.
        """
        tile = self.getTile(i,j)
        if direct=='up':                        # if the direction is up
            iRange = list(range(i - 1, -1, -1))     # list the squares above i,j
            jRange = [j]*len(iRange)            # in iRange,jRange
        elif direct=='down':
            iRange = list(range(i + 1, 4))
            jRange = [j]*len(iRange)
        elif direct=='left':
            jRange = list(range(j - 1, -1, -1))
            iRange = [i]*len(jRange)
        else:
            jRange = list(range(j + 1, 4))
            iRange = [i]*len(jRange)

        # For each tile in the range above, below, to the left or right
        for k in range(len(iRange)):
            nextTile = self.getTile(iRange[k], jRange[k])
            nextTileCombined = self.getCombined(iRange[k], jRange[k])
            # If the next tile isn't empty
            if nextTile != 0:
                # And it's the same as the original tile and the next tile
                # hasn't already been combined
                if nextTile == tile and not nextTileCombined:
                    totalVal = tile*2
                    # Combine the tiles in the place of the hit tile, set
                    # combined, and empty original tile.
                    self.setTile(iRange[k],jRange[k],totalVal)
                    self.setCombined(iRange[k],jRange[k])
                    self.emptyTile(i,j)
                    return totalVal
                # If the tiles are different and it's the first tile
                elif k == 0:
                    return 0 # Do nothing
                # Of they are different and it's after the first tile
                else:
                    # Move tile to place before next tile
                    self.emptyTile(i,j)
                    # Set the space before the nonempty tile to the current
                    self.setTile(iRange[k - 1],jRange[k - 1],tile)
                return 0
            # If it has gone through all squares and they were all empty
            elif k == len(iRange) - 1:
                self.setTile(iRange[k],jRange[k],tile)
                self.emptyTile(i,j)
                return 0

    # def print(self):
    #     for line in self.tiles:
    #         for square in line:
    #             print(square,end='   ')
    #         print()

    def moveUp(self):
        self.resetCombined()
        reward = 0
        # Iterate through tiles
        for j in range(4):
            for i in range(1,4):
                # For each of the bottom three grid spaces
                # see if there are tiles to be moved
                # j=0 doesn't need to be moved regardless of if there is a tile
                if not self.isTileEmpty(i,j):
                    rewardPart = self.slideTile(i,j,'up')
                    reward += rewardPart
        return reward

    def moveDown(self):
        self.resetCombined()
        reward = 0
        for j in range(4):
            for i in range(2,-1,-1):
                # For each of the top three spaces in each column
                # Must start at the second to bottom and go up
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
        """
        Input the move as a string ('up','down','left','right')
        Returns true if move results in different position than the start position
        """
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


    def move(self, direct, afterState=False):
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
                return False # If there is a valid move, it is not game over
        return True # If there are no valid moves, game over is True
        
def move(board, direct, afterState=False):
    boardCopy = copy.deepcopy(board)
    boardCopy.move(direct, afterState)
    return boardCopy


   # def up(self):
   #     if self.checkValidMove('up'):
   #         self.
   #         self.genNewTile()

   # def down(self):
   #     if self.checkValidMove('down'):
   #         self.genNewTile()

   # def right(self):
   #     if self.checkValidMove('right'):
   #         self.genNewTile()

   # def left(self):
   #     if self.checkValidMove('left'):
   #         self.genNewTile()


