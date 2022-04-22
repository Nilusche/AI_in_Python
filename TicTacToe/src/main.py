import pygame
from minimax import TicTacToe

#Testcommit
pygame.init()
FONT = pygame.font.Font('freesansbold.ttf', 11)
WIDTH = 300
ROWS = 3
SQ_SIZE = WIDTH // ROWS
FPS = 60
IMAGES = {}
BOARD = [
    [ '_', '_', '_' ],
    [ '_', '_', '_' ],
    [ '_', '_', '_' ]
]

def load_images():
    pieces = ["X", "O"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("../images/"+piece+".png"),(SQ_SIZE, SQ_SIZE))

def draw_grid(win):
    for i in range(ROWS):
        pygame.draw.line(win, (0,0,0), (0,i*SQ_SIZE+100), (WIDTH+100, i*SQ_SIZE+100))
        for j in range(ROWS):
            pygame.draw.line(win, (0,0,0), (j*SQ_SIZE+100, 0), (j*SQ_SIZE+100, WIDTH+100))

def draw_board(win, board):
    for i in range(ROWS):
        for j in range(ROWS):
            if board[j][i] !="_":
                win.blit(IMAGES[board[j][i]], (i*SQ_SIZE, j*SQ_SIZE))


def draw_game(win, board):
    win.fill((255,255,255))
    draw_grid(win)
    draw_board(win, board)

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def main():
    win = pygame.display.set_mode((WIDTH, WIDTH)) 
    clock = pygame.time.Clock();
    win.fill(pygame.Color("white"))
    load_images()
    game = TicTacToe(BOARD)
    running = True
    Humanturn = False
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if Humanturn and game.evaluate_game_state() not in [10, -10]:
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, WIDTH)
                    if game.board[col][row] == "_":
                        game.board[col][row] = "X"
                        Humanturn = False
        if not Humanturn and game.evaluate_game_state() not in [10, -10]:       
            best_move = game.find_best_move("O")
            row, col = best_move
            if best_move != (None, None):
                game.board[row][col] = "O"
            Humanturn = True
        #AI vs AI
        '''
        elif Humanturn and game.evaluate_game_state() not in [10, -10]:
            best_move = game.find_best_move("X")
            row, col = best_move
            if best_move != (None, None):
                game.board[row][col] = "X"
            Humanturn = False
        
        pygame.time.wait(800)
        '''
        draw_game(win, game.board)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()