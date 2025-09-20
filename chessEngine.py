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