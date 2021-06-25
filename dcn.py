# Schach is a basic chess application that uses the Stockfish chess engine.
# Copyright (C) 2021  Samuel Matzko

# This file is part of Schach.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
# or see <http://www.gnu.org/licenses/>

"""Game saving module for Schach."""

import chess
import chess.dcn
import time

def save_game(board, file, headers):
    """Save the current game under the file given, replacing the file's contents.

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

    # Create the dcn.Game
    dcn = chess.dcn.Game(board)

    # Set the headers
    dcn.headers["Date"] = date
    if event:
        dcn.headers["Event"] = event
    if site:
        dcn.headers["Site"] = site
    if date:
        dcn.headers["Date"] = date
    if roundno:
        dcn.headers["Round"] = roundno
    if white:
        dcn.headers["White"] = white
    if black:
        dcn.headers["Black"] = black
    if result:
        dcn.headers["Result"] = result
    dcn.create_dcn()

    with open(file, "w") as f:
        f.write(str(dcn) + "\n\n\n")
        f.close()

def save_game_append(board, file, headers):
    """Save the current game under the file given.
    
    VALID ARGUMENTS:
        Event, Site, Round, White, Black"""
    
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

    # Create the dcn.Game
    dcn = chess.dcn.Game(board)

    # Set the headers
    dcn.headers["Date"] = date
    if event:
        dcn.headers["Event"] = event
    if site:
        dcn.headers["Site"] = site
    if date:
        dcn.headers["Date"] = date
    if roundno:
        dcn.headers["Round"] = roundno
    if white:
        dcn.headers["White"] = white
    if black:
        dcn.headers["Black"] = black
    if result:
        dcn.headers["Result"] = result

    with open(file, "a") as f:
        f.write(str(dcn) + "\n\n\n")
        f.close()