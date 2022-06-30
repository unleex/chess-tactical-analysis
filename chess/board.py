import sys
import random
from PySide6.QtCore import Qt, Slot, QSize, QSizeF, QRectF, QRect
from PySide6.QtGui import QBrush, QPen
from PySide6.QtWidgets import (QApplication, QGraphicsScene,
    QGraphicsView, QGraphicsRectItem, QGraphicsGridLayout,
    QGraphicsLayoutItem, QGraphicsItem, QWidget,
    QGraphicsWidget, QTextEdit, QPushButton)
from PySide6.QtWidgets import (QGraphicsSceneMouseEvent)


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

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setSceneRect(
            5, 5, self.SCENE_SIZE.width(), self.SCENE_SIZE.height())

        # Will hold references to each square on the board
        self.squares = []

        # Draw the board
        self.drawBoard()

    def drawBoard(self):
        "Draws the board and places squares in the squares list"
        squareNames = iter(SquareCoords.getCoordNames())  # list of [a8, b8, ...]
        whiteOnEven = True
        rowHeight = self.SQUARE_SIZE.height()  # This is equal to column width
        x_coord = [(x * rowHeight) for x in range(0, 8)]
        y_coord = [(y, (y * rowHeight)) for y in range(0, 8)]
        for row in x_coord:
            whiteOnEven = False if whiteOnEven is True else True
            for col_index, col in y_coord:
                sq_coords = QRectF(row, col, 
                    self.SQUARE_SIZE.width(), self.SQUARE_SIZE.height())

                # Check if dark or white square should be drawn
                if ((col_index % 2 == 0 and whiteOnEven) 
                    or (col_index % 2 == 1 and not whiteOnEven)):
                    sq = Square(sq_coords, Qt.white, next(squareNames))
                else:
                    sq = Square(sq_coords, Qt.black, next(squareNames))
                
                # Add the square to the squares list and then add o the scene
                self.squares.append(sq)
                self.addItem(sq)


class Square(QGraphicsRectItem):
    """Represents a square on the chess board"""

    def __init__(self, rect: QRectF, color: Qt.GlobalColor, coord: str, parent: QWidget = None):
        super().__init__(rect, parent)
        # Set coordinate name
        self.coord = coord

        # Set color of the square
        self.setBrush(QBrush(color))


class SquareCoords:
    """Class that links a square's index value in BoardScene.squares to 
    the traditional chess coords (a1, h3, g4) """

    sqCoords = {}
    sqIndex = 0
    letters = "abcdefgh"
    numbers = "87654321"
    for n in numbers:
        for l in letters:
            sqCoords[l+n] = sqIndex
            sqIndex += 1

    @classmethod
    def getCoordNames(cls):
        return cls.sqCoords.keys()

    def __getitem__(self, key: str) -> str:
        return self.sqCoords[key]

    def __getattribute__(self, __name: str) -> str:
        return self.sqCoords[__name]


if __name__ == "__main__":
    app = QApplication([])

    boardView = BoardView()
    boardScene = BoardScene()
    boardView.setScene(boardScene)

    boardView.show()
    sys.exit(app.exec())