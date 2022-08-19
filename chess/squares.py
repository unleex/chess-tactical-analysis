class Squares:

    squares = None

    @classmethod
    def setSquares(cls, squares):
        cls.squares = squares

    @classmethod
    def getSquares(cls):
        return cls.squares