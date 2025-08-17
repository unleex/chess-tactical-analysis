from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import GameSquare  # Adjust the import path as needed

class Squares:

    squares: 'list[list[GameSquare]] | None' = None

    @classmethod
    def setSquares(cls, squares: 'list[list[GameSquare]]') -> None:
        cls.squares = squares

    @classmethod
    def getSquares(cls) -> 'list[list[GameSquare]] | None':
        return cls.squares