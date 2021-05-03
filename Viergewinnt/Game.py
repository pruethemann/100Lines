import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import random
import matplotlib.pyplot as plt
import seaborn  as sns
import sys

class Viergewinnt:
    def __init__(self):
        pass

    def start_game(self,nrows=6, ncols=9, inarow=4):
        """
        Creates a new game instance
        """
        self.config = {'nrows':nrows,
                       'ncols':ncols}

        self.nrows = nrows
        self.ncols = ncols
        self.inarow = inarow

        self.board = np.zeros((nrows,ncols), dtype=np.uint8)
        self.player = 1
        self.last_col = 0
        self.move_count = 0


    def gameplay(self, strategy) -> int:
        # load player strategy

        while True:
            # move of player
            self.move(strategy=strategy[self.player-1])

            # Check win
            if self.check_win():
                return self.player

            if self.move_count == self.ncols * self.nrows:
                print('Unentschieden')
                return -1

            # change player
            if self.player == 1:
                self.player = 2
            else:
                self.player = 1

        #print(f'Player {self.player} won')
        #self.print_board()


    def competition(self, n=1000, strategy=None):

        win_1 = 0
        pat = 0
        for i in range(n):
            self.start_game()
            win = self.gameplay(strategy)
            if win == 1:
                win_1 += 1

            elif win == -1:
                pat += 1

            if n<=10:
                self.print_board()

        # Yield
        player_1 = win_1/n
        player_2 = (n - win_1 - pat) / n

        print(f'Strategy {strategy[0]} : {player_1} {win_1}')
        print(f'Strategy {strategy[1]} : {player_2} {n - win_1 - pat}')
        print(f'Strategy {strategy[1]} : {pat / n} {pat}')

    def move(self,strategy='random'):
        if strategy == 'random':
            self.str_random()
        elif strategy == 'left':
            self.str_left()

        elif strategy == 'manual':
            self.str_manual()

        elif strategy == 'mimic':
            self.str_mimic()

        elif strategy == 'mimic_next':
            self.str_mimic_next()

        elif strategy == 'middle':
            self.str_middle()

        else:
            self.str_random()

    def str_random(self):
        """
        Random strategy
        """

        # get all columns with at least one empty slot
        cols = [c for c in range(self.ncols) if self.check_drop(c)]

        x = random.choice(cols)
        self.drop(self.board, x, self.player)

    def str_left(self):
        """
        Place as left as possible
        """
        # get all columns with at least one empty slot
        cols = [c for c in range(self.ncols) if self.check_drop(c)]

        x = cols[0]
        self.drop(x, self.player)

    def str_middle(self):
        """
        Place in middle
        """
        # get all columns with at least one empty slot
        if not self.drop(self.board, self.ncols // 2, self.player):
            self.str_random()

    def check_drop(self,col):
        for row in range(self.nrows-1,-1,-1):
            if self.board[row,col] == 0:
                return True
        return False

    def print_board(self):
        print(self.board)

    def drop(self, board, col, player):
        if col < 0 or col >= self.ncols:
            return False

        for row in range(self.nrows-1,-1,-1):
            if board[row,col] == 0:
                board[row, col] = player
                self.last_row = row
                self.last_col = col
                self.move_count += 1
                return True

        #print(f'Col {col} is full')
        return False

    def heuristic_score(self, col, window_size, player):
        board = self.board.copy()
        self.drop(board, col, player)

        # horicontal
        for row in range(self.nrows):
            for col in range(0, self.ncols - self.inarow):
                window = board[row, col:col + self.inarow]
                print(window.sum())

        # vertical
        for col in range(self.ncols):
            for row in range(0, self.nrows - self.inarow):
                window = board[row, col:col + self.inarow]
                print(window.sum())

    def testing(self):
        self.start_game()
        self.drop(self.board,1,1)
        self.drop(self.board, 3, 1)
        self.drop(self.board, 4, 1)
        self.print_board()
        self.heuristic_score(4)


    def check_win(self):
        # vertical
        for col in range(self.ncols):
            streak_1 = 0
            streak_2 = 0
            for row in range(self.nrows):
                if self.board[row, col] == 1:
                    streak_1 += 1
                    streak_2 = 0

                elif self.board[row, col] == 2:
                    streak_2 += 1
                    streak_1 = 0

                else:
                    streak_1 = 0
                    streak_2 = 0

               # if streak_1 > 3 or streak_2 > 3:
                #    print('vertical')
                 #   print(streak_1, streak_2, row, col)

                if streak_1 == 4 or streak_2 == 4:
                    #print("vertcial", row, col)
                    return True

        # horicontal

        for row in range(self.nrows):
            streak_1 = 0
            streak_2 = 0
            for col in range(self.ncols):
                if self.board[row, col] == 1:
                    streak_1 += 1
                    streak_2 = 0
                elif self.board[row, col] == 2:
                    streak_2 += 1
                    streak_1 = 0
                else:
                    streak_1 = 0
                    streak_2 = 0

                if streak_1 == 4 or streak_2 == 4:
                    #print("horicontal", row, col)
                    return True

        # diagonal right

        for col in range(self.ncols - 3):
            for row in range(self.nrows - 3):
                if self.board[row,col] == 1 and self.board[row+1,col+1] == 1 and self.board[row+2,col+2] == 1 and self.board[row+3,col+3] == 1:
                    #print("vertical right", row, col)
                    return True
                if self.board[row,col] == 2 and self.board[row+1,col+1] == 2 and self.board[row+2,col+2] == 2 and self.board[row+3,col+3] == 2:
                    return True

        # diagonal left

        for col in range(3,self.ncols):
            for row in range(self.nrows - 3):
                if self.board[row,col] == 1 and self.board[row+1,col-1] == 1 and self.board[row+2,col-2] == 1 and self.board[row+3,col-3] == 1:
                    #print("vertical left", row, col)
                    return True
                if self.board[row,col] == 2 and self.board[row+1,col-1] == 2 and self.board[row+2,col-2] == 2 and self.board[row+3,col-3] == 2:
                    return True

        return False

    def str_mimic(self):
        if not self.drop(self.board, self.last_col, self.player):
            self.str_random()

    def str_mimic_next(self):
        if not self.drop(self.board, self.last_col + 1, self.player):
            self.str_random()

    def str_manual(self):
        self.print_board()
        x = input('Welche column? ')
        self.drop(self.board, int(x)-1, self.player)
        self.print_board()


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

