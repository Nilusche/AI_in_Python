import asyncio
from copy import deepcopy
from distutils.ccompiler import gen_lib_options
from tracemalloc import start
from unittest import findTestCases
import numpy as np
from GeneticAlgorithm import *
from BacktrackingAlgorithm import *


class QueensGame():
    def __init__(self, state=None):
        if state is not None:
            self.state = state
        else:
            #initial state
            self.state = np.array([
                ["□", "□", "□", "□", "□", "□", "□", "□"],
                ["□", "□", "□", "□", "□", "□", "□", "□"],
                ["□", "□", "□", "□", "□", "□", "□", "□"],
                ["□", "□", "□", "□", "□", "□", "□", "□"],
                ["□", "□", "□", "□", "□", "□", "□", "□"],
                ["□", "□", "□", "□", "□", "□", "□", "□"],
                ["□", "□", "□", "□", "□", "□", "□", "□"],
                ["□", "□", "□", "□", "□", "□", "□", "□"],
            ])
        
        self.actions = {"check_goal": self.goal_test, "start_transitions":self.state_machine, "add_queen":self.add_queen, "remove_queen":self.remove_queen} 
        self.gen_algo = None
        self.back_algo = None
        self.result = None

    def add_queen(self, row, col):
        self.state[row][col] = "♛"

    def remove_queen(self, row, col):
        self.state[row][col] = "□"

    def state_machine(self,draw, state="Idle", board=None):
        if state == "Idle":
            self.gen_algo = None
            self.back_algo = None

        elif state =="Genetic Algorithm":
            state = "Initialize GA"

        elif state == "Backtracking Algorithm":
            state = "Initialize BA"

        elif state == "Initialize GA":
            if board is None:
                self.gen_algo = GeneticAlgorithm(self)
            else:
                self.gen_algo = GeneticAlgorithm(board)
            state = "Start GA"

        elif state == "Initialize BA":
            if board is None:
                self.back_algo = BacktrackingAlgorithm(self)
            else:
                self.back_algo= BacktrackingAlgorithm(board)
            state = "Start BA"

        elif state == "Start GA":
            if self.gen_algo is not None:
                self.result = self.gen_algo.genetic_algorithm(self.gen_algo.generate_Population(100), draw)
            state = "Idle"

        elif state == "Start BA":
            if self.back_algo is not None:
                self.back_algo.backtracking_algorithm(0, draw)
            state = "Idle"

        return state

    
    def __is_queen_safe(self, row, col):
        
        if self.state[row][col] == "□":
            raise("Not a Queen")

        #Row Check on left
        for i in range(col):
            if self.state[row][i] == "♛":
                return False
        #Row Check on right
        for i in range(col+1,8):
            if self.state[row][i] == "♛":
                return False
        #Col Check on left
        for i in range(row-1,-1,-1):
            if self.state[i][col] == "♛":
                return False
        #Col Check on right
        for i in range(row+1,8):
            if self.state[i][col] == "♛":
                return False
        #Check upper diagonal on left
        for i, j in zip(range(row-1, -1, -1),range(col-1, -1, -1)):
            if self.state[i][j] == "♛":
                return False
        #Check lower diagonal on left
        for i, j in zip(range(row+1, 8, 1),range(col-1, -1, -1)):
            if self.state[i][j] == "♛":
                return False
        #Check upper diagonal on right
        for i, j in zip(range(row-1, -1, -1),range(col+1, 8, 1)):
            if self.state[i][j] == "♛":
                return False
        #Check lower diagonal on right
        for i, j in zip(range(row+1, 8, 1),range(col+1, 8, 1)):
            if self.state[i][j] == "♛":
                return False

        return True


    #goal test
    def goal_test(self):
        for i in  range(len(self.state)):
            for j in range(len(self.state[i])):
                if self.state[i][j] == "♛":
                    if not self.__is_queen_safe(i,j):
                        return False
        return True

    def heuristics(self,subject):
        if self.gen_algo is not None:
            gene = np.array(subject)
            attacks = 0
            row_col_attacks = abs(len(gene)-len(np.unique(gene)))
            attacks += row_col_attacks
            for i in range(len(gene)):
                for j in range(i,len(gene)):
                    if i!=j:
                        dx = abs(i-j)
                        dy = abs(gene[i]-gene[j])
                        if dx == dy:
                            attacks+=1
            return 28 - attacks  
              
        

