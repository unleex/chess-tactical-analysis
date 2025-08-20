from __future__ import annotations

from typing import TYPE_CHECKING
from PySide6.QtWidgets import QWidget
if TYPE_CHECKING:
    from game import ChessGame

class Interface:
    """Class that allows BoardView and Square class to communicate with
    ChessGame, without having to hold a reference to it.
    
    Note: ChessGame does not a class to communicate with the BoardView,
    is it holds a reference to BoardView. The reason BoardView cannot
    have a reference to ChessGame is that it would create awkward
    cyclic references, which is bad design."""

    CURRENT_GAME = None

    @classmethod
    def setCurrentGame(cls, game: ChessGame):
        """Whenever a ChessGame instance is created, it calls this to
        set itself as the CURRENT_GAME"""
        cls.CURRENT_GAME = game
        game.check

    @classmethod
    def setCurrentWindow(cls, window: QWidget):
        cls.window = window
        
    @classmethod
    def isWhiteTurn(cls):
        """Called by Squares when they are clicked and want to know if
        they're the enemy piece"""
        return cls.CURRENT_GAME.whiteTurn

    @classmethod
    def squareClicked(cls, squareName):
        """Called when a Square is clicked"""
        return cls.CURRENT_GAME.squareClicked(squareName)

    @classmethod
    def pawnPromoted(cls, promotedTo):
        """Called when the user decides what promote"""
        return cls.CURRENT_GAME.pawnPromoted(promotedTo)

    