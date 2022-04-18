from cmath import pi
from copy import deepcopy
from shutil import move
import numpy as np;

class GameState():
    def __init__(self):
        self.board = np.array([
            ["rd", "nd", "bd", "qd", "kd", "bd", "nd", "rd"],
            ["pd", "pd", "pd", "pd", "pd", "pd", "pd", "pd"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["pl", "pl", "pl", "pl", "pl", "pl", "pl", "pl"],
            ["rl", "nl", "bl", "ql", "kl", "bl", "nl", "rl"]
        ])
        self.whiteToMove=True
        self.moveLog = []
        self.whiteKingsPosition = (0,4)
        self.blackKingsPosition = (7,4)
        self.gameOver = False
        self.currentCasteling = Castleling(True, True, True, True)
        self.castleLog = [deepcopy(self.currentCasteling)]

    def printBoard(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                print(self.board[i,j]," ",end="")
            print()

    def movePiece(self, move):
        self.board[move.startRow][move.startCol]= "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == "kl":
            self.whiteKingsPosition = (move.endRow, move.endCol)
        elif move.pieceMoved == "kd":
            self.blackKingsPosition = (move.endRow, move.endCol)

        if move.isPromotion:
            self.board[move.endRow][move.endCol] = move.promotion + move.pieceMoved[1]

        if move.isCastleMove:
            if move.endCol - move.startCol ==2: #Kingside Castle
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = "--"
            else: # Queenside Castle
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = "--"


        #Caste Rights
        if move.pieceMoved == 'kl':
            self.currentCasteling.lks = False
            self.currentCasteling.lqs = False
        elif move.pieceMoved =='kd':
            self.currentCasteling.dks = False
            self.currentCasteling.dqs = False
        elif move.pieceMoved == "rl":
            if move.startRow == 7:
                if move.startCol ==0:
                    self.currentCasteling.lqs = False
                elif move.startCol ==7:
                    self.currentCasteling.lks = False
        elif move.pieceMoved == "rd":
            if move.startRow == 0:
                if move.startCol ==0:
                    self.currentCasteling.dqs = False
                elif move.startCol ==7:
                    self.currentCasteling.dks = False
        
        self.castleLog.append(deepcopy(self.currentCasteling))
                

    def undoMove(self):
        if len(self.moveLog)!=0:
            lastMove = self.moveLog.pop()
            self.board[lastMove.startRow][lastMove.startCol] = lastMove.pieceMoved
            self.board[lastMove.endRow][lastMove.endCol] = lastMove.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if lastMove.pieceMoved == "kl":
                self.whiteKingsPosition = (lastMove.startRow, lastMove.startCol)
            elif lastMove.pieceMoved == "kd":
                self.blackKingsPosition = (lastMove.startRow, lastMove.startCol)
            
            self.castleLog.pop()
            self.currentCasteling =deepcopy(self.castleLog[-1])

            #Undo castle move
            if lastMove.isCastleMove:
                if lastMove.endCol - lastMove.startCol  == 2:
                    self.board[lastMove.endRow][lastMove.endCol+1] = self.board[lastMove.endRow][lastMove.endCol-1]
                    self.board[lastMove.endRow][lastMove.endCol-1] ="--"
                else:
                    self.board[lastMove.endRow][lastMove.endCol-2] = self.board[lastMove.endRow][lastMove.endCol+1]
                    self.board[lastMove.endRow][lastMove.endCol+1] ="--"


    def showPaths(self,move):
        currentpiece = move.pieceMoved
        currentmoves =[]
        
        if currentpiece == "--":
            return
        if self.whiteToMove:
            if currentpiece[1] !="l":
                return
        else:
            if currentpiece[1] !="d":
                return

        if currentpiece[0] =="p":
            self.__getPawnMoves(move.startRow, move.startCol, currentmoves)
        elif currentpiece[0] =="b":
            self.__getBishopMoves(move.startRow, move.startCol, currentmoves)
        elif currentpiece[0] =="n":
            self.__getKnightMoves(move.startRow, move.startCol, currentmoves)
        elif currentpiece[0] =="r":
            self.__getRookMoves(move.startRow, move.startCol, currentmoves)
        elif currentpiece[0] =="q":
            self.__getQueenMoves(move.startRow, move.startCol, currentmoves)
        elif currentpiece[0] =="k":
            self.__getKingMoves(move.startRow, move.startCol, currentmoves)

        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingsPosition[0], self.whiteKingsPosition[1], currentmoves)
        else:
            self.getCastleMoves(self.blackKingsPosition[0], self.blackKingsPosition[1], currentmoves)


        validmoves = self.getValidMoves()
        filteredmoves = []
        for move in currentmoves:
            if move in validmoves:
                filteredmoves.append(move)
        return filteredmoves

    def inCheck(self):
        if self.whiteToMove:
            r, c = self.whiteKingsPosition
        else:
            r, c = self.blackKingsPosition

        self.whiteToMove = not self.whiteToMove
        moves = self.getAllMoves()
        self.whiteToMove = not self.whiteToMove
        for move in moves:
            if move.endRow == r and move.endCol == c:
                return True
        return False
            
    def isUnderAttack(self, row, col):
        self.whiteToMove = not self.whiteToMove
        opponentMoves = self.getAllMoves()
        self.whiteToMove = not self.whiteToMove

        for move in opponentMoves:
            if move.endRow == row and move.endCol == col:
                return True
        return False


    def getValidMoves(self):
        allmoves = self.getAllMoves()
        tempCastleRights = deepcopy(self.currentCasteling)
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingsPosition[0], self.whiteKingsPosition[1], allmoves)
        else:
            self.getCastleMoves(self.blackKingsPosition[0], self.blackKingsPosition[1], allmoves)

        for i in range(len(allmoves)-1, -1,-1):
            self.movePiece(allmoves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                allmoves.remove(allmoves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        if len(allmoves) ==0:
            self.gameOver = True
        else:
            self.gameOver = False
        
        self.currentCasteling = tempCastleRights
        return allmoves

    def getAllMoves(self):
        moves = []
        for i in range(8):
            for j in range(8):
                turn = self.board[i][j][1]
                if (turn == 'l' and self.whiteToMove) or (turn=='d' and not self.whiteToMove):
                    piece = self.board[i][j][0]
                    if piece == 'p':
                        self.__getPawnMoves(i, j, moves)
                    elif piece == 'r':
                        self.__getRookMoves(i, j, moves)
                    elif piece == 'b':
                        self.__getBishopMoves(i, j, moves)
                    elif piece == 'n':
                        self.__getKnightMoves(i, j, moves)
                    elif piece == 'q':
                        self.__getQueenMoves(i, j, moves)
                    elif piece == 'k':
                        self.__getKingMoves(i, j, moves)
        #for i in moves:
            #print(i)  
        return moves

    def __getPawnMoves(self, row, col, moves):
        if self.whiteToMove:
            if row-1>=0 and self.board[row-1][col]=="--": #Square in front is empty
                moves.append(Movement((row,col),(row-1,col), self.board))
                if row == 6 and self.board[row-2][col] =="--":
                    moves.append(Movement((row,col),(row-2,col), self.board))
            if col-1>=0 and row-1>=0: #Capture left
                if self.board[row-1][col-1][1] == "d":
                    moves.append(Movement((row,col),(row-1,col-1), self.board))
            if col+1 <=7 and row-1>=0: #Capture Right
                if self.board[row-1][col+1][1] == "d":
                    moves.append(Movement((row,col),(row-1,col+1), self.board))
        elif not self.whiteToMove:
            if row+1 <=7 and self.board[row+1][col]=="--":
                moves.append(Movement((row,col),(row+1,col), self.board))
                if row == 1 and self.board[row+2][col] =="--":            
                    moves.append(Movement((row,col),(row+2,col), self.board))
            if col-1>=0 and row+1<=7: #Capture left
                if self.board[row+1][col-1][1] == "l":
                    moves.append(Movement((row,col),(row+1,col-1), self.board))
            if col+1 <=7 and row+1<=7: #Capture Right
                if self.board[row+1][col+1][1] == "l":
                    moves.append(Movement((row,col),(row+1,col+1), self.board))

    def __getRookMoves(self, row, col, moves): 
        startrow = row
        startcol = col
        opponentpiececolor = "l"
        if self.whiteToMove:
            opponentpiececolor = "d"

        while row-1>=0: #Upwards
            if self.board[row-1][col] == "--":
                moves.append(Movement((startrow,startcol),(row-1,col), self.board))
            elif self.board[row-1][col][1] ==opponentpiececolor:
                moves.append(Movement((startrow,startcol),(row-1,col), self.board))
                break
            else:
                break
            row-=1
        row = startrow
        col = startcol
        while row+1<=7:#Downwards
            if self.board[row+1][col] == "--":
                moves.append(Movement((startrow,startcol),(row+1,col), self.board))
            elif self.board[row+1][col][1] ==opponentpiececolor:
                moves.append(Movement((startrow,startcol),(row+1,col), self.board))
                break
            else:
                break
            row+=1
        row = startrow
        col = startcol
        while col-1>=0:#Left
            if self.board[row][col-1] == "--":
                moves.append(Movement((startrow,startcol),(row,col-1), self.board))
            elif self.board[row][col-1][1] ==opponentpiececolor:
                moves.append(Movement((startrow,startcol),(row,col-1), self.board))
                break
            else:
                break
            col-=1
        row = startrow
        col = startcol
        while col+1<=7:#Right
            if self.board[row][col+1] == "--":
                moves.append(Movement((startrow,startcol),(row,col+1), self.board))
            elif self.board[row][col+1][1] ==opponentpiececolor:
                moves.append(Movement((startrow,startcol),(row,col+1), self.board))
                break
            else:
                break
            col+=1
    
    def __getBishopMoves(self, row,col,moves):
        startrow = row
        startcol = col
        opponentpiececolor = "l"
        if self.whiteToMove:
            opponentpiececolor = "d"
        while row+1<=7 and col-1>=0:#Diagonal down left
            if self.board[row+1][col-1] == "--": 
                moves.append(Movement((startrow,startcol),(row+1,col-1), self.board))
            elif self.board[row+1][col-1][1] == opponentpiececolor:
                moves.append(Movement((startrow,startcol),(row+1,col-1), self.board))
                break
            else:
                break
            row+=1
            col-=1
        row = startrow
        col = startcol
        while row-1>=0 and col+1<=7:#Diagonal up right
            if self.board[row-1][col+1] == "--": 
                moves.append(Movement((startrow,startcol),(row-1,col+1), self.board))
            elif self.board[row-1][col+1][1] == opponentpiececolor:
                moves.append(Movement((startrow,startcol),(row-1,col+1), self.board))
                break
            else:
                break
            row-=1
            col+=1
        row = startrow
        col = startcol
        while row-1>=0 and col-1>=0:#Diagonal up left
            if self.board[row-1][col-1] == "--": 
                moves.append(Movement((startrow,startcol),(row-1,col-1), self.board))
            elif self.board[row-1][col-1][1] == opponentpiececolor:
                moves.append(Movement((startrow,startcol),(row-1,col-1), self.board))
                break
            else:
                break
            row-=1
            col-=1
        row = startrow
        col = startcol
        while row+1<=7 and col+1<=7:#Diagonal up left
            if self.board[row+1][col+1] == "--": 
                moves.append(Movement((startrow,startcol),(row+1,col+1), self.board))
            elif self.board[row+1][col+1][1] == opponentpiececolor:
                moves.append(Movement((startrow,startcol),(row+1,col+1), self.board))
                break
            else:
                break
            row+=1
            col+=1
        
    def __getKnightMoves(self, row, col, moves):
        opponentpiececolor = "l"
        if self.whiteToMove: 
            opponentpiececolor = "d"
        #Top right
        if row-2>=0 and col+1<=7: #2 Up 1 Right
            if self.board[row-2][col+1] == "--" or self.board[row-2][col+1][1]==opponentpiececolor:
                moves.append(Movement((row,col),(row-2,col+1), self.board))
        if row-1>=0 and col+2<=7: #1 Up 2 Right
            if self.board[row-1][col+2] == "--" or self.board[row-1][col+2][1]==opponentpiececolor:
                moves.append(Movement((row,col),(row-1,col+2), self.board))
        if row+1<=7 and col+2<=7: #1 Down 2 Right
            if self.board[row+1][col+2] == "--" or self.board[row+1][col+2][1]==opponentpiececolor:
                moves.append(Movement((row,col),(row+1,col+2), self.board))
        if row+2<=7 and col+1<=7: #2 Down 1 Right
            if self.board[row+2][col+1] == "--" or self.board[row+2][col+1][1]==opponentpiececolor:
                moves.append(Movement((row,col),(row+2,col+1), self.board))
        if row+2<=7 and col-1>=0: #2 Down 1 Left
            if self.board[row+2][col-1] == "--" or self.board[row+2][col-1][1]==opponentpiececolor:
                moves.append(Movement((row,col),(row+2,col-1), self.board))
        if row+1<=7 and col-2>=0: #1 Down 2 Left
            if self.board[row+1][col-2] == "--" or self.board[row+1][col-2][1]==opponentpiececolor:
                moves.append(Movement((row,col),(row+1,col-2), self.board))
        if row-1>=0 and col-2>=0: #1 Up 2 Left
            if self.board[row-1][col-2] == "--" or self.board[row-1][col-2][1]==opponentpiececolor:
                moves.append(Movement((row,col),(row-1,col-2), self.board))
        if row-2>=0 and col-1>=0: #2 Up 1 Left
            if self.board[row-2][col-1] == "--" or self.board[row-2][col-1][1]==opponentpiececolor:
                moves.append(Movement((row,col),(row-2,col-1), self.board))

    def __getQueenMoves(self, row, col, moves):
        self.__getBishopMoves(row,col, moves)
        self.__getRookMoves(row, col, moves)

    def __getKingMoves(self, row, col,moves):
        opponentpiececolor = "l"
        if self.whiteToMove: 
            opponentpiececolor = "d"

        if row-1>=0: #Top Row
            if col+1<=7:
                if self.board[row-1][col+1] == "--" or self.board[row-1][col+1][1]==opponentpiececolor:
                    moves.append(Movement((row,col),(row-1,col+1), self.board))
            if col-1>=0:
                if self.board[row-1][col-1] == "--" or self.board[row-1][col-1][1]==opponentpiececolor:
                    moves.append(Movement((row,col),(row-1,col-1), self.board))
            if self.board[row-1][col] == "--" or self.board[row-1][col][1]==opponentpiececolor:
                    moves.append(Movement((row,col),(row-1,col), self.board))
        if row+1<=7:#Bottom Row
            if col+1<=7:
                if self.board[row+1][col+1] == "--" or self.board[row+1][col+1][1]==opponentpiececolor:
                    moves.append(Movement((row,col),(row+1,col+1), self.board))
            if col-1>=0:
                if self.board[row+1][col-1] == "--" or self.board[row+1][col-1][1]==opponentpiececolor:
                    moves.append(Movement((row,col),(row+1,col-1), self.board))
            if self.board[row+1][col] == "--" or self.board[row+1][col][1]==opponentpiececolor:
                    moves.append(Movement((row,col),(row+1,col), self.board))

        #Current Row
        if col+1<=7:
                if self.board[row][col+1] == "--" or self.board[row][col+1][1]==opponentpiececolor:
                    moves.append(Movement((row,col),(row,col+1), self.board))
        if col-1>=0:
            if self.board[row][col-1] == "--" or self.board[row][col-1][1]==opponentpiececolor:
                moves.append(Movement((row,col),(row,col-1), self.board))


        

    def getCastleMoves(self, row, col,moves):
        if self.isUnderAttack(row, col):
            return
        if (self.whiteToMove and self.currentCasteling.lks) or (not self.whiteToMove and self.currentCasteling.dks):
            self.getKingsideCastle(row, col, moves,)
        if (self.whiteToMove and self.currentCasteling.lqs) or (not self.whiteToMove and self.currentCasteling.dqs):
            self.getQueensideCastle(row,col,moves)
        

    def getKingsideCastle(self,row, col,moves):
        if self.board[row][col+1] == "--" and self.board[row][col+2] =="--":
            if not self.isUnderAttack(row, col+1) and not self.isUnderAttack(row, col+2):
                moves.append(Movement((row, col),(row,col+2), self.board,isCastleMove=True))

    def getQueensideCastle(self,row, col,moves):
        if self.board[row][col-1] == "--" and self.board[row][col-2] =="--" and self.board[row][col-3]:
            if not self.isUnderAttack(row, col-1) and not self.isUnderAttack(row, col-2):
                 moves.append(Movement((row, col),(row,col-2), self.board,isCastleMove=True))

class Castleling:
    def __init__(self, lks, dks, lqs, dqs):
        self.lks = lks
        self.dks = dks
        self.lqs = lqs
        self.dqs = dqs        

class Movement:
    ranksToRows = {"1":7, "2":6, "3":5, "4":4,
                   "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v:k for k,v in ranksToRows.items()}
    filesToCols = {"a":0, "b":1, "c":2, "d":3,
                   "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v:k for k,v in filesToCols.items()}
    def __init__(self, start, end, board, isCastleMove = False):
        self.startRow = start[0]
        self.startCol = start[1]
        self.endRow= end[0]
        self.endCol= end[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPromotion = False
        self.promotion = 'q'
        if (self.pieceMoved =="pl" and self.endRow == 0) or (self.pieceMoved=="pd"and self.endRow == 7):
            self.isPromotion = True
        self.moveID = self.startRow * 1000 + self.startCol* 100 + self.endRow * 10 +self.endCol 
        self.isCastleMove = isCastleMove

    def getRankFile(self, r, c):
        return self.colsToFiles[c]+ self.rowsToRanks[r] 

    def getNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol) + str(self) 
    def __eq__(self, other):
        if isinstance(other, Movement):
            return self.moveID == other.moveID
        return False
    
    def __str__(self):
        return "(" +str(self.startRow) + ","+str(self.startCol)  + ")(" + str(self.endRow) + ","+str(self.endCol) + ")"