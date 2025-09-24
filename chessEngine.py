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

        self.whiteToMove = True
        self.moveLog = []

    #takes a move as parameter and execute
    #DO NOT WORK --> castling, pawn promotion, en-passant
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)                               #log of moves
        self.whiteToMove = not self.whiteToMove                 #player swap turn

    #undo last move
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    #all moves considering checks
    def getValidMoves(self):
        return self.getAllPossibleMoves()                    #TEMP(does not consider check for now)

    #all moves without considering checks
    def getAllPossibleMoves(self):
        moves = []
        #moves = [Move((6,4),(4,4),self.board),]             #testing case
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]

                if (turn == "w" and self.whiteToMove) and (turn == "b" and not self.whiteToMove):
                    piece = self.board[row][col][1]

                    if piece == "P":
                        self.getPawnMoves(row, col, moves)
                    elif piece == "R":
                        self.getRookMoves(row, col, moves)

        return moves


    #all chess pieces movement(Not Complete)
    def getPawnMoves(self, row, col, moves):
        pass
    def getRookMoves(self, row, col, moves):
        pass

class Move:
    #maps keys to value
    #key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSQ, endSQ, board):
        self.startRow = startSQ[0]
        self.startCol = startSQ[1]
        self.endRow = endSQ[0]
        self.endCol = endSQ[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
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