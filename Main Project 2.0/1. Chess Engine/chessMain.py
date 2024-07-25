"""
This is our main driver file. It will be responsible for handling user input and displaying the current GameState object.
"""
import chessEngine
import pygame as p
from chess import engine
import voiceRecognition 

WIDTH = HEIGHT = 512 # 400 IS another option.
DIMENSION = 8 # dimension of the chess board.
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15 # for animations.
IMAGES = {}

"""
Initialize a global directory of images. This will be called exactly once in the main.
"""

def loadImages():
    pieces = ['wp','wR','wN','wB','wK','wQ','bp','bR','bN','bB','bK','bQ']

    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece +".png"),(SQ_SIZE,SQ_SIZE))

        # we can access the image by saying IMAGES['wp']

"""
This is the main code. Handles input -- updating graphics.
"""
def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # flag variable for when a move is made.

    loadImages() # only once -- before the while loop.
    running = True
    sqSelected = () # no square is selected initially - keep tracks of the last click of the user.
    playerClicks = [] # keep tracks of players clicks.

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handle
            elif e.type == p.MOUSEBUTTONDOWN: # checks whether mouse is pressed.
                location = p.mouse.get_pos() # (x,y) location of mouse.
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                
                if sqSelected == (row,col): # the user clicked the same sq 0--- twice.
                    sqSelected = () # deselect
                    playerClicksq = [] # clear player clicks.
                else:    
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected) # apend for both clicks.
                if len(playerClicks ) == 2:
                    move = chessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move) 
                        moveMade = True 
                        sqSelected = () # resets the user clicks.
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]
            # key handle
            elif e.type == p.KEYDOWN:
                    if e.key == p.K_z: # undo when 'z' is pressed.
                        gs.undoMove()
                        moveMade = True
        
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen,gs)

        clock.tick(MAX_FPS)
        p.display.flip()

"""
For all the graphics within a current Game state.
"""

def drawGameState(screen,gs):
    drawBoard(screen) # draws squares on the board.

    drawPieces(screen,gs.board) # draw pieces on square.

"""
Draws squares on the board. 
"""
def drawBoard(screen):
    colors = [p.Color("white"),p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

"""
Draw the pieces on the board using current GameState.board
"""
def drawPieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": # not a empty square.
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))




if __name__ == "__main__":
    main()