from pydoc import cli
import engine
import pygame

pygame.init()
FONT = pygame.font.Font('freesansbold.ttf', 11)
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

def drawPaths(win,moves):
    if moves is None:
        return
    for x in moves:
        pygame.draw.rect(win,(133,230,160), (x.endCol*SQ_SIZE, x.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawRanks(win,board):
    move = engine.Movement((0,0), (0,0),board)
    for i in range(ROWS):
        for j in range(ROWS):
            rank = move.getRankFile(j, i,);
            text = FONT.render(rank, True, (148, 100, 41))
            win.blit(text, (i*SQ_SIZE,j*SQ_SIZE))
            

def drawGameState(win, state, paths):
    drawBoard(win)
    drawPaths(win, paths)
    drawPieces(win, state.board)
    drawRanks(win, state.board)
    

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
   paths = []
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
                    paths = state.showPaths(engine.Movement((r,c),(0, 0),state.board))
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

        drawGameState(win, state, paths)
        clock.tick(FPS)
        pygame.display.flip()
        
if __name__ == '__main__':
    main()