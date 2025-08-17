from game import Square

from PySide6.QtWidgets import QWidget


class BoardArrow(QWidget):

    def __init__(self, sq_from: Square, sq_to: Square):

        self.sq_from = sq_from
        self.sq_to = sq_to
