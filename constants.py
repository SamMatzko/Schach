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

"""Program constants."""

import gi
import os

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

# The parent directory
ROOT_PATH = f"{os.path.dirname(__file__)}/"

# The config directory
CONFIG_DIR = "%s/.schach/" % os.environ["HOME"]

# The lists of LETTERS and numbers
LETTERS = ["a", "b", "c", "d", "e", "f", "g", "h"]
NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8"]

# The reversed list of letter and numbers
LETTERS_REVERSED = ['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']
NUMBERS_REVERSED = ['8', '7', '6', '5', '4', '3', '2', '1']

# The lists of the odd LETTERS and numbers
ODD_LETTERS = ["a", "c", "e", "g"]
ODD_NUMBERS = ["1", "3", "5", "7"]

# The starting position of the board, as a list
STARTING_POSITION = "r n b q k b n r p p p p p p p p . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . P P P P P P P P R N B Q K B N R".split()

# The list of the order in which to write the pieces to the board
BOARD_ORDER = []

# The square colors
COLOR_MOVEFROM = (0.2, 0.2, 1.0)
COLOR_MOVETO = (0.0, 1.0, 1.0)

# The order in which to write the pieces to the board
for rank in NUMBERS_REVERSED:
    for file in LETTERS:
        BOARD_ORDER.append(f"{file}{rank}")

# The colors
BLACK = "#222222"
WHITE = "#ffffff"
BLACK2 = (0.2, 0.2, 0.2)
WHITE2 = (1.0, 1.0, 1.0)

# The images
IMAGE_EMPTY = f"{ROOT_PATH}icons/pieces/base.png"
IMAGE_K = f"{ROOT_PATH}icons/pieces/64x64/king_w.png"
IMAGE_k = f"{ROOT_PATH}icons/pieces/64x64/king_b.png"
IMAGE_Q = f"{ROOT_PATH}icons/pieces/64x64/queen_w.png"
IMAGE_q = f"{ROOT_PATH}icons/pieces/64x64/queen_b.png"
IMAGE_B = f"{ROOT_PATH}icons/pieces/64x64/bishop_w.png"
IMAGE_b = f"{ROOT_PATH}icons/pieces/64x64/bishop_b.png"
IMAGE_N = f"{ROOT_PATH}icons/pieces/64x64/knight_w.png"
IMAGE_n = f"{ROOT_PATH}icons/pieces/64x64/knight_b.png"
IMAGE_R = f"{ROOT_PATH}icons/pieces/64x64/rook_w.png"
IMAGE_r = f"{ROOT_PATH}icons/pieces/64x64/rook_b.png"
IMAGE_P = f"{ROOT_PATH}icons/pieces/64x64/pawn_w.png"
IMAGE_p = f"{ROOT_PATH}icons/pieces/64x64/pawn_b.png"

IMAGE_APPLICATION = f"{ROOT_PATH}icons/application/appicon.png"

# The audio file
AUDIO_FILE_1 = f"{ROOT_PATH}audio/move1.wav"
AUDIO_FILE_2 = f"{ROOT_PATH}audio/move2.wav"

# The menu .xml file
MENU_XML = f"{ROOT_PATH}ui/menu.xml"

# The application info file
APP_INFO = f"{ROOT_PATH}data/appinfo.json"

# The settings file
SETTINGS_FILE = f"{CONFIG_DIR}settings.json"

# The menu options file
MENU_OPTIONS = f"{ROOT_PATH}data/menuoptions.json"

# The list of filters for the filedialogs
FILE_FILTERS = []
f1 = Gtk.FileFilter()
f1.set_name("Descriptive chess notation (*.dcn)")
f1.add_pattern("*.dcn")
FILE_FILTERS.append(f1)
f2 = Gtk.FileFilter()
f2.set_name("All files")
f2.add_pattern("*.*")
FILE_FILTERS.append(f2)

FILE_FILTERS_PGN = []
f1 = Gtk.FileFilter()
f1.set_name("PGN chess notation (*.pgn)")
f1.add_pattern("*.pgn")
FILE_FILTERS_PGN.append(f1)
f2 = Gtk.FileFilter()
f2.set_name("All files")
f2.add_pattern("*.*")
FILE_FILTERS_PGN.append(f2)