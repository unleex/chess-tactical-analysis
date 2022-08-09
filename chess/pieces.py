"""This module defines classes for every type of chess piece"""
from abc import ABC, abstractmethod

class Piece(ABC):
    """Base class for all pieces"""

    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def getPossibleSquares(self):
        ...


class King(Piece):
    pass

class Queen(Piece):
    pass

class Pawn(Piece):
    pass

class Rook(Piece):
    pass

class Knight(Piece):
    pass

class Bishop(Piece):
    pass
