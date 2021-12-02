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

"""Pgn-format game saving module for Schach."""

import io
import time

import chess
import chess.pgn

def load_file(file):
    """Load the games from FILE."""

    # Check the file's type before reading it
    if type(file) == type(""):
        with open(file) as f:
            games = f.read()
            f.close()
    else:
        games = file.read()
        file.close()

    # Separate the games in the string, and add a chess.dcn.Game instance to
    # the game_list for each game
    game_list = []
    games = games.split("\n\n\n")
    for game in games:
        if game != "":
            pgn_game = chess.pgn.read_game(io.StringIO(game))
            if pgn_game is not None:
                game_list.append(pgn_game)

    return game_list

def save_game(game, file):
    """Save GAME to FILE in pgn format."""

    with open(file, "w") as f:
        f.write(str(game) + "\n\n\n")
        f.close()

def save_game_append(game, file):
    """Save GAME appending to FILE in pgn format."""

    with open(file, "a") as f:
        f.write(str(game) + "\n\n\n")
        f.close()