from PySide6.QtWidgets import QWidget, QHBoxLayout, QFrame
from PySide6.QtCore import Qt
from board import BoardView

class ChessGame(QWidget):
    
    def __init__(self, parent=None, f=Qt.WindowFlags()):
        super().__init__(parent, f)

        self.board = BoardView()
        self.gameInfo = GameInfo()

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.board, stretch=3)
        self.layout.addWidget(self.gameInfo, stretch=1)
        self.setLayout(self.layout)


class GameInfo(QFrame):

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background: blue")


