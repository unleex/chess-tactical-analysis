"""This module defines classes for every type of chess piece"""
import logger

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
        self.trackedSquares = []
        self.moves = []
        self.nonMovesControlledSquares = []
        self.pinning = []
        self.pinnedBy = {}

        # Adds itself to a square, which starts things off
        self.square = square
        self.square.setPiece(self, init=True)

    def addTrackedSquare(self, square):
        self.trackedSquares.append(square)
        square.addTrackingPiece(self)

    def addNonMoveControlledSquare(self, square):
        self.nonMovesControlledSquares.append(square)
        square.addControllingPiece(self)

    def setSquare(self, square):
        """Sets a square to this piece. Called when this piece moves to
        another square"""
        old_square = self.square  # save old square
        old_square.setPiece(None)  # remove itself from old square

        self.square = square  # update square
        self.square.setPiece(self)
        
        # Get all pieces that could be affected by the move
        oldSquareTrackers = set(old_square.getTrackingPieces())
        newSquareTrackers = set(self.square.getTrackingPieces())

        piecesToUpdate = oldSquareTrackers.union(newSquareTrackers)

        logger.pieceMoved(self, piecesToUpdate)  # Marks the start
        for piece in piecesToUpdate:
            piece.updateSquares()
        logger.pieceMoved(self)  # Marks the end of the updates

    def updateSquares(self, init=False):
        """This function should be reimplemented to update the squares of
        this piece. This only serves to log the changes."""
        if not init:
            logger.pieceUpdatedSquares(self)

    def linearUpdateSquares(self, init=False):
        """updateSquares() implementation for Bishops, Rooks and Queens.
        Their move generation and ability to pin is all the same, and
        they move in a 'linear' fashion."""
        self.clearTrackedAndControlledSquares()
        coord = self.square.getCoord()
        squares = Board.getSquares()

        for d in self.directions:
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
                self.addTrackedSquare(sq)

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
                            self.addMove(sq)
                            canAddToMoves = False
                        else:
                            self.addNonMoveControlledSquare(sq)
                            canAddToMoves = False
                else:
                    # Everything that needs to happen if there is no piece
                    if canAddToMoves:
                        self.addMove(sq)

        if not init:
            logger.pieceUpdatedSquares(self)

    def clearTrackedAndControlledSquares(self):
        """Goes through a squares' trackedSquares list and removes the piece
        from their trackingPiece lists. Goes through a squares' controlledBy list
        and removes the piece from their controlledBy list. Also clears the piece's
        controlledSquares and moves list as they will be refreshed. This will be called
        whenever a piece is updating their squares due to a move."""
        for sq in self.trackedSquares:
            sq.removeTrackingPiece(self)
        for sq in self.moves:
            sq.removeControllingPiece(self)
        for sq in self.nonMovesControlledSquares:
            sq.removeControllingPiece(self)
        
        self.trackedSquares.clear()
        self.moves.clear()
        self.nonMovesControlledSquares.clear()

    def addMove(self, square):
        """Adds square to moves list and adds the piece to the squares's
        controlledBy list."""
        self.moves.append(square)
        square.addControllingPiece(self)

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
                   f"Controlling: {self.trackedSquares}\n"
                   f"Pinned By: {self.pinnedBy}\n"
                   f"Moves: {self.moves}\n" + "-"*20)
        return toPrint

    def __repr__(self):
        return self.name

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
    
    def __init__(self, isWhite, square):
        super().__init__(isWhite, square)

    def updateSquares(self, init=False):
        self.clearTrackedAndControlledSquares()
        coord = self.square.getCoord()
        squares = Board.getSquares()

        directions = (
            (1,0), (0, 1), (-1, 0), (0, -1),
            (1, 1), (1, -1), (-1, -1), (-1, 1))
        
        for d in directions:
            new_coord = coord[0] + d[0], coord[1] + d[1]
            if ((new_coord[0] > 7 or new_coord[1] > 7)
                    or (new_coord[0] < 0 or new_coord[1] < 0)):
                continue

            sq = squares[new_coord[0]][new_coord[1]]
            self.addTrackedSquare(sq)
            ctrledByOppColor = sq.isControlledByOppositeColor(self)

            if sq.hasPiece():
                if (self.isOppositeColorAs(sq.getPiece())
                        and (not ctrledByOppColor)):
                    self.addMove(sq)
                else:
                    self.addNonMoveControlledSquare(sq)
            else:
                if not ctrledByOppColor:
                    self.addMove(sq)
                else:
                    self.addNonMoveControlledSquare(sq)
                
        
        super().updateSquares(init=init)


class Queen(Piece):
    w_id = 0
    b_id = 0
    pieceName = "Queen"
    
    def __init__(self, isWhite, square):
        super().__init__(isWhite, square)
        self.directions = (
            (1, 0), (0, -1), (-1, 0), (0, 1),
            (1, 1), (1, -1), (-1, -1), (-1, 1)
        )

    def updateSquares(self, init=False):
        super().linearUpdateSquares(init)


