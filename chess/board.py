import sys
from game import ChessGame
import resources
from PySide6.QtCore import (Qt, Slot, QSize, QSizeF, QRectF, QRect,
    QPointF)
from PySide6.QtGui import QBrush, QPen, QPixmap
from PySide6.QtWidgets import (QApplication, QGraphicsScene,
    QGraphicsView, QGraphicsRectItem, QGraphicsGridLayout,
    QGraphicsLayoutItem, QGraphicsItem, QWidget,
    QGraphicsWidget, QTextEdit, QPushButton,
    QLabel, QGraphicsPixmapItem)
from PySide6.QtWidgets import (QGraphicsSceneMouseEvent)


# Create a list with the names of each square starting from 
# [a8, b8, ..., h8, a7, b7, ..., h7, etc..]
SQUARE_NAMES = [(l+n) for n in "87654321" for l in "abcdefgh"]


class BoardView(QGraphicsView):

    VIEW_SIZE = QSize(600, 600)

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setGeometry(
            0, 0, self.VIEW_SIZE.width(), self.VIEW_SIZE.height())
        self.setMinimumSize(self.VIEW_SIZE)
        self.setMaximumSize(self.VIEW_SIZE)

        
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

    def __init__(self, game: ChessGame, parent: QWidget = None):
        super().__init__(parent)
        self.setSceneRect(
            5, 5, self.SCENE_SIZE.width(), self.SCENE_SIZE.height())

        # 'game' attribute is the object handling the actual mechanics
        # of a chess game. Only used to set mouse events for the squares
        self.game = game
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
        them in a dictionary.
        
        The game parameter is only used to set up mouse events for the 
        squares"""
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
        
        # Give references to squares to game as well
        self.game.setSquares(squares)
        return squares

    def drawBoard(self):
        "Draws the board and places squares in the squares list"
        for sq in self.squares:
            self.addItem(self.squares[sq])

    def drawPiecesInInitialPos(self):
        """Draw the pieces in their initial positions"""
        for piece in self.INITIAL_POS:
            img = QPixmap(f":pieces\\{piece}")
            for pos in self.INITIAL_POS[piece]:
                imgItem = self.addPixmap(img)
                sq = self.squares[pos]
                # Use coordinates of square to position the piece
                imgItem.setOffset(sq.getCoord())
                # Let square know what piece it has
                sq.setPiece(piece)

    def getSquares(self) -> dict:
        return self.squares

    def highlightSquares(self, squares):
        """Change color of selected squares to highlight them"""
        # First unhighlight previously selected squares, if any
        for sq, brush in self.highlightedSquares:
            sq.setBrush(brush)
        self.highlightedSquares.clear()

        # Highlight selected squares    
        for sq in squares:
            self.highlightedSquares.append((sq, sq.brush()))
            sq.setBrush(Qt.yellow)


class Square(QGraphicsRectItem):
    """Represents a square on the chess board"""

    def __init__(self, rect: QRectF, color: Qt.GlobalColor, name: str, 
                 parent: QWidget = None):
        super().__init__(rect, parent)
        # Set coordinate name
        self.name = name

        self.piece = None

        # Set color of the square
        self.setBrush(QBrush(color))

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """When a square is clicked and there is a piece on that square,
        this function will highlight the squares that the piece can move
        to."""
        if self.hasPiece():
            squares = self.scene().game.getPossibleSquares(self)
            self.scene().highlightSquares(squares)
        return super().mousePressEvent(event)

    def setPiece(self, piece: str):
        self.piece = piece

    def getPiece(self):
        return self.piece

    def getName(self):
        return self.name

    def getCoord(self):
        return self.rect().topLeft()

    def getCenter(self):
        return self.rect().center()

    def hasPiece(self):
        if self.piece is None:
            return False
        return True

    def hasWhitePiece(self):
        if not self.hasPiece():
            return False

        if self.piece[0] == "w":
            return True
        return False
    
    def hasBlackPiece(self):
        if not self.hasPiece():
            return False

        if self.piece[0] == "b":
            return True
        return False
