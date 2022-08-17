"""Class that determines whether some of chess' special moves are legal"""
from squares import Squares

class Castle:

    wRook0 = None
    wRook1 = None
    bRook0 = None
    bRook1 = None

    wRook0Move = ["a1", "d1"]
    wRook1Move = ["h1", "f1"]

    bRook0Move = ["a8", "d8"]
    bRook1Move = ["h8", "f8"]

    @classmethod
    def setWhiteRook(cls, wRook):
        if wRook.name == "wRook0":
            cls.wRook0 = wRook
        else:
            cls.wRook1 = wRook

    @classmethod
    def setBlackRook(cls, bRook):
        if bRook.name == "bRook0":
            cls.bRook0 = bRook
        else:
            cls.bRook1 = bRook

    @classmethod
    def canCastle(cls, king):
        moves = []

        squares = Squares.getSquares()
        if king.isWhite:
            kingCoord = king.square.getCoord()
            # Check if king can castle queenside
            if not cls.wRook0.moved:  # If rook hasn't moved
                for i in range(1, 4):
                    sq = squares[kingCoord[0]-i][kingCoord[1]]
                    if sq.hasPiece():
                        break
                else:
                    moves.append(squares[2][0])  # square on 'c1'

            # Check if king can castle kingside
            if not cls.wRook1.moved:  # If rook hasn't moved
                for i in range(1, 3):
                    sq = squares[kingCoord[0]+i][kingCoord[1]]
                    if sq.hasPiece():
                        break
                else:
                    moves.append(squares[6][0])  # square on 'g1'
        else:
            kingCoord = king.square.getCoord()
            # Check if king can castle queenside
            if not cls.bRook0.moved:  # If rook hasn't moved
                for i in range(1, 4):
                    sq = squares[kingCoord[0]-i][kingCoord[1]]
                    if sq.hasPiece():
                        break
                else:
                    moves.append(squares[2][7])  # square on 'c8'

            # Check if king can castle kingside
            if not cls.bRook1.moved:  # If rook hasn't moved
                for i in range(1, 3):
                    sq = squares[kingCoord[0]+i][kingCoord[1]]
                    if sq.hasPiece():
                        break
                else:
                    moves.append(squares[6][7])  # square on 'g8'

        return moves


class EnPassant:

    def __init__(cls):
        pass