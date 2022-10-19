from copy import deepcopy
from stockfish import Stockfish
import random
import numpy as np
import chess
import chess.engine

from engine import GameState
weights = { 'p': 100, 'n': 280, 'b': 320, 'r': 479, 'q': 929, 'k': 60000, 'k_e': 60000 };
pst_l = {
    'p':np.array([
            [ 100, 100, 100, 100, 105, 100, 100,  100],
            [  78,  83,  86,  73, 102,  82,  85,  90],
            [   7,  29,  21,  44,  40,  31,  44,   7],
            [ -17,  16,  -2,  15,  14,   0,  15, -13],
            [ -26,   3,  10,   9,   6,   1,   0, -23],
            [ -22,   9,   5, -11, -10,  -2,   3, -19],
            [ -31,   8,  -7, -37, -36, -14,   3, -31],
            [   0,   0,   0,   0,   0,   0,   0,   0]
        ]),
    'n': np.array([ 
            [-66, -53, -75, -75, -10, -55, -58, -70],
            [ -3,  -6, 100, -36,   4,  62,  -4, -14],
            [ 10,  67,   1,  74,  73,  27,  62,  -2],
            [ 24,  24,  45,  37,  33,  41,  25,  17],
            [ -1,   5,  31,  21,  22,  35,   2,   0],
            [-18,  10,  13,  22,  18,  15,  11, -14],
            [-23, -15,   2,   0,   2,   0, -23, -20],
            [-74, -23, -26, -24, -19, -35, -22, -69]
        ]),
    'b': np.array([ 
            [-59, -78, -82, -76, -23,-107, -37, -50],
            [-11,  20,  35, -42, -39,  31,   2, -22],
            [ -9,  39, -32,  41,  52, -10,  28, -14],
            [ 25,  17,  20,  34,  26,  25,  15,  10],
            [ 13,  10,  17,  23,  17,  16,   0,   7],
            [ 14,  25,  24,  15,   8,  25,  20,  15],
            [ 19,  20,  11,   6,   7,   6,  20,  16],
            [ -7,   2, -15, -12, -14, -15, -10, -10]
        ]),
    'r': np.array([  
            [ 35,  29,  33,   4,  37,  33,  56,  50],
            [ 55,  29,  56,  67,  55,  62,  34,  60],
            [ 19,  35,  28,  33,  45,  27,  25,  15],
            [  0,   5,  16,  13,  18,  -4,  -9,  -6],
            [-28, -35, -16, -21, -13, -29, -46, -30],
            [-42, -28, -42, -25, -25, -35, -26, -46],
            [-53, -38, -31, -26, -29, -43, -44, -53],
            [-30, -24, -18,   5,  -2, -18, -31, -32]
        ]),
    'q': np.array([   
            [  6,   1,  -8,-104,  69,  24,  88,  26],
            [ 14,  32,  60, -10,  20,  76,  57,  24],
            [ -2,  43,  32,  60,  72,  63,  43,   2],
            [  1, -16,  22,  17,  25,  20, -13,  -6],
            [-14, -15,  -2,  -5,  -1, -10, -20, -22],
            [-30,  -6, -13, -11, -16, -11, -16, -27],
            [-36, -18,   0, -19, -15, -15, -21, -38],
            [-39, -30, -31, -13, -31, -36, -34, -42]
        ]),
    'k':np.array([  
            [  4,  54,  47, -99, -99,  60,  83, -62],
            [-32,  10,  55,  56,  56,  55,  10,   3],
            [-62,  12, -57,  44, -67,  28,  37, -31],
            [-55,  50,  11,  -4, -19,  13,   0, -49],
            [-55, -43, -52, -28, -51, -47,  -8, -50],
            [-47, -42, -43, -79, -64, -32, -29, -32],
            [ -4,   3, -14, -50, -57, -18,  13,   4],
            [ 17,  30,  -3, -14,   6,  -1,  40,  18]
        ]),
    'k_e':np.array([
            [-50, -40, -30, -20, -20, -30, -40, -50],
            [-30, -20, -10,   0,   0, -10, -20, -30],
            [-30, -10,  20,  30,  30,  20, -10, -30],
            [-30, -10,  30,  40,  40,  30, -10, -30],
            [-30, -10,  30,  40,  40,  30, -10, -30],
            [-30, -10,  20,  30,  30,  20, -10, -30],
            [-30, -30,   0,   0,   0,   0, -30, -30],
            [-50, -30, -30, -30, -30, -30, -30, -50]
        ])
};

