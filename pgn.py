import chess
import chess.pgn
import time


def save_game(board, file, **kw):
    """Save the current game under the file given.
    
    VALID ARGUMENTS:
        event, site, round, white, black"""
    
    # Get the keyword arguments
    try: event = kw["event"]
    except:
        event = None
    try: site = kw["site"]
    except:
        site = None
    try: roundno = kw["round"]
    except:
        roundno = None
    try: white = kw["white"]
    except:
        white = None
    try: black = kw["black"]
    except:
        black = None

    # Create the pgn.Game
    pgn = chess.pgn.Game.from_board(board)

    # Get the date for the header
    date = time.strftime("%Y.%m.%d")

    # Set the headers
    pgn.headers["Date"] = date
    if event:
        pgn.headers["Event"] = event
    if site:
        pgn.headers["Site"] = site
    if roundno:
        pgn.headers["Round"] = roundno
    if white:
        pgn.headers["White"] = white
    if black:
        pgn.headers["Black"] = black

    with open(file, "a") as f:
        f.write(str(pgn) + "\n\n\n")
        f.close()