
class TicTacToe:
    __player  = "X"
    __opponent = "O"
    def __init__(self, board):
        self.__board = board

    def evaluate_game_state(self,player):
        if player == "X":
            opponent = "O"
        else:
            opponent = "X"
        for row in range(3):
            if self.__board[row][0]==self.__board[row][1] and self.__board[row][1] == self.__board[row][2]:
                if self.__board[row][0] == player:
                    return 10
                elif self.__board[row][0] == opponent:
                    return -10
        for col in range(3):
            if self.__board[0][col]==self.__board[1][col] and self.__board[1][col] == self.__board[2][col]:
                if self.__board[0][col] == player:
                    return 10
                elif self.__board[0][col] == opponent:
                    return -10

        if self.__board[0][0] == self.__board[1][1] and self.__board[1][1] == self.__board[2][2]:
            if self.__board[0][0] == player:
                return 10
            elif self.__board[0][0] == opponent:
                return -10
        
        if self.__board[0][2] == self.__board[1][1] and self.__board[1][1] == self.__board[2][0]:
            if self.__board[0][2] == player:
                return 10
            elif self.__board[0][2] == opponent:
                return -10
        
        return 0
    
    def game_not_ended(self):
        for i in range(3):
            for j in range(3):
                if self.__board[i][j] == '_':
                    return True
        return False

    def minimax(self, depth, isMax, alpha, beta,player):
        score = self.evaluate_game_state(player)
        #If Maximizer or Minimizer has won
        if score == 10 or score == -10:
            return score
        
        if not self.game_not_ended():
            return 0
        
        if isMax:
            best = -1000
            for i in range(3):
                for j in range(3):
                    if self.__board[i][j] == "_":
                        self.__board[i][j] = self.__player
                        val= max(best, self.minimax(depth+1, not isMax,alpha,beta,player))
                        best = max(best, val)
                        alpha = max(alpha,best)
                        self.__board[i][j] = "_"
                        if beta <= alpha:
                            break
            return best
        else:
            best = 1000
            for i in range(3):
                for j in range(3):
                    if self.__board[i][j] == "_":
                        self.__board[i][j] = self.__opponent
                        val= min(best, self.minimax(depth+1, not isMax, alpha, beta,player))
                        best = min(best, val)
                        alpha = min(alpha,best)
                        self.__board[i][j] = "_"
                        if beta <= alpha:
                            break
            return best
    
    def find_best_move(self,player):
        best_value = -1000
        best_move = (None, None)
        for i in range(3):
            for j in range(3):
                if self.__board[i][j] == '_':
                    self.__board[i][j] = player
                    move_value = self.minimax( 0, False, -1000, 1000, player)
                    self.__board[i][j] = '_'
                    if move_value > best_value:
                        best_move = (i, j)
                        best_value = move_value
        print("The value of the best Move is: ", best_value)
        return best_move


board = [
    [ 'X', 'O', 'X' ],
    [ 'O', 'X', 'O' ],
    [ '_', '_', '_' ]
]
tictacttoe = TicTacToe(board)

best_move = tictacttoe.find_best_move("O")
print(best_move[0]," ",  best_move[1])