pst_d = {
    'p': np.flip(pst_l['p']),
    'n': np.flip(pst_l['n']),
    'b': np.flip(pst_l['b']),
    'r': np.flip(pst_l['r']),
    'q': np.flip(pst_l['q']),
    'k': np.flip(pst_l['k']),
    'k_e':np.flip(pst_l['k_e'])
}


stockfish = Stockfish(path="../stockfish/stockfish_15_x64_popcnt.exe", depth=20, parameters={"Threads": 2})


def getRandomMove(validMoves):
    return random.choice(validMoves)

def makeStockfishMove(move):
    stockfish.make_moves_from_current_position([move])

def getStockfishMove(validMoves):
    st_move = stockfish.get_best_move()
    move_to_do = None
    for move in validMoves:
        if move.getNotation() == st_move:
            move_to_do = move
            break

    if move_to_do is not None:
        makeStockfishMove(st_move)
    print("move to do", move_to_do, st_move)
    return move_to_do

# minimax with alpha beta pruning for piece square tables
def minimax(board, depth, alpha, beta, maximizingPlayer, validMoves):
    if depth == 0:
        return evaluateBoard(board)

    if maximizingPlayer:
        maxEval = -99999
        for move in validMoves:
            board.movePiece(move)
            eval = minimax(board, depth - 1, alpha, beta, False, board.getValidMoves())
            board.undoMove()
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = 99999
        for move in validMoves:
            board.movePiece(move)
            eval = minimax(board, depth - 1, alpha, beta, True, board.getValidMoves())
            board.undoMove()
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval
#evaluate board with piece square tables
def evaluateBoard(board, pst=pst_d):
    if board.gameOver:
        if not board.whiteToMove:
            return -9999
        else:
            return 9999

    score = 0
    for row in range(8):
        for col in range(8):
            piece = board.board[row][col]
            if piece != "--":
                if piece[1] == "d":
                    score += pst[piece[0]][row][col]
                else:
                    score -= pst[piece[0]][7-row][col]   
    return score
    
    
def negamax(board, depth, alpha, beta, validMoves):
    if depth == 0:
        return evaluateBoard(board)

    maxEval = -99999
    for move in validMoves:
        board.movePiece(move)
        eval = -negamax(board, depth - 1, -beta, -alpha, board.getValidMoves())
        board.undoMove()
        maxEval = max(maxEval, eval)
        alpha = max(alpha, eval)
        if beta <= alpha:
            break
    return maxEval

def getBestMove(state, validMoves):
    bestMove = None
    bestEval = -99999
    for move in validMoves:
        state.movePiece(move)
        eval = minimax(state, 2, -99999, 99999, False, state.getValidMoves())
        state.undoMove()
        if eval > bestEval:
            bestEval = eval
            bestMove = move
    return bestMove


def monteCarlo(board, depth, iterations):
    if depth == 0:
        return evaluateBoard(board)

    maxEval = -99999
    for i in range(iterations):
        if board.getValidMoves() == []:
            break
        board.movePiece(getRandomMove(board.getValidMoves()))
        eval = monteCarlo(board, depth - 1, iterations)
        board.undoMove()
        maxEval = max(maxEval, eval)
    return maxEval

def getBestMoveMCTS(board, validMoves):
    bestMove = None
    bestEval = -99999
    for move in validMoves:
        board.movePiece(move)
        eval = monteCarlo(board, 2, 50)
        board.undoMove()
        if eval > bestEval:
            bestEval = eval
            bestMove = move
    return bestMove


def getBestMoveNegamax(board, validMoves):
    bestMove = None
    bestEval = -99999
    for move in validMoves:
        board.movePiece(move)
        eval = negamax(board, 2, -99999, 99999, board.getValidMoves())
        board.undoMove()
        if eval > bestEval:
            bestEval = eval
            bestMove = move
    return bestMove



