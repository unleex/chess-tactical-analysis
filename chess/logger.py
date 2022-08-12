"""Module that will log certain activities in another file"""

print("Opening log file...")
LOG_FILE = open("logs.txt", "w", )

def pieceUpdatedSquares(piece):
    """Shows that piece was updated and its current state"""
    toLog = f"UPDATED {piece.name}\n" + str(piece) + '\n'
    LOG_FILE.write(toLog)
    LOG_FILE.flush()

def pieceMoved(piece, piecesToUpdate=None):
    """Shows that a piece has moved. If piecesToUpdate is not None, this
    marks the start of updates. If None, it marks the end of updates."""
    if piecesToUpdate is not None:
        toLog = (f"START\t{piece.name} HAS MOVED\t" + "-"*20 + "\n"
               + f"PIECES AFFECTED: {piecesToUpdate}\n")
    else:
        toLog = f"END  \t{piece.name} HAS MOVED\t" + "-"*20 + "\n"
    LOG_FILE.write(toLog)
    LOG_FILE.flush()

def closeLog():
    print("Closing log file...")
    LOG_FILE.close()