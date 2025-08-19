import typing

from stockfish import Stockfish


class Engine:
    """Computes best moves and evaluates position"""

    def __init__(
            self,  
            stockfish_engine_path: str,
            depth: int,
            move_history: typing.Optional[list[str]] = None
        ):
        self.stockfish = Stockfish(
            path=stockfish_engine_path,
            depth=depth
        )
        _move_history = move_history if move_history is not None else []
        self.stockfish.set_position(_move_history)
    
    def add_move(self, move: str):
        self.stockfish.make_moves_from_current_position([move])
    
    def get_best_move(self):
        return self.stockfish.get_best_move()