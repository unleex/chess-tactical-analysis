from PySide6.QtWidgets import (QWidget, QHBoxLayout, QFrame, QLabel,
                               QGridLayout, QVBoxLayout)
from PySide6.QtCore import Qt
from board import BoardView, Square 
from interface import BoardToGameInterface
from pieces import *
import logger

class ChessGame(QWidget):
    
    def __init__(self):
        super().__init__()

        BoardToGameInterface.setCurrentGame(self)

        # Widgets
        self.board = BoardView()
        self.gameInfo = GameInfo()
        
        # Game variables
        self.turn = 0
        self.whiteTurn = True
        self.selectedPiece = None
        self.selectedSquare = None  # square of the selected piece
        self.wKing = None
        self.bKing = None

        # Make a board state
        self.squares = [[], [], [], [], [], [], [], []]
        self.pieces = []
        Board.setSquares(self.squares)  # So that pieces have access to squares
        self.initializeBoardState()

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.board, stretch=3)
        self.layout.addWidget(self.gameInfo, stretch=1)
        self.setLayout(self.layout)

    def initializeBoardState(self):
        """Initializes the board state by creating all the squares
        and adding the appropriate Pieces to their initial squares."""
        for i in range(8):
            for j in range(8):
                sqName = self.coordToSquareName((i, j))
                self.squares[i].append(Square((i, j), sqName))

        for i in range(8):
            # Piece instances save themselves as an attribute to
            # the passed in 'square' using square.setPiece(self).

            # Add pawns
            p1 = Pawn(isWhite=True, square=self.squares[i][1])
            p2 = Pawn(isWhite=False, square=self.squares[i][6])
            self.pieces.extend((p1, p2))

            # Add rooks
            if i == 0 or i == 7:  # i=0 is the a file and i=7 is the h file
                p1 = Rook(isWhite=True, square=self.squares[i][0])
                p2 = Rook(isWhite=False, square=self.squares[i][7])
                self.pieces.extend((p1, p2))

            # Add knights
            if i == 1 or i == 6:
                p1 = Knight(isWhite=True, square=self.squares[i][0])
                p2 = Knight(isWhite=False, square=self.squares[i][7])
                self.pieces.extend((p1, p2))

            # Add bishops
            if i == 2 or i == 5:
                p1 = Bishop(isWhite=True, square=self.squares[i][0])
                p2 = Bishop(isWhite=False, square=self.squares[i][7])
                self.pieces.extend((p1, p2))

            # Add queens
            if i == 3:
                p1 = Queen(isWhite=True, square=self.squares[i][0])
                p2 = Queen(isWhite=False, square=self.squares[i][7])
                self.pieces.extend((p1, p2))

            # Add kings
            if i == 4:
                self.wKing = King(isWhite=True, square=self.squares[i][0])
                self.bKing = King(isWhite=False, square=self.squares[i][7])
                self.pieces.extend((self.wKing, self.bKing))

        for piece in self.pieces:
            piece.updateSquares(init=True)
        logger.showBoard(self.squares)

    def squareNameToCoord(self, squareName):
        """Convert a square's name (eg. a1) to indexes for the square
        on self.squares"""
        letters = "abcdefgh"

        letterCoord = letters.index(squareName[0])
        numCoord = int(squareName[1]) - 1

        return letterCoord, numCoord

    def coordToSquareName(self, coord):
        """Convert a square's index in self.squares (nicknamed coords),
        to the traditional square names in chess (eg. a1, b2)"""
        letters = "abcdefgh"

        sqName = letters[coord[0]] + str(coord[1] + 1)
        return sqName

    def squareClicked(self, squareName):
        """"""
        coord = self.squareNameToCoord(squareName)
        sq = self.squares[coord[0]][coord[1]]

        if sq.hasPiece():
            # If there is a piece on the clicked square, select the piece
            # and visually highlight where it can go.
            self.selectedPiece = sq.getPiece()
            self.selectedSquare = sq
            return {
                "action": "highlightSquares",
                "squares": self.selectedPiece.getMoves(nameOnly=True)
            }
        else:
            # If there is no piece, check if there is a piece selected
            # that can move to the square.
            if (self.selectedPiece is not None 
                    and self.selectedPiece.canMoveTo(sq)):
                self.selectedPiece.setSquare(sq) # Moves the piece to sq
                
                # After every turn, one of the kings will have their squares
                # updated, as they could be restricted at any time and their
                # trackedSquares list is not enough.
                if self.whiteTurn:
                    self.bKing.updateSquares()
                else:
                    self.wKing.updateSquares()

                old_sq = self.selectedSquare  # Save the square the piece used to be on
                self.selectedPiece = None
                self.selectedSquare = None

                self.whiteTurn = True if self.whiteTurn is False else False  # switch turns

                logger.showBoard(self.squares)

                return {
                    "action": "movePiece",
                    "squares": [str(old_sq), str(sq)]
                }


        
        return {}

    def createMoveName(self, oldSquare: Square, newSquare: Square):
        """Creates a move name (eg. Nf3) from looking at a pieces'
        current square (oldSquare) and the square it's going to move
        to (newSquare)"""
        # Abbreviation for knight in moves is N, as the King takes K
        if (pieceName := oldSquare.getPiece()[1:]) == "Knight":
            abbr = "N"
        elif pieceName == "Pawn":
            abbr = ""
        else:
            abbr = pieceName[0]

        # TODO: MOVE NAMES FOR PROMOTION

        # Checks if it's a capture
        if newSquare.hasPiece():
            return abbr + 'x' + newSquare.getName()
        return abbr + newSquare.getName()


