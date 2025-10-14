"""
-> stores all info of current state
-> checks for valid moves
-> keeps move log
"""
import numpy as np

class GameState:
    def __init__(self):
        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],       #8x8 board
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],       #1st character color = b,w
            ["--", "--", "--", "--", "--", "--", "--", "--"],       #2nd character piece = P,R,N,B,Q,K
            ["--", "--", "--", "--", "--", "--", "--", "--"],       #empty space = --
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ])

        self.moveFunctions = {'P': self.getPawnMoves,                #dictonary for the pieces
                              'R': self.getRookMoves,
                              'N': self.getKnightMoves,
                              'B': self.getBishopMoves,
                              'Q': self.getQueenMoves,
                              'K': self.getKingMoves }
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.enPassantPossible = ()             #cords of square

    #takes a move as a parameter and execute
    #DO NOT WORK --> castling, pawn promotion, en-passant
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)                               #log of moves
        self.whiteToMove = not self.whiteToMove                 #player swap turn
        #update king location
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        #pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        #enpassant move
        if move.isEnPassantMove:
            self.board[move.startRow][move.endCol] = "--"
        #2 square enpassant
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
            self.enPassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enPassantPossible = ()

    #undo last move
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            # update king position
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

            #undo Enpassant
            if move.isEnPassantMove:
                self.board[move.endRow][move.endCol] = "--"                         #leave the landing square blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enPassantPossible = (move.endRow, move.endCol)
            #undo 2 square enpassant
            if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
                self.enPassantPossible = ()


    #all moves considering checks
    def getValidMoves(self):
        tempEnpassantPossible = self.enPassantPossible
        moves = self.getAllPossibleMoves()                   #genarates all possible moves

        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        if len(moves) == 0:                 #checkmate or stalemate
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        self.enPassantPossible = tempEnpassantPossible
        return moves

    #check if the current player is in check
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])


    #check if the enemy can attack
    def squareUnderAttack(self, row, col):
        self.whiteToMove = not self.whiteToMove                 # opponent's turn
        oppoMoves = self.getAllPossibleMoves()                  # generates all possible moves for the opponent
        self.whiteToMove = not self.whiteToMove                 #switch back turn

        for move in oppoMoves:
            if move.endRow == row and move.endCol == col:       #square under attack
                #self.whiteToMove = not self.whiteToMove        #-----BUG-----
                return True
        return False


    #all moves without considering checks
    def getAllPossibleMoves(self):
        moves = []
        #moves = [Move((6,4),(4,4),self.board),]             #testing case
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]

                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[row][col][1]

                    self.moveFunctions[piece](row, col, moves)

        return moves


    #all chess pieces movement(Not Complete)
    def getPawnMoves(self, row, col, moves):
        #white's move
        if self.whiteToMove:
            if self.board[row-1][col] == "--":                                             #1 square move
                moves.append(Move((row, col), (row-1, col), self.board))
                if row == 6 and self.board[row-2][col] == "--":                            #2 square move
                    moves.append(Move((row, col), (row-2, col), self.board))

            if col-1 >= 0:                                                                 #left capture
                if self.board[row-1][col-1][0] == 'b':
                    moves.append(Move((row, col), (row-1, col-1), self.board))
                elif (row -1, col-1) == self.enPassantPossible:
                    moves.append(Move((row, col), (row-1, col-1), self.board, isEnpassantMove=True))
            if col+1 <= 7:
                if self.board[row-1][col+1][0] == 'b':                                      #right capture
                    moves.append(Move((row, col), (row-1, col+1), self.board))
                elif (row -1, col+1) == self.enPassantPossible:
                    moves.append(Move((row, col), (row-1, col+1), self.board, isEnpassantMove=True))
        #black's move
        else:
            if self.board[row+1][col] == "--":                                             #1 square move
                moves.append(Move((row, col), (row+1, col), self.board))
                if row == 1 and self.board[row+2][col] == "--":                            #2 square move
                    moves.append(Move((row, col), (row+2, col), self.board))

            if col-1 >= 0:                                                                 #left capture
                if self.board[row+1][col-1][0] == 'w':
                    moves.append(Move((row, col), (row+1, col-1), self.board))
                elif (row +1, col-1) == self.enPassantPossible:
                    moves.append(Move((row, col), (row+1, col-1), self.board, isEnpassantMove=True))
            if col+1 <= 7:
                if self.board[row+1][col+1][0] == 'w':                                      #right capture
                    moves.append(Move((row, col), (row+1, col+1), self.board))
                elif (row +1, col+1) == self.enPassantPossible:
                    moves.append(Move((row, col), (row+1, col+1), self.board, isEnpassantMove=True))


    def getRookMoves(self, row, col, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        if self.whiteToMove:
            enemyColor = 'b'
        else:
            enemyColor = 'w'

        for d in directions:
            for i in range(1,8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:                     #on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":                                    #empty space
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:                         #enemy space
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else:                                                   #friendly space
                        break
                else:                                                       #off board
                    break


    def getKnightMoves(self, row, col, moves):
        knightMoves = ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1))
        if self.whiteToMove:
            allyColor = 'w'
        else:
            allyColor = 'b'

        for m in knightMoves:
            endRow = row + m[0]
            endCol = col + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:                 #on board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((row, col), (endRow, endCol), self.board))

    def getBishopMoves(self, row, col, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        if self.whiteToMove:
            enemyColor = 'b'
        else:
            enemyColor = 'w'

        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:                        # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # empty space
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # enemy space
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else:  # friendly space
                        break
                else:  # off board
                    break

    def getQueenMoves(self, row, col, moves):
        self.getRookMoves(row, col, moves)                  #for horizontal and vertical moves
        self.getBishopMoves(row, col, moves)                #for diagonal moves

    def getKingMoves(self, row, col, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        if self.whiteToMove:
            allyColor = 'w'
        else:
            allyColor = 'b'

        for i in range(8):
            endRow = row + kingMoves[i][0]
            endCol = col + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:                # on board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((row, col), (endRow, endCol), self.board))

class Move:
    #maps keys to value
    #key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSQ, endSQ, board, isEnpassantMove=False):
        self.startRow = startSQ[0]
        self.startCol = startSQ[1]
        self.endRow = endSQ[0]
        self.endCol = endSQ[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = (self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7)
        #self.isEnPassantMove = (self.pieceMoved[1] == 'P' and (self.endRow, self.endCol) == enpassantPossible)
        self.isEnPassantMove = isEnpassantMove
        if self.isEnPassantMove:
            self.pieceCaptured = "wP" if self.pieceMoved == "bP" else "bP"
        self.moveId = (self.startRow * 1000) + (self.startCol * 100) + (self.endRow * 10) + self.endCol
        print(self.moveId)                    #testing for move id

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveId == other.moveId
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, row, col):
        return  self.colsToFiles[col] + self.rowsToRanks[row]
