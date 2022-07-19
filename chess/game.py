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
        squares to allow the BoardView to redraw the piece."""
        if newSquare in self.possibleSquares:
            prevSquare = self.selectedSquare
            self.selectedSquare = None
            self.possibleSquares = []
            self.whiteTurn = True if self.whiteTurn is False else False
            newSquare.setPiece(prevSquare.getPiece())
            prevSquare.setPiece(None)
            return newSquare, prevSquare
        

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
        moveList.setLayout(layout)
        return moveList, layout

    def addMove(self, move: str, isWhite=True):
        """Adds move to the move history"""
        label = QLabel(move)
        if isWhite:
            self.moveListLayout.addWidget(label, self.row, 0)
        else:
            self.moveListLayout.addWidget(label, self.row, 1)
            self.row += 1
