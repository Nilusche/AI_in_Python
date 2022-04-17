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

    def undoMove(self):
        if len(self.moveLog)!=0:
            lastMove = self.moveLog.pop()
            self.board[lastMove.startRow][lastMove.startCol] = lastMove.pieceMoved
            self.board[lastMove.endRow][lastMove.endCol] = lastMove.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        return self.getAllMoves()

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
        for i in moves:
            print(i)  
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
        if self.whiteToMove:
            startrow = row
            startcol = col
            while row-1>=0: #Upwards
                if self.board[row-1][col] == "--":
                    moves.append(Movement((startrow,startcol),(row-1,col), self.board))
                elif self.board[row-1][col][1] =="d":
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
                elif self.board[row+1][col][1] =="d":
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
                elif self.board[row][col-1][1] =="d":
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
                elif self.board[row][col+1][1] =="d":
                    moves.append(Movement((startrow,startcol),(row,col+1), self.board))
                    break
                else:
                    break
                col+=1
        if not self.whiteToMove:
            startrow = row
            startcol = col
            while row-1>=0: #Upwards
                if self.board[row-1][col] == "--":
                    moves.append(Movement((startrow,startcol),(row-1,col), self.board))
                elif self.board[row-1][col][1] =="l":
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
                elif self.board[row+1][col][1] =="l":
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
                elif self.board[row][col-1][1] =="l":
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
                elif self.board[row][col+1][1] =="l":
                    moves.append(Movement((startrow,startcol),(row,col+1), self.board))
                    break
                else:
                    break
                col+=1

            
    def __getBishopMoves(self, row,col,moves):
        startrow = row
        startcol = col
        if self.whiteToMove:
            while row+1<=7 and col-1>=0:#Diagonal down left
                if self.board[row+1][col-1] == "--": 
                    moves.append(Movement((startrow,startcol),(row+1,col-1), self.board))
                elif self.board[row+1][col-1][1] == "d":
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
                elif self.board[row-1][col+1][1] == "d":
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
                elif self.board[row-1][col-1][1] == "d":
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
                elif self.board[row+1][col+1][1] == "d":
                    moves.append(Movement((startrow,startcol),(row+1,col+1), self.board))
                    break
                else:
                    break
                row+=1
                col+=1
        else: 
            while row+1<=7 and col-1>=0:#Diagonal down left
                if self.board[row+1][col-1] == "--": 
                    moves.append(Movement((startrow,startcol),(row+1,col-1), self.board))
                elif self.board[row+1][col-1][1] == "l":
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
                elif self.board[row-1][col+1][1] == "l":
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
                elif self.board[row-1][col-1][1] == "l":
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
                elif self.board[row+1][col+1][1] == "l":
                    moves.append(Movement((startrow,startcol),(row+1,col+1), self.board))
                    break
                else:
                    break
                row+=1
                col+=1
    def __getKnightMoves(self, row, col, moves):
        if self.whiteToMove: 
            #Top right
            if row-2>=0 and col+1<=7: #2 Up 1 Right
                if self.board[row-2][col+1] == "--" or self.board[row-2][col+1][1]=="d":
                    moves.append(Movement((row,col),(row-2,col+1), self.board))
            if row-1>=0 and col+2<=7: #1 Up 2 Right
                if self.board[row-1][col+2] == "--" or self.board[row-1][col+2][1]=="d":
                    moves.append(Movement((row,col),(row-1,col+2), self.board))
            if row+1<=7 and col+2<=7: #1 Down 2 Right
                if self.board[row+1][col+2] == "--" or self.board[row+1][col+2][1]=="d":
                    moves.append(Movement((row,col),(row+1,col+2), self.board))
            if row+2<=7 and col+1<=7: #2 Down 1 Right
                if self.board[row+2][col+1] == "--" or self.board[row+2][col+1][1]=="d":
                    moves.append(Movement((row,col),(row+2,col+1), self.board))

class Movement:
    ranksToRows = {"1":7, "2":6, "3":5, "4":4,
                   "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v:k for k,v in ranksToRows.items()}
    filesToCols = {"a":0, "b":1, "c":2, "d":3,
                   "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v:k for k,v in filesToCols.items()}
    def __init__(self, start, end, board):
        self.startRow = start[0]
        self.startCol = start[1]
        self.endRow= end[0]
        self.endCol= end[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol* 100 + self.endRow * 10 +self.endCol 

    def __getRankFile(self, r, c):
        return self.colsToFiles[c]+ self.rowsToRanks[r] 

    def getNotation(self):
        return self.__getRankFile(self.startRow, self.startCol) + self.__getRankFile(self.endRow, self.endCol) + str(self) 
    def __eq__(self, other):
        if isinstance(other, Movement):
            return self.moveID == other.moveID
        return False
    
    def __str__(self):
        return "(" +str(self.startRow) + ","+str(self.startCol)  + ")(" + str(self.endRow) + ","+str(self.endCol) + ")"