class Pawn(Piece):
    w_id = 0
    b_id = 0
    pieceName = "Pawn"

    def __init__(self, isWhite, square):
        super().__init__(isWhite, square)
        self.controlledSquares = []

    def updateSquares(self, init=False):
        """Gets the squares this pawn can move to and updates the state
        of any squares that this pawn affects."""
        self.clearTrackedAndControlledSquares()
        coord = self.square.getCoord()
        squares = Board.getSquares()

        self.updateMoves()

        if self.isWhite:
            if coord[0] != 0:
                sq = squares[coord[0]-1][coord[1]+1]
                self.addTrackedSquare(sq)
                self.controlledSquares.append(sq)
                sq.addControllingPiece(self)
                if sq.hasPiece() and self.isOppositeColorAs(sq.getPiece()):
                    self.addMove(sq)
            if coord[0] != 7:
                sq = squares[coord[0]+1][coord[1]+1]
                self.addTrackedSquare(sq)
                self.controlledSquares.append(sq)
                sq.addControllingPiece(self)
                if sq.hasPiece() and self.isOppositeColorAs(sq.getPiece()):
                    self.addMove(sq)
        else:
            if coord[0] != 0:
                sq = squares[coord[0]-1][coord[1]-1]
                self.addTrackedSquare(sq)
                self.controlledSquares.append(sq)
                sq.addControllingPiece(self)
                if sq.hasPiece() and self.isOppositeColorAs(sq.getPiece()):
                    self.addMove(sq)
            if coord[0] != 7:
                sq = squares[coord[0]+1][coord[1]-1]
                self.addTrackedSquare(sq)
                self.controlledSquares.append(sq)
                sq.addControllingPiece(self)
                if sq.hasPiece() and self.isOppositeColorAs(sq.getPiece()):
                    self.addMove(sq)

        super().updateSquares(init=init)

    def updateMoves(self):
        """Updates the possible squares this pawn can move to"""
        coord = self.square.getCoord()
        squares = Board.getSquares()

        if self.isWhite:
            sq = squares[coord[0]][coord[1]+1]
            self.addTrackedSquare(sq)
            if not sq.hasPiece():
                self.addMove(sq)
                if coord[1] == 1:  # If pawn is still on 2nd rank
                    sq = squares[coord[0]][coord[1]+2]
                    self.addTrackedSquare(sq)

                    if not sq.hasPiece():
                        self.addMove(sq)
        else:
            sq = squares[coord[0]][coord[1]-1]
            self.addTrackedSquare(sq)
            if not sq.hasPiece():
                self.moves.append(sq)
                if coord[1] == 6:  # If pawn is still on 7th rank
                    sq = squares[coord[0]][coord[1]-2]
                    self.addTrackedSquare(sq)
                    if not sq.hasPiece():
                        self.moves.append(sq)

    def clearTrackedAndControlledSquares(self):
        for sq in self.trackedSquares:
            sq.removeTrackingPiece(self)
        for sq in self.controlledSquares:
            sq.removeControllingPiece(self)

        self.trackedSquares.clear()
        self.controlledSquares.clear()
        self.moves.clear()

    def addMove(self, square):
        # Adds move to Pawn's moves list without 'controlling' the square.
        # This is done because a Pawn always controls its two upper
        # adjacent squares. This function enables them to move there, but
        # the square is already 'controlled'.
        self.moves.append(square)
    

class Rook(Piece):
    w_id = 0
    b_id = 0
    pieceName = "Rook"

    def __init__(self, isWhite, square):
        super().__init__(isWhite, square)
        self.directions = (
            (1, 0), (0, -1), (-1, 0), (0, 1)
        )

    def updateSquares(self, init=False):
        super().linearUpdateSquares(init)
                    
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
    
    def __init__(self, isWhite, square):
        super().__init__(isWhite, square)

    def updateSquares(self, init=False):
        self.clearTrackedAndControlledSquares()
        coord = self.square.getCoord()
        squares = Board.getSquares()

        direction = (
            (1, 2), (2, 1), (2, -1), (1, -2),
            (-1, -2), (-2, -1), (-2, 1), (-1, 2))
        
        for d in direction:
            new_coord = coord[0] + d[0], coord[1] + d[1]
            if ((new_coord[0] > 7 or new_coord[1] > 7)
                    or (new_coord[0] < 0 or new_coord[1] < 0)):
                continue

            sq = squares[new_coord[0]][new_coord[1]]
            self.addTrackedSquare(sq)
            if not sq.hasPiece() or self.isOppositeColorAs(sq.getPiece()):
                self.addMove(sq)
            else:
                self.addNonMoveControlledSquare(sq)

        super().updateSquares(init=init)
    

class Bishop(Piece):
    w_id = 0
    b_id = 0
    pieceName = "Bishop"
    
    def __init__(self, isWhite, square):
        super().__init__(isWhite, square)
        self.directions = (
            (1, 1), (1, -1), (-1, -1), (-1, 1)
        )

    def updateSquares(self, init=False):
        super().linearUpdateSquares(init)