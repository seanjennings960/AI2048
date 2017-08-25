from tkinter import *
from tkinter import ttk
from Board2048 import *



root = Tk()
root.title('2048!!!')
root.rowconfigure(0,weight=1)
root.columnconfigure(0,weight=1)


#init main,game and display frames
mainFrame = ttk.Frame(root, padding=12,relief = 'sunken',borderwidth=5)
mainFrame.grid(column=0, row=0, sticky=(N,W,E,S))
gameFrame = ttk.Frame(mainFrame,padding=12,relief = 'sunken')
gameFrame.grid(column=0,row=0,sticky=(N,W,E,S))
displayFrame = ttk.Frame(mainFrame,padding=12,relief = 'sunken')
displayFrame.grid(column=1,row=0,sticky=(N,W,E,S))
mainFrame.columnconfigure(1,weight=1)


tileColors = {}
tileColors[0] = '#999999'
tileColors[2] = '#f2f2f2'
tileColors[4] = '#cccccc'
tileColors[8] = '#ff9900'
tileColors[16] = '#ff6600'
tileColors[32] = '#ff3300'
tileColors[64] = '#ff0000'
tileColors[128] = '#ffff99'
tileColors[256] = '#ffff66'
tileColors[512] = '#ffff33'
tileColors[1024] = '#ffff1a'
tileColors[2048] = '#ffff00'

#initialize style that contains all color info for all values of squares
s = ttk.Style()
for i in range(12):
    if i == 0:
        val = 0
    else:
        val = 2**i
    styleName = str(val)
    s.configure(styleName+'.TFrame',background=tileColors[val])
    s.configure(styleName+'.TLabel',background=tileColors[val])
    
A = Board2048()


def setTileValues(board):
    for i in range(4):
        for j in range(4):
            val = board.getTile(i,j)
            if val == 0:
                labelText = ''.center(10)
            else:
                labelText = str(val).center(10)
            B[i][j].set(labelText)

def moveUp(*args):
    A.move('up')
    update(A)

def moveDown(*args):
    A.move('down')
    update(A)
    
def moveRight(*args):
    A.move('right')
    update(A)
    
def moveLeft(*args):
    A.move('left')
    update(A)

def update(board):
    setTileValues(board)
    updateRelief()
    updateStyle()
    scoreVar.set('Score: '+str(board.score))
    if board.gameOver():
        gameOver.grid()
        newGame.grid()
    
def updateRelief():
    for i in range(4):
        for j in range(4):
            if A.isTileEmpty(i,j):
                r = 'sunken'
            else:
                r = 'raised'
            squareFrameArray[i][j].configure(relief=r)


def updateStyle():
    for i in range(4):
        for j in range(4):
            val = A.getTile(i,j)
            squareFrame = squareFrameArray[i][j]
            squareLabel = squareFrame.winfo_children()[0]
            squareFrame.configure(style=str(val)+'.TFrame')
            squareLabel.configure(style=str(val)+'.TLabel')

def resetBoard(*args):
    global A
    A = Board2048()
    update(A)
    gameOver.grid_remove()
    newGame.grid_remove()

def runGUI():
    root.mainloop()


            
B = []          #holds string variables for each square in GUI
for i in range(4):
    B.append([])
    for j in range(4):
        B[i].append(StringVar())

scoreVar = StringVar()



for i in range(4):
    gameFrame.columnconfigure(i,weight=1,pad=3)     #make square in grid scale with window
    gameFrame.rowconfigure(i,weight=1)


#initialize the squares of the game frame
squareFrameArray = []
for i in range(4):
    squareFrameArray.append([])
    for j in range(4):
        if A.isTileEmpty(i,j):
            r = 'sunken'
        else:
            r = 'raised'
        val = A.getTile(i,j)
        squareFrame = ttk.Frame(gameFrame,relief=r,padding=15,style=str(val)+'.TFrame')      #create frame for each square
        squareFrame.grid(row=i,column=j,padx=5,pady=5,sticky=(N,W,E,S)) #place frame in the grid
        squareFrame.rowconfigure(0,weight=1)                            #make inside label scale with the window
        squareFrame.columnconfigure(0,weight=1)
        squareFrameArray[i].append(squareFrame)                         #add it to array so it can be referenced later
        label = ttk.Label(squareFrame,textvariable = B[i][j],width=6,style=str(val)+'.TLabel')   #add label with the text
        label.grid(column=0,row=0)          #place label in frame


#initialize ingame display GUI
scoreLabel = ttk.Label(displayFrame,padding=15,textvariable = scoreVar,width = 15,anchor=CENTER)
scoreLabel.grid(column=0,row=0)
gameOver = ttk.Label(displayFrame,text='Game Over')
gameOver.grid(column=0,row=1)
gameOver.grid_remove()
newGame = ttk.Button(displayFrame,text='New Game?',command=resetBoard)
newGame.grid(column=0,row=2)
newGame.grid_remove()

update(A)

root.bind('<Up>',moveUp)
root.bind('<Right>',moveRight)
root.bind('<Left>',moveLeft)
root.bind('<Down>',moveDown)


if __name__=='__main__':
    runGUI()
