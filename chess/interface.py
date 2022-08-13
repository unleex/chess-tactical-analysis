from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game import ChessGame
    from board import Square

class BoardToGameInterface:
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

    @classmethod
    def selectSquare(cls, square: Square):
        """Called when a square is clicked. Looks at the piece on the
        square and returns a list of possible squares it can move to."""
        return cls.CURRENT_GAME.selectSquare(square)

    @classmethod
    def moveToSquare(cls, square: Square):
        """Called when an empty square or an enemy piece is clicked. 
        Checks if a selected piece can move to it."""
        return cls.CURRENT_GAME.moveToSquare(square)

    @classmethod
    def isWhiteTurn(cls):
        """Called by Squares when they are clicked and want to know if
        they're the enemy piece"""
        return cls.CURRENT_GAME.whiteTurn

    @classmethod
    def squareClicked(cls, squareName):
        """Called when a Square is clicked"""
        return cls.CURRENT_GAME.squareClicked(squareName)
