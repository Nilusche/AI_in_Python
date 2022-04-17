from pydoc import cli
import engine
import pygame

pygame.init()
WIDTH = 400
ROWS = 8
SQ_SIZE = WIDTH // ROWS
FPS = 60
IMAGES = {}

def loadImages():
    pieces = ["bd", "bl", "kd", "kl", "nd", "nl", "pd", "pl", "qd","ql","rd", "rl"]
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("../images/Chess_"+piece+"t60.png"),(SQ_SIZE, SQ_SIZE))

def drawBoard(win):
    #brown: 215, 168, 110
    #light: 255, 235, 193
    for i in range(ROWS):
        for j in range(ROWS):
            if (i+j) % 2 ==0:
                pygame.draw.rect(win,(255,235,193), (i*SQ_SIZE, j*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            else:
                pygame.draw.rect(win,(215,168,110), (i*SQ_SIZE, j*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(win, board):
    for i in range(ROWS):
        for j in range(ROWS):
            if board[j][i] != "--":
                win.blit(IMAGES[board[j][i]], (i*SQ_SIZE,j*SQ_SIZE))


def drawGameState(win, state):
    drawBoard(win)
    drawPieces(win, state.board)

def main():
   win = pygame.display.set_mode((WIDTH, WIDTH)) 
   clock = pygame.time.Clock();
   win.fill(pygame.Color("white"))
   state = engine.GameState()
   validMoves = state.getValidMoves()
   moveMade = False
   loadImages()
   running = True
   selected= ()
   clicks = []
   while running: 
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
               running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                r = pos[1] // SQ_SIZE
                c = pos[0] // SQ_SIZE
                if selected == (r,c):
                    selected = ()
                    clicks = []
                else:
                    selected= (r, c)
                    clicks.append(selected)
                if len(clicks) ==2:
                    move = engine.Movement(clicks[0], clicks[1],state.board)
                    print(move.getNotation())
                    if move in validMoves: 
                        state.movePiece(move)
                        moveMade = True
                    selected = ()
                    clicks = []
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    state.undoMove()
                    moveMade = True
        if moveMade:
            validMoves= state.getValidMoves()
            moveMade = False

        drawGameState(win, state)
        clock.tick(FPS)
        pygame.display.flip()
        
if __name__ == '__main__':
    main()