import sys 

UP_FORBIDDEN = {0, 1, 2}  
RIGHT_FORBIDDEN = {2, 5, 8} 
DOWN_FORBIDDEN = {6, 7, 8} 
LEFT_FORBIDDEN = {0, 3, 6} 

numberOfExpandedNodes = 0
check08 = 0
check09 = 0
check18 = 0
check19 = 0
check71 = 0
check72 = 0
check81 = 0
check82 = 0  

class Game:
    def __init__(self, board, agent):
        self.initializeGame(board, agent) 

    def initializeGame(self, board, agent):
        self.currentState = board
        self.player = agent
        self.opponent = 3 - self.player 
        self.depth = 0
        self.lastMove = {1: None, 2: None} 
        self.repeated = {1: False, 2: False} 
        self.occupied = {1: False, 2: False} 
        self.alpha = -2
        self.beta = 2

    def isTerminal(self):
        
        # agent 1 reaches the goal
        if self.currentState[0] == 1 and self.currentState[1] == 2:
            return 1
        
        if self.currentState[1] == 1 and self.currentState[0] == 2:
            return 1
        
        # agent 2 reaches the goal
        if self.currentState[7] == 8 and self.currentState[8] == 9:
            return 2

        if self.currentState[8] == 8 and self.currentState[7] == 9:
            return 2 
        
    def maximize(self, depth, alpha, beta):

        max_value = -2

        result = self.isTerminal()

        if result == self.player:
            return 1
        elif result == self.opponent:
            return -1 
        
        if depth == 10: 
            return 0 
            
        moves = self.possibleMoves(self.player)
        if len(moves) == 0:
            return -1
        for move in moves:
            self.doMove(move)
            
            if self.repeated[self.player] or self.occupied[self.player]: 
                value = -1 
            else:
                value = self.minimize(depth + 1, alpha, beta)  
            if value > max_value:
                max_value = value 
            #prunning 
            if max_value >= beta:
                return max_value 
            alpha = max(alpha, max_value) 
            # undo Move
            self.undoMove(move)  

        return max_value 
    
    def minimize(self, depth, alpha, beta): 
        min_value = 2
        result = self.isTerminal()

        if result == self.player:
            return 1
        elif result == self.opponent:
            return -1 
        
        if depth == 10: 
            return 0
        moves = self.possibleMoves(self.opponent) 
        if len(moves) == 0:
            return 1 
        for move in moves:
            self.doMove(move)
            
            if self.repeated[self.opponent] or self.occupied[self.opponent]:
                value = 1
            else:
                value = self.maximize(depth + 1, alpha, beta) 
            if value < min_value:
                min_value = value 
            # prunnig
            if min_value <= alpha: 
                return min_value 
            beta = min(beta, min_value) 
            # undo Move
            self.undoMove(move) 

        return min_value 
    
    def undoMove(self, move):  
        self.currentState[move[2]], self.currentState[move[2]+move[3]] = self.currentState[move[2]+move[3]], self.currentState[move[2]]
        self.repeated[move[0]] = False
        self.occupied[move[0]] = False  

    def doMove(self, move): 

        self.currentState[move[2]], self.currentState[move[2]+move[3]] = self.currentState[move[2]+move[3]], self.currentState[move[2]] 

        if self.lastMove[move[0]] == self.reverseMove(move):
            self.repeated[move[0]] = True 
        else: 
            self.repeated[move[0]] = False 
        
        self.checkOccupation() 

        self.lastMove[move[0]] = move 
    
    def checkOccupation(self):  
        global check08, check09, check18, check19, check71, check72, check81, check82 
        index8 = self.currentState.index(8)  
        index9 = self.currentState.index(9) 
        if index8 == 0:
            check08 +=1
        else: 
            check08 = 0
        if index8 == 1:
            check18 +=1
        else: 
            check18 = 0 
        if index9 == 0:
            check09 +=1
        else: 
            check09 = 0
        if index9 == 1: 
            check19 +=1
        else: 
            check19 = 0 
        index1 = self.currentState.index(1) 
        index2 = self.currentState.index(2) 
        if index1 == 7:
            check71 +=1
        else: 
            check71 = 0
        if index1 == 8:
            check81 +=1
        else: 
            check81 = 0
        if index2 == 7:
            check72 +=1
        else: 
            check72 = 0
        if index2 == 8:
            check82 +=1
        else: 
            check82 = 0

        if check71 > 4 or check81 > 4 or check72 > 4 or check82 > 4:
            self.occupied[1] = True
        else: 
            self.occupied[1] = False

        if check08 > 4 or check18 > 4 or check09 > 4 or check19 > 4:
            self.occupied[2] = True
        else: 
            self.occupied[2] = False 
    
    def reverseMove(self, move):
        reversedMove = [move[0],move[1], move[2] + move[3], -move[3]]  
        return reversedMove 

    def possibleMoves(self, turn):
        global numberOfExpandedNodes 
        allowedMoves = [] 
        if turn == 1:
            index1 = self.currentState.index(1) 
            index2 = self.currentState.index(2)

            if index1 not in UP_FORBIDDEN: 
                if self.currentState[index1-3] == 0: 
                    allowedMoves.append([1,1,index1,-3]) 
                    numberOfExpandedNodes += 1
            if index1 not in RIGHT_FORBIDDEN:
                if self.currentState[index1+1] == 0: 
                    allowedMoves.append([1,1,index1,1]) 
                    numberOfExpandedNodes += 1
            if index1 not in DOWN_FORBIDDEN:
                if self.currentState[index1+3] == 0: 
                    allowedMoves.append([1,1,index1,3]) 
                    numberOfExpandedNodes += 1
            if index1 not in LEFT_FORBIDDEN:
                if self.currentState[index1-1] == 0: 
                    allowedMoves.append([1,1,index1,-1]) 
                    numberOfExpandedNodes += 1
            if index2 not in UP_FORBIDDEN: 
                if self.currentState[index2-3] == 0: 
                    allowedMoves.append([1,2,index2,-3])
                    numberOfExpandedNodes += 1
            if index2 not in RIGHT_FORBIDDEN:
                if self.currentState[index2+1] == 0: 
                    allowedMoves.append([1,2,index2,1]) 
                    numberOfExpandedNodes += 1
            if index2 not in DOWN_FORBIDDEN:
                if self.currentState[index2+3] == 0: 
                    allowedMoves.append([1,2,index2,3]) 
                    numberOfExpandedNodes += 1
            if index2 not in LEFT_FORBIDDEN:
                if self.currentState[index2-1] == 0:  
                    allowedMoves.append([1,2,index2,-1])  
                    numberOfExpandedNodes += 1
        
        else:
            index8 = self.currentState.index(8) 
            index9 = self.currentState.index(9)
            
            if index8 not in UP_FORBIDDEN: 
                if self.currentState[index8-3] == 0: 
                    allowedMoves.append([2,8,index8,-3])
                    numberOfExpandedNodes += 1
            if index8 not in RIGHT_FORBIDDEN:
                if self.currentState[index8+1] == 0: 
                    allowedMoves.append([2,8,index8,1])
                    numberOfExpandedNodes += 1
            if index8 not in DOWN_FORBIDDEN:
                if self.currentState[index8+3] == 0: 
                    allowedMoves.append([2,8,index8,3]) 
                    numberOfExpandedNodes += 1
            if index8 not in LEFT_FORBIDDEN:
                if self.currentState[index8-1] == 0: 
                    allowedMoves.append([2,8,index8,-1])
                    numberOfExpandedNodes += 1
            if index9 not in UP_FORBIDDEN: 
                if self.currentState[index9-3] == 0: 
                    allowedMoves.append([2,9,index9,-3])
                    numberOfExpandedNodes += 1
            if index9 not in RIGHT_FORBIDDEN:
                if self.currentState[index9+1] == 0:
                    allowedMoves.append([2,9,index9,1])
                    numberOfExpandedNodes += 1
            if index9 not in DOWN_FORBIDDEN:
                if self.currentState[index9+3] == 0: 
                    allowedMoves.append([2,9,index9,3])
                    numberOfExpandedNodes += 1
            if index9 not in LEFT_FORBIDDEN:
                if self.currentState[index9-1] == 0: 
                    allowedMoves.append([2,9,index9,-1])  
                    numberOfExpandedNodes += 1     

        return allowedMoves

    def play(self): 
        global numberOfExpandedNodes 
        result = self.maximize(self.depth, self.alpha, self.beta) 
        return result 
    
# main 

with open(sys.argv[2]) as f: 
    contents = f.read()
board = [int(val) for val in contents.split()] 
agent = int(sys.argv[1] ) 
game = Game(board, agent)

file = open(sys.argv[3], 'w') 
file.write(f"Minimax value of root node: {str(game.play())}") 
file.write('\n') 
file.write(f"Number of expanded nodes: {str(numberOfExpandedNodes)}")  
file.write('\n')

file.close()   
