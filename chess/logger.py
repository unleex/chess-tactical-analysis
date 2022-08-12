"""Module that will log certain activities in another file"""

print("Opening log file...")
LOG_FILE = open("logs/logs.txt", "w", )
BOARD_LOG_FILE = open("logs/board_logs.txt", "w")

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

def showBoard(squares):
    """Shows every square and the pieces that control them"""
    # Clear file first so it only shows latest board
    BOARD_LOG_FILE.truncate(0)
    BOARD_LOG_FILE.seek(0)

    toLog = ""
    for l in range(8):
        for n in range(8):
            sq = squares[l][n]
            toLog += f"{str(sq)}: {sq.getControllingPieces()}\n"
    BOARD_LOG_FILE.write(toLog)
    BOARD_LOG_FILE.flush()

def closeLog():
    print("Closing log file...")
    LOG_FILE.close()
    BOARD_LOG_FILE.close()