class GameInfo(QFrame):

    def __init__(self):
        super().__init__()
        self.moveList = MoveList()

        layout = QVBoxLayout()
        layout.addWidget(self.moveList, stretch=1)
        self.setLayout(layout)


class MoveList(QFrame):
    """Widget that shows move history of a game"""

    def __init__(self):
        super().__init__()
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.setLineWidth(3)

        # Row number for the move list (increments after black's turn)
        self.row = 0

        label = QLabel("Moves")
        self.moveList, self.moveListLayout = self.createMoveList()

        self.layout = QVBoxLayout()
        self.layout.addWidget(label, stretch=1, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.moveList, stretch=9)
        self.setLayout(self.layout)

    def createMoveList(self):
        """Creates frame that will hold move history"""
        moveList = QFrame()
        layout = QGridLayout()
        for i in range(20):
            layout.setRowStretch(i, 1)
        layout.setColumnStretch(0, 1)  # Column showing turn number should be smaller.
        layout.setColumnStretch(1, 2)
        layout.setColumnStretch(2, 2)
        moveList.setLayout(layout)
        return moveList, layout

    def addMove(self, move: str, isWhite=True):
        """Adds move to the move history"""
        turnLabel = QLabel(str(self.row + 1))
        label = QLabel(move)
        if isWhite:
            self.moveListLayout.addWidget(turnLabel, self.row, 0)
            self.moveListLayout.addWidget(label, self.row, 1)
        else:
            self.moveListLayout.addWidget(label, self.row, 2)
            self.row += 1

class Square:
    """A detailed representation of a square that will hold
    info about the square's state"""

    def __init__(self, coord, name):
        self.name = name
        self.piece = None
        self.trackedBy = []
        self.controlledBy = []
        self.pinned = False
        self.coord = coord

    def setPiece(self, piece, init=False):
        self.piece = piece

        # Don't update squares when initializing the pieces on their
        # initial positions
        if (not init) and (piece is not None):
            self.piece.updateSquares()

    def addTrackingPiece(self, piece):
        self.trackedBy.append(piece)

    def removeTrackingPiece(self, piece):
        indexToRemove = self.trackedBy.index(piece)
        del self.trackedBy[indexToRemove]

    def getTrackingPieces(self):
        return self.trackedBy

    def addControllingPiece(self, piece):
        self.controlledBy.append(piece)
    
    def getControllingPieces(self):
        return self.controlledBy
    
    def removeControllingPiece(self, piece):
        indexToRemove = self.controlledBy.index(piece)
        del self.controlledBy[indexToRemove]

    def isControlledByOppositeColor(self, piece):
        for controllingPiece in self.controlledBy:
            if controllingPiece.isOppositeColorAs(piece):
                return True
        return False

    def getCoord(self):
        return self.coord

    def hasPiece(self):
        if self.piece is not None:
            return True
        return False

    def getPiece(self):
        return self.piece

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name