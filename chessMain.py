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
def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

# draw squares on the board
def drawBoard(screen):
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

def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))

    gs = chessEngine.GameState()
    loadImages()

    sqSelected = ()              #selects empty square, last click of user
    playerClicks = []            #playerclick tracker

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:                #exit game
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
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
                    #------debug------
                    print(move.getChessNotation())
                    gs.makeMove(move)
                    sqSelected = ()
                    playerClicks = []


        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        pg.display.flip()


if __name__ == "__main__":
    main()