import chess
import chess.pgn
import time


def save_game(board, file, headers):
    """Save the current game under the file given.
    
    VALID ARGUMENTS:
        event, site, round, white, black"""
    
    # Get the keyword arguments
    try: event = headers["Event"]
    except:
        event = None
    try: site = headers["Site"]
    except:
        site = None
    try: roundno = headers["Round"]
    except:
        roundno = None
    try: white = headers["White"]
    except:
        white = None
    try: black = headers["Black"]
    except:
        black = None
    try: result = headers["Result"]
    except:
        result = None

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
    if result:
        pgn.headers["Result"] = result

    with open(file, "a") as f:
        f.write(str(pgn) + "\n\n\n")
        f.close()