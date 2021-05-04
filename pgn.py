""" Schach is a basic chess application that uses the Stockfish chess engine.
    Copyright (C) 2021  Samuel Matzko

    This file is part of Schach.

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
    or see <http://www.gnu.org/licenses/>"""

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
    try: date = headers["Date"]
    except:
        date = time.strftime("%Y.%m.%d")
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

    # Set the headers
    pgn.headers["Date"] = date
    if event:
        pgn.headers["Event"] = event
    if site:
        pgn.headers["Site"] = site
    if date:
        pgn.headers["Date"] = date
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