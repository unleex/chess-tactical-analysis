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

    def __init__(self, isWhite, square):
        pieceType = type(self)
        if isWhite:
            self.name = "w" + pieceType.pieceName + str(pieceType.w_id)
            pieceType.w_id += 1
        else:
            self.name = "b" + pieceType.pieceName + str(pieceType.b_id)
            pieceType.b_id += 1


        self.isWhite = isWhite
        self.controlledSquares = []
        self.moves = []
        self.pinning = []
        self.pinnedBy = {}

        # Adds itself to a square, which starts things off
        self.square = square
        self.square.setPiece(self)
    
    def getPossibleSquares(self):
        ...

    def setSquare(self, square):
        self.square = square

    def updateSquares(self):
        ...

    def addPinningPiece(self, piece, allowedSquares):
        self.pinnedBy[piece] = allowedSquares

    def isOppositeColorAs(self, piece):
        if self.isWhite is piece.isWhite:
            return False
        return True

    def isSameColorAs(self, piece):
        if self.isWhite is piece.isWhite:
            return True
        return False

    def __str__(self):
        toPrint = (f"{self.name} on square {self.square.name}\n"
                   f"Controlling: {self.controlledSquares}\n"
                   f"Pinned By: {self.pinnedBy}\n"
                   f"Moves: {self.moves}\n" + "-"*20)
        return toPrint

    def getMoves(self, nameOnly=False):
        if nameOnly:
            # Square.__str__ simply returns the name of a square
            return [str(sq) for sq in self.moves]
        return self.moves

    def canMoveTo(self, square):
        """Checks if square is in this Piece's move list"""
        return square in self.moves


class King(Piece):
    w_id = 0
    b_id = 0
    pieceName = "King"
    pass

class Queen(Piece):
    w_id = 0
    b_id = 0
    pieceName = "Queen"
    pass

class Pawn(Piece):
    w_id = 0
    b_id = 0
    pieceName = "Pawn"

    def __init__(self, isWhite, square):
        super().__init__(isWhite, square)

    def updateSquares(self):
        """Gets the squares this pawn can move to and updates the state
        of any squares that this pawn affects."""
        self.controlledSquares.clear()
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
        self.moves.clear()
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
    pieceName = "Rook"

    def __init__(self, isWhite, square):
        super().__init__(isWhite, square)

    def updateSquares(self):
        """Updates the states of squares this rook can move to"""
        coord = self.square.getCoord()
        squares = Board.getSquares()

        directions = ((1,0), (0, 1), (-1, 0), (0, -1))
        
        for d in directions:
            canAddToMoves = True
            piecesOnRankOrFile = []
            for i in range(1, 8):
                sqCoords = coord[0] + d[0]*i, coord[1] + d[1]*i
                if (sqCoords[0] == 8 or sqCoords[1] == 8  # End of file or rank 
                    or sqCoords[0] == -1 or sqCoords[1] == -1):  # No negs
                    break

                sq = squares[sqCoords[0]][sqCoords[1]]
                piece = sq.getPiece()
                
                # Update Piece and Square's control vars
                self.controlledSquares.append(sq)
                sq.addControllingPiece(self)

                # Everything that needs to happen if there is a piece
                if sq.hasPiece():

                    # Check if piece is a king. If piece is a king of 
                    # opposite color, determine if there is an enemy 
                    # piece in front of it that should be pinned.
                    if piece.pieceName == "King" and self.isOppositeColorAs(piece):
                        if (len(piecesOnRankOrFile) == 1
                                and (self.isOppositeColorAs(piecesOnRankOrFile[0]))):
                            self.pinPiece(piece, d)
                        
                    # Track pieces on the rank or file. Used to
                    # determine if a piece should be pinned if a
                    # king is encountered.
                    piecesOnRankOrFile.append(piece)
                
                    # If piece is of opposite color, add to moves list.
                    if canAddToMoves:
                        if self.isOppositeColorAs(piece):
                            self.moves.append(sq)
                            canAddToMoves = False
                        else:
                            canAddToMoves = False
                    
    def pinPiece(self, piece, direction):
        """Pins piece and gives the piece its allowed squares"""
        # NOT TESTED
        coord = self.square.getCoord()
        squares = Board.getSquares()

        pieceCoord = piece.square.getCoord()
        allowedSquares = []
        
        # Get all the squares the pinned piece has available to it
        for i in range(8):
            new_coord = coord[0] + direction[0]*i, coord[1] + direction[1]*i
            if ((new_coord[0] == pieceCoord[0])
                    and (new_coord[1] == pieceCoord[1])):
                break

            sq = squares[new_coord[0]][new_coord[1]]
            allowedSquares.append(sq)
        
        self.pinning.append(piece)
        piece.addPinningPiece(self, allowedSquares)


class Knight(Piece):
    w_id = 0
    b_id = 0
    pieceName = "Knight"  
    pass  
    

class Bishop(Piece):
    w_id = 0
    b_id = 0
    pieceName = "Bishop"
    pass
