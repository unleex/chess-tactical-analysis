import sys
from board import BoardView, BoardScene
from game import ChessGame

from PySide6.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication([])

    # Create game object first (must be created first)
    game = ChessGame()

    boardView = BoardView()
    boardScene = BoardScene(game)
    boardView.setScene(boardScene)
    boardView.show()
    
    sys.exit(app.exec())