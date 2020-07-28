import numpy as np
import tkinter as tk
from PIL import Image, ImageTk



class Viergewinnt:
    def __init__(self, nrows=6, ncols=8):
        """
        Creates a new game instance
        """
        self.config = {'nrows':nrows,
                       'ncols':ncols}

        self.nrows = nrows
        self.ncols = ncols

        self.board = np.zeros((nrows,ncols), dtype=np.uint8)
        """
        print("Start Windows")
        window = tk.Tk()
        greeting = tk.Label(text="Vier gewinnt")
        greeting.pack()
        print("Start Windows")
        window.mainloop()
        """

    def gameplay(self):
        if self.check_win():
            print(f'Player {self.player} won')

        if self.player == 1:
            self.player = 2
        else:
            self.player = 1


    def print_board(self):
        print(self.board)

    def drop(self, col, player):
        for row in range(self.nrows-1,-1,-1):
            if self.board[row,col] == 0:
                self.board[row, col] = player
                return

        print(f'Col {col} is full')

    def check_win(self):
        # horicontal
        streak = 0
        for col in range(self.ncols):
            for row in range(self.nrows):
                if self.board[row,col] in [1,2]:
                    streak += 1
                else:
                    streak = 0

                if streak == 4:
                    return True

        # vertical
        streak = 0
        for row in range(self.nrows):
            for col in range(self.ncols):
                if self.board[row, col] in [1, 2]:
                    streak += 1
                else:
                    streak = 0
                if streak == 4:
                    return True

        return False

    def testing(self):
        self.drop(1, 2)
        self.print_board()
        self.check_win()
        self.drop(1, 2)
        self.print_board()
        self.check_win()
        self.drop(1, 2)
        self.print_board()
        self.check_win()
        self.drop(1, 2)
        self.print_board()
        self.check_win()

        self.drop(0, 1)
        self.print_board()
        self.check_win()
        self.drop(1, 1)
        self.print_board()
        self.check_win()
        self.drop(2, 1)
        self.print_board()
        self.check_win()
        self.drop(3, 1)
        self.print_board()
        self.check_win()

    def paint_board(self):
        self.print_board()
        #img = Image.fromarray(self.board, 'RGB')
        #img = img.resize((1000*self.ncols,1000*self.nrows))

        #img.save('board.png')
        #img.show()
        render = ImageTk.PhotoImage(img)
        label = tk.Label(self, image=render)
        label.image = render
        label.place(x=0,y=0)

