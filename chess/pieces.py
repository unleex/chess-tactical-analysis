"""This module defines classes for every type of chess piece"""
class Board:
    """Provides an easy way for a Piece to access the board state of a game
    by getting the squares. Centralizes access so that 16 Piece objects do
    not each have to hold a reference to squares."""
    SQUARES = None

    @classmethod
    def setSquares(cls, squares):
        cls.SQUARES = squares

    @classmethod
    def getSquares(cls):
        return cls.SQUARES


class Piece():
    """Base class for all pieces"""

    def __init__(self, isWhite):
        self.isWhite = isWhite
        self.square = None
        self.controls = []
    
    def getPossibleSquares(self):
        ...

    def setSquare(self, square):
        self.square = square

    def updateSquares(self):
        ...


class King(Piece):
    pass

class Queen(Piece):
    pass

class Pawn(Piece):
    w_id = 0
    b_id = 0

    def __init__(self, isWhite):
        super().__init__(isWhite)
        if isWhite:
            self.name = "wPawn" + str(Pawn.w_id)
            Pawn.w_id += 1
        else:
            self.name = "bPawn" + str(Pawn.b_id)
            Pawn.b_id += 1

        self.controlledSquares = []
        self.moves = []

    def updateSquares(self):
        """Gets the squares this pawn can move to and updates the state
        of any squares that this pawn affects."""
        coord = self.square.getCoord()
        squares = Board.getSquares()

        self.updateMoves()

        if coord[0] != 0:
            sq = squares[coord[0]-1][coord[1]+1]
            self.controlledSquares.append(sq)
            sq.addControllingPiece(self)
        if coord[0] != 7:
            sq = squares[coord[0]+1][coord[1]+1]
            self.controlledSquares.append(sq)
            sq.addControllingPiece(self)

    def updateMoves(self):
        """Updates the possible squares this pawn can move to"""
        coord = self.square.getCoord()
        squares = Board.getSquares()

        if self.isWhite:
            sq = squares[coord[0]][coord[1]+1]
            if not sq.hasPiece():
                self.moves.append(sq)
            if coord[1] == 1:  # If pawn is still on 2nd rank
                sq = squares[coord[0]][coord[1]+2]
                if not sq.hasPiece():
                    self.moves.append(sq)
        else:
            sq = squares[coord[0]][coord[1]-1]
            if not sq.hasPiece():
                self.moves.append(sq)
            if coord[1] == 6:  # If pawn is still on 7th rank
                sq = squares[coord[0]][coord[1]-2]
                if not sq.hasPiece():
                    self.moves.append(sq)
    

class Rook(Piece):
    w_id = 0
    b_id = 0
    pass

class Knight(Piece):
    w_id = 0
    b_id = 0
    

class Bishop(Piece):
    w_id = 0
    b_id = 0
    pass
