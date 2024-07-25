"""
This class is responsible for storing all the information of the current state of the chess game . also responsible for determining the valid moves at the current state.It will also keep a move log.
"""

class GameState():
    def __init__(self) -> None:
        # Board is a 8*8 2d list . each element of list has 2 characters. 
        # first char - represents colour. second char - represents the type of the piece.
        # "--" represents empty spaces on the board.
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        self.moveFunctions = {'p':self.getPawnMoves,'R':self.getRookMoves,'N':self.getKnightMoves,
                            'B':self.getBishopMoves,'Q':self.getQueenMoves,'K':self.getKingMoves}

        self.whitetoMove = True
        self.moveLog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        # self.checkMate = False
        # self.staleMate = False -- naive algorithm
        self.inCheck = False
        self.pins = []
        self.checks = []


       


    """Takes a move as parameter -- executes it (not for casstiling,en passant and pawn promotion.)
    """    
    def makeMove(self,move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # log the move -- to see the history of the game.
        self.whitetoMove = not self.whitetoMove # swap players.
        # update the kings location.
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow,move.endCol)
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow,move.endCol)

    '''
    Undo the last move made.
    '''
    def undoMove(self):
        if len(self.moveLog)!=0: # make sure there is a move to undo.
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whitetoMove = not self.whitetoMove # switch players.  
            # update the king's position if needed.      
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow,move.startCol)
            if move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow,move.startCol)

    def getValidMoves(self):
        moves = []
        self.inCheck,self.pins,self.checks = self.checkForPinsAndChecks()
        if self.whitetoMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks)==1: # onlly 1 check , block check or move king.
                moves = self.getAllPossibleMoves()
                # to block a check you must move a piece into one of the squares between the enemy pieces and king
                check = self.check[0] # check information.
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol] # enemy piece causing the check.
                validSquares = [] # squares that pieces can move to.
                # if knight, must capture knight or move king, other pieces can be blocked.
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow,checkCol)]
                else:
                    for i in range(1,8):
                        validSquare = (kingRow + check[2]*i, kingCol + check[3]*i) # check[2] and check[3] are the check directions.
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol: # once you get to piece and checks.
                            break

                # get rid of any moves that don't block check or move king.
                for i in range(len(moves) -1,-1,-1): # go through backwards when you are removing from a list as iterating.
                    if moves[i].pieceMoved[1] != 'K': # move doesnt move king to it  -- must block or capture.
                        if not (moves[i].endRow,moves[i].endCol) in validSquares: # move doesnt block check or capture piece.
                            moves.remove(moves[i])
            else: # double check, king has to move.
                self.getKingMoves(kingRow,kingCol,moves)
        else: # not in check so all moves are fine.
            moves = self.getAllPossibleMoves()
        
        return moves


    '''
    All moves considering checks
    '''
    # def getValidMoves(self): -- naive algorithm
    #     # 1) generate all possible moves
    #     moves = self.getAllPossibleMoves()
    #     # 2) for each move, make the move
    #     for i in range(len(moves)-1,-1,-1): # when removing from a list go backwards through that list.
    #         self.makeMove(moves[i])
    #     # 3) generate all opponent's move
    #     # 4) for each of your opponent's moves, see if they attack your king
    #         self.whitetoMove = not self.whitetoMove
    #         if self.inCheck():
    #             moves.remove(moves[i])  # 5) if they do attack your king , not a valid move.
    #         self.whitetoMove = not self.whitetoMove
    #         self.undoMove()

    #     if len(moves) == 0: # either checkmate or stalemate.
    #         if self.inCheck():
    #             self.checkMate = True
    #         else:
    #             self.staleMate = True
    #     else:
    #         self.checkMate = False
    #         self.staleMate = False

    #     return moves
    

    '''
    determie if the current player is in check.
    '''
    # def inCheck(self): --- naive algo
    #     if self.whitetoMove:
    #         return self.squareUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
    #     else:
    #         return self.squareUnderAttack(self.blackKingLocation[0],self.blackKingLocation[1])


    
    '''
        determine if the enemy can attack the square.
    '''
    # def squareUnderAttack(self,r,c): // naive algo
    #     self.whitetoMove = not self.whitetoMove # switch to opponens's move.
    #     oppMoves = self.getAllPossibleMoves()
    #     self.whitetoMove = not self.whitetoMove # switch turns back
    #     for move in oppMoves:
    #         if move.endRow == r and move.endCol  == c:# square is under attack
    #             return True
    #     return False
        
             
    



    '''
    All moves withoud considering checks.
    '''
    def getAllPossibleMoves(self):
        moves=[]
        for r in range(len(self.board)): # no. of rows
            for c in range(len(self.board[r])): # no . of columns
                 turn = self.board[r][c][0]
                 if (turn == 'w' and self.whitetoMove) or (turn == 'b' and not self.whitetoMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves) # calls the appropriate funcrtion based on piece type.
        
        return moves     

    '''
    Returns if the player is in check, a list of pins, and a list of checks.
    '''
    def checkForPinsAndChecks(self):
        pins = [] # squares where the allied pinned piece is and direction pinned from.
        checks = [] # squares where enemy is applying a check.
        inCheck = False
        if self.whitetoMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        # check outward from king for pins and checks, keep track of pins.
        directions = ((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = () # resets possible pins
            for i in range(1,8):
                endRow = startRow + d[0]*i
                endCol = startCol + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor:
                        if possiblePin == (): # 1st allied piece could be pinned.
                            possiblePin = (endRow,endCol,d[0],d[1])
                        else: # 2nd allied piece , so no pin or check possible in this direction.
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        # 5 possiblities here in this complex conditional
                        # 1) orthogonally away from king and piece is a rook.
                        # 2) diagonally away from king and piece is a bishop.
                        # 3) 1 square away diagonally from king and piece is a pawn.
                        # 4) any direction and piece is a queen.
                        # 5) any direction 1 square away and piece is a king(this is neccesasry to prevent a kiing move to a square controled by another king.)
                        if (0 <= j <= 7 and type =="R") or  \
                                (4 <= j <= 7 and type =='B') or \
                                (i==1 and type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                                (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == (): # no piece blocking , so check.
                                inCheck = True
                                checks.append((endRow,endCol,d[0],d[1]))
                                break
                            else: # piece blocking so pin
                                pins.append(possiblePin)
                                break
                        else: # enemy piece not applying check.
                            break
                # check for knight checks
                knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
                for m in knightMoves:
                    endRow = startRow + m[0]
                    endCol = startCol + m[1]
                    if 0 <= endRow < 8 and 0 <= endCol < 8:
                        endPiece = self.board[endRow][endCol]
                        if endPiece[0] == enemyColor and endPiece[1] =='N': # enemy knight attacking king.
                            inCheck = True
                            checks.append((endRow,endCol,m[0],m[1]))
                return inCheck,pins,checks

    '''
    Get all the pawn moves for the pawn located at row, col and add these moves to the list
    '''                
    def getPawnMoves(self,r,c,moves):
        if self.whitetoMove: # white pawn moves.
            if self.board[r-1][c] == "--": # 1 pawn square pawn advance.
                moves.append(Move((r,c),(r-1,c),self.board))
                if r == 6 and self.board[r-2][c]=="--": # 2 square pawn advancee.
                    moves.append(Move((r,c),(r-2,c),self.board))
            if c-1 >= 0: # capture to the left.
                if self.board[r-1][c-1][0] == 'b': # enemy piece to capture.
                    moves.append(Move((r,c),(r-1,c-1),self.board))
            
            if c+1 <= 7: # captures to the right.
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r,c),(r-1,c+1),self.board))

        else: # for black pawn moves.
            if self.board[r+1][c] == "--": # 1 square moves
                moves.append(Move((r,c),(r+1,c),self.board))
                if r==1 and self.board[r+2][c] == "--": # 2 square moves.
                    moves.append(Move((r,c),(r+2,c),self.board))
            
            # captures
            if c-1>=0: # capture to left
                if self.board[r+1][c-1][0] == "w":
                    moves.append(Move((r,c),(r+1,c-1),self.board))
            if c+1<=7: # capture to right
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r,c),(r+1,c+1),self.board))

            # make pawn promotion later.


    '''
    Get all the rook moves for the rook located at row, col and add these moves to the list
    '''                
    def getRookMoves(self,r,c,moves):
        directions = ((-1,0),(0,-1),(1,0),(0,1)) # up, left, down,right
        enemyColor = "b" if self.whitetoMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": # empty space valid
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0] == enemyColor: # enemy piece valid
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else: # friendly piece invalid
                        break
                else: # off board
                    break

    '''
    Get all the Knight moves for the Knight located at row, col and add these moves to the list
    '''                
    def getKnightMoves(self,r,c,moves):
        knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        allyColor = "w" if self.whitetoMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: # not an ally piece (empty or enemy piece)
                    moves.append(Move((r,c),(endRow,endCol),self.board))

    '''
    Get all the bishop moves for the bishop located at row, col and add these moves to the list
    '''                
    def getBishopMoves(self,r,c,moves):
        directions = ((-1,-1),(-1,1),(1,-1),(1,1)) # 4 diagonals. 
        enemyColor = "b" if self.whitetoMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol <8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": # empty space valid
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0] == enemyColor: # enemmy piece valid
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else: # friendly piece invalid
                        break
                else: # off board
                    break

    '''
    Get all the queen moves for the queen located at row, col and add these moves to the list
    '''                
    def getQueenMoves(self,r,c,moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)

    '''
    Get all the king moves for the king located at row, col and add these moves to the list
    '''                
    def getKingMoves(self,r,c,moves):
        kingMoves = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        allyColor = "w" if self.whitetoMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: # not an ally piece(empty or enemy piece)
                    moves.append(Move((r,c),(endRow,endCol),self.board))



class Move():
    # maps keys to values
    # key:value
    ranksToRows = {"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowsToRanks = {v:k for k, v in ranksToRows.items()}
    filestoCols = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    colsToFiles = {v:k for k, v in filestoCols.items()}

    def __init__(self,startSq,endSq,board) -> None:
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow *1000 + self.startCol*100 + self.endRow*10 + self.endCol

    '''
    Overriding the equals method
    '''
    def __eq__(self,other):
        if isinstance(other, Move):
            return self.moveID ==  other.moveID
        return False

    def getChessNotation(self):
        # not real chess notation rn .... but will update it later.
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)

    
    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
    
