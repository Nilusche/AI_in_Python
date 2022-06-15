import numpy as np
import pygame

class BacktrackingAlgorithm:
    def __init__(self, game):
        self.game = game
        self.state =game.state
        self.count = 1

    

    def print_solution_toconsole(self, draw):
        print(self.count)
        self.count +=1
        print(self.state)
        
        draw()
        pygame.display.flip()
        pygame.time.wait(120)

    def is_queen_safe(self, r, c):

        for i in range(r):
            if self.state[i][c] == '♛':
                return False

        # diagonal left up to right down
        (i, j) = (r, c)
        while i >= 0 and j >= 0:
            if self.state[i][j] == '♛':
                return False
            i = i - 1
            j = j - 1
 
        # diagonal left bottom to right up
        (i, j) = (r, c)
        while i >= 0 and j < 8:
            if self.state[i][j] == '♛':
                return False
            i = i - 1
            j = j + 1
 

        return True

    def backtracking_algorithm(self,r, draw):
        if r==8:
            self.print_solution_toconsole(draw)
            draw

        for i in range(8):
            if self.is_queen_safe(r,i):
                self.game.actions["add_queen"](r,i)
                self.game.state = self.state

                self.backtracking_algorithm(r+1,draw)

                self.game.actions["remove_queen"](r,i)
                self.game.state = self.state


