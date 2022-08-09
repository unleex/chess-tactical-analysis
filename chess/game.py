from PySide6.QtWidgets import (QWidget, QHBoxLayout, QFrame, QLabel,
                               QGridLayout, QVBoxLayout)
from PySide6.QtCore import Qt
from board import BoardView, Square
from movement import PieceMovements
from interface import BoardToGameInterface

class ChessGame(QWidget):
    
    def __init__(self):
        super().__init__()

        BoardToGameInterface.setCurrentGame(self)

        # Widgets
        self.board = BoardView()
        self.gameInfo = GameInfo()
        
        # Get squares and give a reference to them to PieceMovements
        self.squares = self.board.getSquares()
        
        # Class that provides squares that a piece can move to
        self.movement = PieceMovements()
        self.movement.setSquares(self.squares)

        # Game variables
        self.turn = 0
        self.whiteTurn = True
        self.selectedSquare = None
        self.possibleSquares = None

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.board, stretch=3)
        self.layout.addWidget(self.gameInfo, stretch=1)
        self.setLayout(self.layout)

    def squareClicked(self, squareName, piece):
        """"""
        print(squareName + ' with a ' + piece + ' has been clicked')
        return {}

    def selectSquare(self, square: Square):
        """Saves square and its piece as the selected square and
        returns squares that the piece can go to."""
        self.selectedSquare = square
        self.possibleSquares = self.getPossibleSquares(square)
        return self.possibleSquares

    def getPossibleSquares(self, square: Square):
        if (self.whiteTurn and square.hasWhitePiece() 
                or (not self.whiteTurn) and square.hasBlackPiece()):
            return self.movement.getPossibleSquares(square)
        return []

    def moveToSquare(self, newSquare: Square):
        """Move piece in selected square to passed in square. Changes
        attributes of the squares to reflect the move, and returns the
        squares to allow the BoardView to redraw the piece. Also adds
        the move to the move list"""
        if newSquare in self.possibleSquares:
            # Add move to to the move list.
            moveName = self.createMoveName(self.selectedSquare, newSquare)
            self.gameInfo.moveList.addMove(moveName, isWhite=self.whiteTurn)

            # Because we want to return the selectedSquare and set 
            # self.selectedSquare to None, we give it the name prevSquare.   
            prevSquare = self.selectedSquare
            newSquare.setPiece(prevSquare.getPiece())
            prevSquare.setPiece(None)
            self.selectedSquare = None
            self.possibleSquares = []

            # Now that piece has moved, get its possible squares to move to
            # from its new square and add them to the appropriate
            # controlledSquares list
            if self.whiteTurn:
                self.updateControlledSquares(newSquare)
            else:
                self.updateControlledSquares(newSquare)

            self.whiteTurn = True if self.whiteTurn is False else False
            return newSquare, prevSquare

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

    def updateControlledSquares(self, square: Square):
        """Compare the king's possible moves and this piece's possible moves
        to update what squares the king cannot move to. """
        pieceSquares = set(self.getPossibleSquares(square))
        if self.whiteTurn:
            self.bKingControlledSquares[square.getPiece()] = \
                pieceSquares.intersection(self.bKingSquares)
        else:
            self.wKingControlledSquares[square.getPiece()] = \
                pieceSquares.intersection(self.wKingSquares)


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
