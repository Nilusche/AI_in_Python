# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 19:56:54 2022

@author: User Ben
"""

import pygame
import math

from Queue import *

WIN_WIDTH = 600 
WIN = pygame.display.set_mode((WIN_WIDTH+200, WIN_WIDTH+200))
pygame.display.set_caption("A* Pathplanning")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165 ,0)

GREY = (128, 128, 128)
#Startnode
PINK = (255,51,153)
#Endnode
PURPLE = (255, 255, 64)

GRID =          [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 3],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

pygame.init()

def drawcaption():
    font1 = pygame.font.SysFont('Arial', 20)
    for i in range(1, 21):
        WIN.blit(font1.render(str(i), True, BLACK), (30*i+75, 70))
        WIN.blit(font1.render(str(21-i), True, BLACK), (70, 30*i+75))

    WIN.blit(font1.render('S', True, BLACK), (108, 675))
    WIN.blit(font1.render('G', True, BLACK), (678, 104))
    pygame.display.update()


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt(math.pow((x1-x2), 2) + math.pow((y1-y2), 2)) #Euclidean distance
    #return abs(x1-x2) + abs(y1-y2) #Manhattan distance

class Grid:
    
    def __init__(self):
        self.grid = []
    
    def make_node_grid(self, rows, width,  grid):
        node_grid = []
        gap = width// rows
        for i in range(rows):
            node_grid.append([])
            for j in range(rows):
                node = Field(i, j, gap)
                if grid[j][i] == 0:
                    node.set_obstacle()
                elif grid[j][i] == 2:
                    node.set_start()
                elif grid[j][i] == 3:
                    node.set_end()
                node_grid[i].append(node)

        return node_grid

    def draw_grid_lines(self,win,  rows, width):
        gap = width // rows
        for i in range(21):  
            pygame.draw.line(win, BLACK, (100, i*gap+100), (width+100, i*gap+100))
            for j in range(21):
                pygame.draw.line(win, BLACK, (j*gap+100, 100), (j*gap+100, width+100))                 

    def udpate(self,win, rows, width):
        for i in range(20):
            for j in range(20):
                self.grid[i][j].draw(win)
        self.draw_grid_lines(win,rows, width)
        drawcaption()
        #pygame.time.wait(50)
        pygame.display.update()

    def draw_grid(self, win, rows, width):
        win.fill(WHITE)

        grid = self.make_node_grid(rows, width, GRID)
        self.grid = grid
        #update neigbours of grid
        for row in self.grid:
            for field in row:
                field.update_neighbours(grid)

        for i in range(20):
            for j in range(20):
                grid[i][j].draw(win)
        self.draw_grid_lines(win, rows,width)

        
        pygame.display.update()



class Field:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.width = width
        self.x = row*width
        self.y = col*width
        self.neighbours= []
        self.color = WHITE
        self.g_value = float("inf")
        self.f_value = float("inf")

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == YELLOW
    
    def is_open(self):
        return self.color == GREEN

    def is_obstacle(self):
        return self.color == BLACK
    
    def is_start(self): 
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == PURPLE    

    def reset(self):
        self.color = WHITE
    
    def set_start(self):
        self.color = ORANGE

    def set_end(self):
        self.color = PURPLE

    def set_open(self):
        self.color = GREEN

    def set_closed(self):
        self.color =YELLOW
    
    def set_obstacle(self):
        self.color = BLACK
    
    def set_path(self):
        self.color = RED

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x+100, self.y+100, self.width, self.width))
    

    def update_neighbours(self, node_grid):
        self.neighbours=[]
        if self.col <19: #Right
            if not node_grid[self.row][self.col+1].is_obstacle():
                self.neighbours.append(node_grid[self.row][self.col+1]) 

        if self.col > 0: # Left
            if not node_grid[self.row][self.col-1].is_obstacle():
                self.neighbours.append(node_grid[self.row][self.col-1])

        if self.row <19: #DOWN
            if not node_grid[self.row+1][self.col].is_obstacle():
                self.neighbours.append(node_grid[self.row+1][self.col]) 

        if self.row > 0: #UP
            if not node_grid[self.row-1 ][self.col].is_obstacle():
                self.neighbours.append(node_grid[self.row-1 ][self.col])

    def __lt__(self, other):
        return self.f_value < other.f_value

def draw_path(path, current, draw):
    current.set_path()
    while current in path:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = path[current]
        current.set_path()
        draw()
        
    drawcaption()

def dfs(draw,start:Field, end:Field):
    open_list = Queue("LIFO")
    path = {}
    open_list.push(start)
    start.set_closed()
    while not open_list.is_empty():

        current_node = open_list.pop()
        current_node.set_closed()
        if current_node == end:
            draw_path(path,end,draw)
            return True

        for neighbour in current_node.neighbours:
            if not neighbour.is_closed():
                path[neighbour] =current_node
                open_list.push(neighbour)

        draw()  

    return False      

def bfs(draw, start:Field, end:Field):
    open_list = Queue("FIFO")
    path = {}
    open_list.push(start)
    start.set_closed()
    while not open_list.is_empty():

        current_node = open_list.pop()
        if current_node == end:
            draw_path(path,end,draw)
            return True

        for neighbour in current_node.neighbours:
            if not neighbour.is_closed():
                path[neighbour] =current_node
                open_list.push(neighbour)
                neighbour.set_closed()

        draw()  

    return False      


def astar(draw, start:Field, end:Field):
    open_list = Queue("PRIO", False)
    #Initialize the starting node scores
    start.g_value = 0
    start.f_value = start.g_value + h(start.get_pos(), end.get_pos())
    
    open_list.push(start) 
    path ={}

    while not open_list.is_empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_node = open_list.pop()

        if current_node == end:
            draw_path(path,end, draw)
            return True
        
        for neighbour in current_node.neighbours:
            tmp_g = current_node.g_value +1
            if tmp_g < neighbour.g_value:
                if not neighbour.is_closed():
                    if neighbour not in open_list:
                        open_list.push(neighbour)             
                path[neighbour] = current_node
                neighbour.g_value = tmp_g
                neighbour.f_value = tmp_g + h(neighbour.get_pos(), end.get_pos())
                neighbour.set_open()
        
        draw()
        
        if current_node != start:
            current_node.set_closed()
        
    return False    


def main(win, width):
    g = Grid()
    run = True
    g.draw_grid(win,20, width)
    drawcaption()
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN: 
                g.draw_grid(win,20, width)
                if event.key == pygame.K_RETURN:
                    astar(lambda: g.udpate(win,20, WIN_WIDTH),g.grid[0][19], g.grid[19][0])
                if event.key == pygame.K_t:
                    dfs(lambda: g.udpate(win,20, WIN_WIDTH),g.grid[0][19], g.grid[19][0])
                if event.key == pygame.K_b:
                    bfs(lambda: g.udpate(win,20, WIN_WIDTH),g.grid[0][19], g.grid[19][0])
        pygame.time.Clock().tick(60)            
        

    pygame.quit()     
            

main(WIN, WIN_WIDTH) 
