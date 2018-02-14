from Tkinter import *
import ttk
from Board2048 import *


TILE_COLORS = {
    0:    '#999999',
    2:    '#f2f2f2',
    4:    '#cccccc',
    8:    '#ff9900',
    16:   '#ff6600',
    32:   '#ff3300',
    64:   '#ff0000',
    128:  '#ffff99',
    256:  '#ffff66',
    512:  '#ffff33',
    1024: '#ffff1a',
    2048: '#ffff00',
}


class Gui2048:
    """
    Class that contains the GUI of a 2048 board
    """

    def __init__(self):

        self.root = Tk()
        self.root.title('2048!!!')
        self.root.rowconfigure(0,weight=1)
        self.root.columnconfigure(0,weight=1)


        # Init frames. Game frame and display frame are children of the main
        # frame.
        self.mainFrame = ttk.Frame(self.root, padding=12,
                            relief = 'sunken', borderwidth=5)
        self.mainFrame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.gameFrame = ttk.Frame(self.mainFrame, padding=12,
                                   relief = 'sunken')
        self.gameFrame.grid(column=0, row=0, sticky=(N,W,E,S))
        self.displayFrame = ttk.Frame(self.mainFrame, padding=12,
                                      relief = 'sunken')
        self.displayFrame.grid(column=1, row=0, sticky=(N, W, E, S))
        self.mainFrame.columnconfigure(1, weight=1)

        self.board = Board2048()

        # Initialize GUI elements
        self._set_scaling()
        self._init_style()
        self._init_gui_board()
        self._init_frame_array()
        self._init_display_frame()

        self._update_gui()

    def _init_style(self):
        """Initialize style that contains all color info for all
        values of squares"""
        self.square_style = ttk.Style()
        for squareVal in TILE_COLORS:
            frame_style_name = str(squareVal) + '.TFrame'
            label_style_name = str(squareVal) + '.TLabel'
            self.square_style.configure(frame_style_name,
                                background=TILE_COLORS[squareVal])
            self.square_style.configure(label_style_name,
                                background=TILE_COLORS[squareVal])

    def _init_gui_board(self):
        """
        Initializes the array which hold the string variables used by the GUI
        """
        self.gui_board = []
        for i in range(4):
            self.gui_board.append([])
            for j in range(4):
                self.gui_board[i].append(StringVar())

        self.score_var = StringVar()

    def _init_frame_array(self):
        """Initialize the squares of the game frame"""
        self.squareFrameArray = []
        for i in range(4):
            self.squareFrameArray.append([])
            for j in range(4):
                if self.board.isTileEmpty(i,j):
                    r = 'sunken'
                else:
                    r = 'raised'
                val = self.board.getTile(i,j)
                # Create frame for each square
                squareFrame = ttk.Frame(self.gameFrame, relief=r,
                                        padding=15, style=str(val)+'.TFrame')
                # Place frame in the grid
                squareFrame.grid(row=i, column=j, padx=5, pady=5,
                                      sticky=(N,W,E,S))
                # Make inside label scale with the window
                squareFrame.rowconfigure(0, weight=1)
                squareFrame.columnconfigure(0, weight=1)
                # Add it to array so it can be referenced later
                self.squareFrameArray[i].append(squareFrame)
                # Add label with the text and place in square frame
                label = ttk.Label(squareFrame, textvariable=self.gui_board[i][j],
                                  width=6, style=str(val)+'.TLabel')
                label.grid(column=0,row=0)

    def _init_display_frame(self):
        """initialize ingame display GUI"""
        scoreLabel = ttk.Label(self.displayFrame, padding=15,
                textvariable = self.score_var, width = 15, anchor=CENTER)
        scoreLabel.grid(column=0,row=0)
        self._game_over_label = ttk.Label(self.displayFrame, text='Game Over')
        self._game_over_label.grid(column=0,row=1)
        self._game_over_label.grid_remove()
        self._new_game_label = ttk.Button(self.displayFrame, text='New Game?',
                                         command=self.reset_board)
        self._new_game_label.grid(column=0,row=2)
        self._new_game_label.grid_remove()


    def run(self):
        self._bind_controls()
        self.root.mainloop()

    def reset_board(self, *args):
        self.board = Board2048()
        self._update_gui()
        self._game_over_label.grid_remove()
        self._new_game_label.grid_remove()

    def moveUp(self, *args):
        self.board.move('up')
        self._update_gui()

    def moveDown(self, *args):
        self.board.move('down')
        self._update_gui()

    def moveRight(self, *args):
        self.board.move('right')
        self._update_gui()

    def moveLeft(self, *args):
        self.board.move('left')
        self._update_gui()

    def _update_gui(self):
        self._set_tile_values()
        self._update_relief()
        self._update_style()
        self.score_var.set('Score: '+str(self.board.score))
        if self.board.gameOver():
            self._game_over_label.grid()
            self._new_game_label.grid()

    def _set_tile_values(self):
        """Sets the string var of the gui_board to be the same as
        the board"""
        for i in range(4):
            for j in range(4):
                val = self.board.getTile(i,j)
                if val == 0:
                    labelText = ''.center(10)
                else:
                    labelText = str(val).center(10)
                self.gui_board[i][j].set(labelText)

    def _update_relief(self):
        """Sets the relief of the frames based on tile value"""
        for i in range(4):
            for j in range(4):
                if self.board.isTileEmpty(i,j):
                    r = 'sunken'
                else:
                    r = 'raised'
                self.squareFrameArray[i][j].configure(relief=r)


    def _update_style(self):
        for i in range(4):
            for j in range(4):
                val = self.board.getTile(i,j)
                squareFrame = self.squareFrameArray[i][j]
                squareLabel = squareFrame.winfo_children()[0]
                squareFrame.configure(style=str(val)+'.TFrame')
                squareLabel.configure(style=str(val)+'.TLabel')


    def _set_scaling(self):
        """Sets the weight of all columns and rows of the game frame
        so that board scales with window resizing."""
        for i in range(4):
            self.gameFrame.columnconfigure(i, weight=1, pad=3)
            self.gameFrame.rowconfigure(i, weight=1)

    def _bind_controls(self):
        """Binds the arrow keys to GUI move functions"""
        self.root.bind('<Up>', self.moveUp)
        self.root.bind('<Right>', self.moveRight)
        self.root.bind('<Left>', self.moveLeft)
        self.root.bind('<Down>', self.moveDown)


if __name__=='__main__':
    gui = Gui2048()
    gui.run()
