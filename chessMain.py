"""
main driver file
-> takes user input
-> displays current GameState object
"""

import pygame as pg
import chessEngine

WIDTH = HEIGHT = 400
DIMENSION = 8
SQ_SIZE = WIDTH // DIMENSION
MAX_FPS = 15
IMAGES = {}

#loads all images once
def loadImages():
    pieces = ["wP","wR", "wN", "wB", "wQ", "wK","bP", "bR", "bN", "bQ", "bK", "bB"]

    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

#graphics for the current game state
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)

# draw squares on the board
def drawBoard(screen):
    global colors
    colors = [pg.Color("white"), pg.Color("gray")]

    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row+col)%2)]
            pg.draw.rect(screen, color, pg.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

# draw pieces on those square
def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]

            if piece != "--":
                screen.blit(IMAGES[piece], pg.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

#highlights the squares that can be selected by the user
def highlightSquares(screen, gs, validMoves,sqSelected):
    if sqSelected != ():
        row, col = sqSelected
        if gs.board[row][col][0] == ("w" if gs.whiteToMove else "b"):
            #selected square
            s = pg.Surface((SQ_SIZE,SQ_SIZE))
            s.set_alpha(100)                               #transparancy value
            s.fill(pg.Color('blue'))
            screen.blit(s, (col*SQ_SIZE, row*SQ_SIZE))
            #highlight valid moves
            s.fill(pg.Color('yellow'))
            for move in validMoves:
                if move.startRow == row and move.startCol == col:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

#animations
def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount+1):
        row, col = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)

        color = colors[(move.endRow+move.endCol)%2]
        endSquare = pg.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pg.draw.rect(screen, color, endSquare)

        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], pg.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pg.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = pg.font.SysFont("Helvicta", 32, True, False)
    textObject = font.render(text, 0, pg.Color("Gray"))
    textLocation = pg.Rect(0,0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, pg.Color("Black"))
    screen.blit(textObject, textLocation.move(2,2))

def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    gs = chessEngine.GameState()

    validMoves = gs.getValidMoves()
    moveMade = False                       #flag move made
    animate = False                         #flag for animation

    loadImages()

    sqSelected = ()              #selects empty square, last click of user
    playerClicks = []            #playerclick tracker
    gameOver = False

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:                #exit game
                running = False
            #mouse handler
            elif event.type == pg.MOUSEBUTTONDOWN:   #mouse click gameplay
                if not gameOver:
                    location = pg.mouse.get_pos()        #(x,y) of mouse
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE

                    if sqSelected == (row, col):         #undo action
                        sqSelected = ()
                        playerClicks = []
                    else:                                #update action
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)

                    if len(playerClicks) == 2:
                        move = chessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:                               #fix for 2-click issue
                            playerClicks = [sqSelected]
            #key handler
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_z:             #undo a move
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if event.key == pg.K_r:             #reset the board
                    gs = chessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs, validMoves, sqSelected)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Black wins by checkmate")
            else:
                drawText(screen, "White wins by checkmate")
        elif gs.staleMate:
            gameOver = True
            drawText(screen, "stalemate")

        clock.tick(MAX_FPS)
        pg.display.flip()



if __name__ == "__main__":
    main()