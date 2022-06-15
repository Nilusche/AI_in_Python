import asyncio
import pygame
from Queens import *

pygame.init()
WIDTH = 400
ROWS = 8
RECT_SIZE = WIDTH // ROWS
FPS = 60
IMAGE = {"♛":pygame.transform.scale(pygame.image.load("./images/Chess_qdt60.png"), (RECT_SIZE,RECT_SIZE))}
INITIAL_STATE = np.array([
    ["□", "□", "□", "□", "□", "□", "□", "□"],
    ["□", "□", "□", "□", "□", "□", "□", "□"],
    ["□", "□", "□", "□", "□", "□", "□", "□"],
    ["□", "□", "□", "□", "□", "□", "□", "□"],
    ["□", "□", "□", "□", "□", "□", "□", "□"],
    ["□", "□", "□", "□", "□", "□", "□", "□"],
    ["□", "□", "□", "□", "□", "□", "□", "□"],
    ["□", "□", "□", "□", "□", "□", "□", "□"], 
])

def draw_board(win):
    for i in range(ROWS):
        for j in range(ROWS):
            if (i+j) % 2 == 0:
                pygame.draw.rect(win,(255,255,255), (i*RECT_SIZE, j*RECT_SIZE, RECT_SIZE, RECT_SIZE))
            else:
                pygame.draw.rect(win,(148,149,153), (i*RECT_SIZE, j*RECT_SIZE, RECT_SIZE, RECT_SIZE))
    
def draw_queens(win, state):
    for i in range(ROWS):
        for j in range(ROWS):
            if state[j][i] != "□":
                win.blit(IMAGE["♛"], (i* RECT_SIZE, j*RECT_SIZE))

def draw_state(win, board, crossoverpoint):
    draw_board(win)
    draw_queens(win, board)
    shape_surf = pygame.Surface((RECT_SIZE, RECT_SIZE))
    shape_surf.set_alpha(128)
    if crossoverpoint != -1:
        for row in range(ROWS):
            for col in range(ROWS):
                if row < crossoverpoint:
                    shape_surf.fill((255,255,0))
                    win.blit(shape_surf,(row*RECT_SIZE, col*RECT_SIZE, RECT_SIZE, RECT_SIZE))
                else:
                    shape_surf.fill((0,0,255))
                    win.blit(shape_surf,(row*RECT_SIZE, col*RECT_SIZE, RECT_SIZE, RECT_SIZE))
    #pygame.time.wait(10)
def draw_backtracking(win,board):
    draw_board(win)
    draw_queens(win,board)  
    font = pygame.font.Font('freesansbold.ttf', 25)
    text = font.render("BA computing", True, pygame.Color('Brown'))
    location = pygame.Rect(0,0, WIDTH, WIDTH).move(WIDTH/2 - text.get_width()/2, WIDTH/2 - text.get_height()/2)
    win.blit(text, location) 


def draw_generation(win, gen,game):
    if gen=="Generation: 0":
        return

    font = pygame.font.Font('freesansbold.ttf', 25)
    text = font.render(gen, True, pygame.Color('Brown'))
    location = pygame.Rect(0,0, WIDTH, WIDTH).move(WIDTH/2 - text.get_width()/2, WIDTH/2 - text.get_height()/2)
    win.blit(text, location)

    if not game.actions["check_goal"]():
        text = font.render("No Solution", True, pygame.Color('Brown'))
        win.blit(text, location.move(25,25))

def main():
    win = pygame.display.set_mode((WIDTH, WIDTH))
    clock = pygame.time.Clock();
    win.fill(pygame.Color("white"))
    running = True
    game = QueensGame(INITIAL_STATE)
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    ## Genetic Algorithm ##
                    initial_state = "Genetic Algorithm"
                    while initial_state != "Idle":
                        initial_state = game.actions["start_transitions"](lambda:draw_state(win, game.state, game.gen_algo.crossoverpoint), state=initial_state)
                    game.gen_algo.crossoverpoint = -1
                    #######################
                elif e.key ==pygame.K_b:#
                    ## Backtracking ##
                    initial_state = "Backtracking Algorithm"
                    while initial_state != "Idle":
                        initial_state = game.actions["start_transitions"](lambda:draw_backtracking(win, game.state), state=initial_state)
                    #######################

        if game.gen_algo is not None:
            draw_state(win, game.state, game.gen_algo.crossoverpoint)
            draw_generation(win,"Generation: "+str(game.gen_algo.generation), game)
        elif game.back_algo is not None:
            draw_backtracking(win,game.state)
        else:
            draw_state(win,game.state,-1)    


        
        clock.tick(FPS)
        pygame.display.flip()

if __name__ == '__main__':
    main()