from pydoc import cli
from ChessAi import *

import numpy as np
import engine
import pygame

pygame.init()
FONT = pygame.font.Font('freesansbold.ttf', 11)
WIDTH =600 
ROWS = 8
SQ_SIZE = WIDTH // ROWS
FPS = 60
IMAGES = {}
BOARD = np.array([
            ["rd", "nd", "bd", "qd", "kd", "bd", "nd", "rd"],
            ["pd", "pd", "pd", "pd", "pd", "pd", "pd", "pd"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["pl", "pl", "pl", "pl", "pl", "pl", "pl", "pl"],
            ["rl", "nl", "bl", "ql", "kl", "bl", "nl", "rl"]
        ])
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
        pygame.draw.rect(win,(255, 245, 109), (x.startCol*SQ_SIZE, x.startRow*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pygame.draw.rect(win,(133,230,160), (x.endCol*SQ_SIZE, x.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawRanks(win,board):
    move = engine.Movement((0,0), (0,0),board)
    for i in range(ROWS):
        for j in range(ROWS):
            rank = move.getRankFile(j, i,);
            text = FONT.render(rank, True, (148, 100, 41))
            win.blit(text, (i*SQ_SIZE,j*SQ_SIZE))

def drawCheck(win, state, inCheck):
    if not inCheck:
        return
    else:       
        if state.whiteToMove:
            (r, c) = state.whiteKingsPosition
        else:
            (r,c) = state.blackKingsPosition
        pygame.draw.rect(win,(245, 102, 66), (c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_last_move(win, move):
    if move is None:
        return
    else:
        pygame.draw.rect(win,(255, 245, 109), (move.startCol*SQ_SIZE, move.startRow*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pygame.draw.rect(win,(133,230,160), (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawGameState(win, state, paths, inCheck, move):
    drawBoard(win)
    drawPaths(win, paths)
    draw_last_move(win,move)
    drawCheck(win, state, inCheck)
    drawPieces(win, state.board)
    drawRanks(win, state.board)

def draw_end(win, endmessage):
    font = pygame.font.Font('freesansbold.ttf', 25)
    text = font.render(endmessage, True, pygame.Color('Brown'))
    location = pygame.Rect(0,0, WIDTH, WIDTH).move(WIDTH/2 - text.get_width()/2, WIDTH/2 - text.get_height()/2)
    win.blit(text, location)

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
   inCheck = False
   last_move = None
   while running: 
        ############################
        #AI Moves
        
        if not state.whiteToMove:
            """
            validMoves = state.getValidMoves()
            if len(validMoves)>0:
                move = getStockfishMove(validMoves)
                last_move = move
                state.movePiece(move)
                moveMade = True
            else: 
                state.gameOver= True
            """
             #get best move
            validMoves = state.getValidMoves()
            if len(validMoves)>0:
                move = getBestMoveNegamax(deepcopy(state), validMoves)
                last_move = move
                state.movePiece(move)
                moveMade = True
            else:
                state.gameOver= True
        
        else:
            """
            validMoves = state.getValidMoves()
            if len(validMoves)>0:
                move = getStockfishMove(validMoves)
                last_move = move
                state.movePiece(move)
                moveMade = True
            else: 
                state.gameOver= True
            """
           
        
        
        
        #############################
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
               running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if not state.gameOver:
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
                        for i in range(len(validMoves)):
                            if move == validMoves[i]: 
                                if validMoves[i].isPromotion:
                                    validOptions = ['q', 'r', 'n','b']
                                    piece = None
                                    while piece not in validOptions:
                                        print("Press q for Queen, r for Rook, n for knight or b for Bishop")
                                        piece = input()
                                    validMoves[i].promotion = piece
                                state.movePiece(validMoves[i])
                                makeStockfishMove(validMoves[i].getNotation())
                                last_move = move
                                moveMade = True
                                selected = ()
                                clicks = []
                                
                        if not moveMade:
                            clicks = [selected]
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    state.undoMove()
                    moveMade = True
            
        if moveMade:
            validMoves= state.getValidMoves()
            moveMade = False
        if state.inCheck():
            inCheck = True
        else:
            inCheck = False
        if state.gameOver:
            drawGameState(win, state, paths, inCheck, last_move)
            if state.stalemate:
                draw_end(win,"Stalemate, Game ended")
            else:
                draw_end(win, "Checkmate Game ended")
        else:
            drawGameState(win, state, paths, inCheck, last_move)
        
        clock.tick(FPS)
        pygame.display.flip()
        
if __name__ == '__main__':
    main()