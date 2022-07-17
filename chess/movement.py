"""Module that holds PieceMovements class, which is used to determine
squares available to a piece"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from board import Square


class PieceMovements:
    """Class that determines squares available to a piece"""

    def __init__(self):
        # BoardScene will create the squares and call setSquares() to 
        # give PieceMovements a reference to squares as well.
        self.squares = None

    def setSquares(self, squares):
        self.squares = squares

    def getSquares(self, names: str):
        # If type not string it must be a list of square names
        squares = []
        for name in names:
            squares.append(self.squares[name])
        return squares

    def getPossibleSquares(self, square: Square) -> list:
        """Called when a square is clicked. Looks at the piece on the 
        square and returns a list of possible squares it can move to."""
        pieceOnSquare = square.getPiece()
        piece, color = pieceOnSquare[1:], pieceOnSquare[:1]
        if pieceOnSquare is None:
            return

        if piece == "Pawn" and color == "w":
            squares = self.getPossiblePawnSquares(square)
        elif piece == "Pawn" and color == "b":
            squares = self.getPossiblePawnSquares(square, isWhite=False)
        elif piece == "Rook" and color == "w":
            squares = self.getPossibleRookMoves(square)
        elif piece == "Rook" and color == "b":
            squares = self.getPossibleRookMoves(square, isWhite=False)
        elif piece == "Knight" and color == "w":
            squares = self.getPossibleKnightMoves(square)
        elif piece == "Knight" and color == "b":
            squares = self.getPossibleKnightMoves(square, isWhite=False)
        elif piece == "Bishop" and color == "w":
            squares = self.getPossibleBishopMoves(square)
        elif piece == "Bishop" and color == "b":
            squares = self.getPossibleBishopMoves(square, isWhite=False)
        elif piece == "Queen" and color == "w":
            squares = self.getPossibleQueenMoves(square)
        elif piece == "Queen" and color == "b":
            squares = self.getPossibleQueenMoves(square, isWhite=False)
        elif piece == "King" and color == "w":
            squares = self.getPossibleKingMoves(square)
        elif piece == "King" and color == "b":
            squares = self.getPossibleKingMoves(square, isWhite=False)

        return squares
    
    def getPossiblePawnSquares(self, square: Square, isWhite = True):
        """Returns list of all possible moves for a pawn starting on square"""
        l, n = square.getName()
        n = int(n)
        squares = []
        
        # White and black pawns move in opposite directions
        if isWhite:
            one, two, s_rank = 1, 2, 2
        else:
            one , two, s_rank = -1, -2, 7

        if n == s_rank:
            for new_n in range(n+one, n+two+one, one): 
                sq = self.squares[l + str(new_n)]
                if sq.hasPiece():
                    break

                squares.append(sq)
        else:
            # If not on starting rank, pawn can only move forward
            # one square, so check if it is occupied
            sq = self.squares[l + str(n+one)]
            if not sq.hasPiece():
                squares.append(sq)

        # Check if there are enemy pieces on the forward diagonal
        sqLeftD = self.squares.get(chr(ord(l)-1)+str(n+one))
        sqRightD = self.squares.get(chr(ord(l)+1)+str(n+one))
        # Checking the diagonal square to the right
        try:
            if ((isWhite and sqRightD.hasBlackPiece()) 
                or ((not isWhite) and sqRightD.hasWhitePiece())):
                squares.append(sqRightD)
        # If there is an AttributeError it means square does not exist
        # happens if we're on the 'a' or 'h' files
        except AttributeError:
            pass
        # Checking the diagonal square to the left
        try:
            if ((isWhite and sqLeftD.hasBlackPiece()) 
                or ((not isWhite) and sqLeftD.hasWhitePiece())):
                squares.append(sqLeftD)
        except AttributeError:
            pass

        return squares

    def getPossibleRookMoves(self, square: Square, isWhite = True):
        """Returns list of all possible moves for a rook starting on square"""
        # rook moves to the left
        l, n = square.getName()
        n = int(n)
        # code point for letter
        cp = ord(l)
        squares = []

        # Get all squares to the left of the rook
        # chr(97) is 'a' which is the last file to the left
        for new_cp in range(cp-1, 96, -1):
            new_l = chr(new_cp)
            sq = self.squares[new_l + str(n)]
            # Check if square is occupied
            if isWhite:
                if sq.hasWhitePiece():
                    break
                if sq.hasBlackPiece():
                    squares.append(sq)
                    break
            else:
                if sq.hasWhitePiece():
                    squares.append(sq)
                    break
                if sq.hasBlackPiece():
                    break
            squares.append(sq)

        # Get all squares to the right
        # chr(104) is 'h', the last file to the right
        for new_cp in range(cp+1, 105):
            new_l = chr(new_cp)
            sq = self.squares[new_l + str(n)]
            if isWhite:
                if sq.hasWhitePiece():
                    break
                if sq.hasBlackPiece():
                    squares.append(sq)
                    break
            else:
                if sq.hasWhitePiece():
                    squares.append(sq)
                    break
                if sq.hasBlackPiece():
                    break
            squares.append(sq)

        # Get all squares upwards
        # 8 is the top rank
        for new_n in range(n+1, 9):
            sq = self.squares[l + str(new_n)]
            if isWhite:
                if sq.hasWhitePiece():
                    break
                if sq.hasBlackPiece():
                    squares.append(sq)
                    break
            else:
                if sq.hasWhitePiece():
                    squares.append(sq)
                    break
                if sq.hasBlackPiece():
                    break

            squares.append(sq)

        # Get all squares downwards
        # 1 is the bottom rank
        for new_n in range(n-1, 0, -1):
            sq = self.squares[l + str(new_n)]
            if isWhite:
                if sq.hasWhitePiece():
                    break
                if sq.hasBlackPiece():
                    squares.append(sq)
                    break
            else:
                if sq.hasWhitePiece():
                    squares.append(sq)
                    break
                if sq.hasBlackPiece():
                    break
            
            squares.append(sq)

        return squares

    def getPossibleKnightMoves(self, square: Square, isWhite = True):
        """Get all possible moves for a knight"""
        l, n = square.getName()
        n = int(n)
        cp = ord(l)
        squares = []

        # At most eight possible moves for a knight, just check them all.
        sqs = (
            self.squares.get(f"{chr(cp+1)}{n+2}"),
            self.squares.get(f"{chr(cp+2)}{n+1}"),
            self.squares.get(f"{chr(cp+2)}{n-1}"),
            self.squares.get(f"{chr(cp+1)}{n-2}"),
            self.squares.get(f"{chr(cp-1)}{n+2}"),
            self.squares.get(f"{chr(cp-2)}{n+1}"),
            self.squares.get(f"{chr(cp-2)}{n-1}"),
            self.squares.get(f"{chr(cp-1)}{n-2}"))

        for sq in sqs:
            if sq is None:
                continue
            if not sq.hasPiece():
                squares.append(sq)
            else:
                if isWhite:
                    if sq.hasBlackPiece():
                        squares.append(sq)
                else:
                    if sq.hasWhitePiece():
                        squares.append(sq)
        
        return squares

    def getPossibleBishopMoves(self, square: Square, isWhite = True):
        """Get all possible bishop moves"""
        l, n = square.getName()
        n = int(n)
        cp = ord(l)
        squares = []

        # Each tuple represents a diagonal and how the letter and number of
        # a square changes on that diagonal. (-1, 1) says go back one
        # letter and go up one number (eg. e4->d5), and that is the diagonal
        # pointing to the top left
        changes = ((-1, 1), (1, 1), (1, -1), (-1, -1))

        for c in changes:
            for i in range(1, 8):
                sq = self.squares.get(f"{chr(cp+c[0]*i)}{n+c[1]*i}")
                if sq is None:
                    break
                else:
                    if not sq.hasPiece():
                        squares.append(sq)
                    else:
                        if isWhite and sq.hasBlackPiece():
                            squares.append(sq)
                        else:
                            if (not isWhite) and sq.hasWhitePiece():
                                squares.append(sq)
                        break
        return squares

    def getPossibleQueenMoves(self, square: Square, isWhite = True):
        """Get all possible queen moves"""
        bishopMoves = self.getPossibleBishopMoves(square, isWhite=isWhite)
        rookMoves = self.getPossibleRookMoves(square, isWhite=isWhite)
        bishopMoves.extend(rookMoves)
        return bishopMoves

    def getPossibleKingMoves(self, square: Square, isWhite = True):
        """Get all possible king moves"""
        l, n = square.getName()
        n = int(n)
        cp = ord(l)
        squares = []

        # King has a maximum of eight moves at any time, check them all
        sqs = (
            self.squares.get(f"{chr(cp)}{n+1}"),
            self.squares.get(f"{chr(cp+1)}{n+1}"),
            self.squares.get(f"{chr(cp+1)}{n}"),
            self.squares.get(f"{chr(cp+1)}{n-1}"),
            self.squares.get(f"{chr(cp)}{n-1}"),
            self.squares.get(f"{chr(cp-1)}{n-1}"),
            self.squares.get(f"{chr(cp-1)}{n}"),
            self.squares.get(f"{chr(cp-1)}{n+1}"))

        for sq in sqs:
            if sq is None:
                continue
            if not sq.hasPiece():
                squares.append(sq)
            else:
                if isWhite:
                    if sq.hasBlackPiece():
                        squares.append(sq)
                else:
                    if sq.hasWhitePiece():
                        squares.append(sq)
        
        return squares