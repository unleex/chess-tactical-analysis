"""This module handles the drawing of the board and its pieces."""
from __future__ import annotations
from tkinter.messagebox import NO
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from movement import PieceMovements
import sys
import resources
from PySide6.QtCore import (Qt, Slot, QSize, QSizeF, QRectF, QRect,
    QPointF)
from PySide6.QtGui import QBrush, QPen, QPixmap
from PySide6.QtWidgets import (QApplication, QGraphicsScene,
    QGraphicsView, QGraphicsRectItem, QGraphicsGridLayout,
    QGraphicsLayoutItem, QGraphicsItem, QWidget,
    QGraphicsWidget, QTextEdit, QPushButton,
    QLabel, QGraphicsPixmapItem)
from PySide6.QtWidgets import QGraphicsSceneMouseEvent
from interface import BoardToGameInterface


# Create a list with the names of each square starting from
# [a8, b8, ..., h8, a7, b7, ..., h7, etc..]
SQUARE_NAMES = [(l+n) for n in "87654321" for l in "abcdefgh"]


class BoardView(QGraphicsView):

    VIEW_SIZE = QSize(600, 600)

    def __init__(self):
        super().__init__()
        self.setGeometry(
            0, 0, self.VIEW_SIZE.width(), self.VIEW_SIZE.height())
        self.setMinimumSize(self.VIEW_SIZE)

        scene = BoardScene()
        self.setScene(scene)


class BoardScene(QGraphicsScene):

    # Make a little smaller than the view for some margins
    SCENE_SIZE = QSize(555, 555)
    SQUARE_SIZE = SCENE_SIZE / 8

    INITIAL_POS = {
        "wRook": ("a1", "h1"),
        "wKnight": ("b1", "g1"),
        "wBishop": ("c1", "f1"),
        "wQueen": ("d1",),
        "wKing": ("e1",),
        "wPawn": ("a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"),
        "bRook": ("a8", "h8"),
        "bKnight": ("b8", "g8"),
        "bBishop": ("c8", "f8"),
        "bQueen": ("d8",),
        "bKing": ("e8",),
        "bPawn": ("a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"),
    }

    def __init__(self):
        super().__init__()
        self.setSceneRect(
            5, 5, self.SCENE_SIZE.width(), self.SCENE_SIZE.height())

        # Create the squares.
        self.squares = self.createSquares()
        # Draw the board
        self.drawBoard()
        # Draw pieces on their initial position
        self.drawPiecesInInitialPos()

        # Util variables
        self.highlightedSquares = []

    def createSquares(self):
        """Create Square objects for every square on the board and put
        them in a dictionary."""
        squares = {}
        squareNames = iter(SQUARE_NAMES)
        whiteOnEven = True
        # row height and col width are the same
        rowHeight = self.SQUARE_SIZE.height()
        rowCoord = [(x * rowHeight) for x in range(0, 8)]
        colCoord = [(y, y * rowHeight) for y in range(0, 8)]

        for row in rowCoord:
            # At each row, white squares will be on the even numbered cols
            # or the odd numbered cols. c is the variable that knows the
            # parity of a column
            whiteOnEven = False if whiteOnEven is True else True
            for c, col in colCoord:
                rect = QRectF(QPointF(col, row), self.SQUARE_SIZE)
                name = next(squareNames)

                if (c%2==0 and whiteOnEven) or (c%2==1 and not whiteOnEven):
                    squares[name] = Square(
                        rect=rect, color=Qt.white, name=name)
                else:
                    squares[name] = Square(
                        rect=rect, color=Qt.black, name=name)

        return squares

    def drawBoard(self):
        "Draws all the Square objects to make a chess board"
        for sq in self.squares:
            self.addItem(self.squares[sq])

    def drawPiecesInInitialPos(self):
        """Draw the pieces in their initial positions"""
        # These ids are appened to the piece's name so that they're unique
        for piece in self.INITIAL_POS:
            img = QPixmap(f":pieces\\{piece}")
            for id_, pos in enumerate(self.INITIAL_POS[piece]):
                imgItem = self.addPixmap(img)
                sq = self.squares[pos]
                sq.setPiece(piece + str(id_), imgItem)

    def highlightSquares(self, squares):
        """Change color of selected squares to highlight them"""
        # First unhighlight previously selected squares, if any
        self.unhighlightSquares()

        # Highlight selected squares
        for sqName in squares:
            sq = self.squares[sqName]
            self.highlightedSquares.append((sq, sq.brush()))
            sq.setBrush(Qt.yellow)

    def unhighlightSquares(self):
        """Unhighlight currently highlighted squares"""
        for sq, brush in self.highlightedSquares:
            sq.setBrush(brush)
        self.highlightedSquares.clear()

    def movePiece(self, squares):
        """Move piece from squares[0] to squares[1]"""
        from_sq, to_sq = self.squares[squares[0]], self.squares[squares[1]]
        from_sq.movePieceTo(to_sq)

        self.unhighlightSquares()

    def printSquares(self):
        """Prints all the squares and the pieces on each square.
        Used for debugging."""
        i = 1
        for name in self.squares:
            end = '\t' if i % 8 != 0 else '\n'
            piece = self.squares[name].getPiece()
            print(name + ': ' + str(self.squares[name].getPiece()), end=end)
            i += 1
        print('-' * 20)


class Square(QGraphicsRectItem):
    """This class inherits from QGraphicsRectItem, so it is used to
    draw a square on the board scene. Keeps track of the name of any
    piece that is on it and has mouse events to handle when the user
    clicks it."""

    def __init__(self, rect: QRectF, color: Qt.GlobalColor, name):
        super().__init__(rect)
        self.name = name
        self.piece = None
        self.piecePixmap = None

        # Set color of the square
        self.setBrush(QBrush(color))

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """When a square is clicked and there is a piece on that square,
        this function will highlight the squares that the piece can move
        to."""
        # Let the game know this square has been clicked
        result = BoardToGameInterface.squareClicked(
            self.name)

        # Check result to know what to do
        if result["action"] == "highlightSquares":
            self.scene().highlightSquares(result["squares"])
        elif result["action"] == "movePiece":
            self.scene().movePiece(result["squares"])

        return super().mousePressEvent(event)

    def setPiece(self, piece: str, pixmap: str):
        """Sets a piece to this square. Has the effect of visually moving
        the piece to this square on the board."""
        # Must come first, as it checks the current value of self.piece
        self.setPiecePixmap(pixmap)

        self.piece = piece

    def getPiece(self):
        return self.piece

    def movePieceTo(self, square_to):
        """Moves the piece on this square to another square"""
        piece, pixmap = self.piece, self.piecePixmap
        self.piece = self.piecePixmap = None

        square_to.setPiece(piece, pixmap)

    def setPiecePixmap(self, pixmap: QGraphicsPixmapItem):
        """Gives a reference to the square of the pixmap item of the piece
        on this square."""
        if self.hasPiece():
            # If there was a piece on this square, it was captured
            # and its pixmap can be deleted off the scene
            self.scene().removeItem(self.piecePixmap)
        
        pixmap.setOffset(self.getCoord())  # moves img of piece to sq
        self.piecePixmap = pixmap

    def getPiecePixmap(self):
        return self.piecePixmap

    def getCoord(self):
        return self.rect().topLeft()

    def getCenter(self):
        return self.rect().center()

    def hasPiece(self):
        if self.piece is None:
            return False
        return True

