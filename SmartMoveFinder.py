import random

pieceScore = {"K":0, "Q":10, "R":5, "B":3, "N":3, "P":1 }
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2

#random moves algorithm
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

#greedy algorithm + minimax
def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1

    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()

        if gs.staleMate:
            opponentMaxScore = STALEMATE
        elif gs.checkMate:
            opponentMaxScore = -CHECKMATE
        else:
            opponentMaxScore = -CHECKMATE
            for opponentMove in opponentsMoves:
                gs.makeMove(opponentMove)
                gs.getValidMoves()

                if gs.checkMate:
                    score = CHECKMATE
                elif gs.staleMate:
                    score = STALEMATE
                else:
                    score = - turnMultiplier * scoreMaterial(gs.board)
                if score > opponentMaxScore:
                    opponentMaxScore = score
                    #bestMove = playerMove
                gs.undoMove()

        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()

    return bestPlayerMove

#minmax algorithm
def findBestMoveMinMax(gs, validMoves):
    global nextMove
    nextMove = None
    findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    return nextMove

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)

    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMove = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMove, depth-1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            score = findMoveMinMax(gs, validMoves, depth-1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore


def scoreBoard(gs):
    #positive score for white and negative score for black
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE                   #white wins by checkmate
        else:
            return CHECKMATE                    #black wins by checkmate
    elif gs.staleMate:
        return STALEMATE                             #stalemate

    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == "w":
                score += pieceScore[square[1]]
            elif square[0] == "b":
                score -= pieceScore[square[1]]

    return score



def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += pieceScore[square[1]]
            elif square[0] == "b":
                score -= pieceScore[square[1]]

    return score
