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

import cairo
import cairoarea
import chess
import gi
import random
import time

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")

from constants import *
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import Gtk

class Area:

    def __init__(self):
        self.widget = cairoarea.CairoDrawableArea2(
            500,
            500,
            self._draw
        )

    def _draw(self, event, cr, allocation):
        x, y, w, h = allocation
        for x in range(0, 3):
            image = cairo.ImageSurface.create_from_png("/home/sam/Pictures/Icons/idle.png")
            cr.set_source_surface(image, 50 * x, 50 * x)
            cr.paint()

class ChessBoard(cairoarea.CairoDrawableArea2):
    """The chessboard widget."""

    def __init__(self, parent=None, string=None, flipped=False):

        cairoarea.CairoDrawableArea2.__init__(self, 560, 560, self._create_squares)

        # Whether we are flipped or not
        self.flipped = flipped

        # # Create the board
        # self._create_squares()
        # self.set_no_show_all(False)

        # if string is not None:
            # self.from_string(string)

        # The parent
        self.parent = parent

        # The fuction to call when a square is invoked
        self.square_function = None

        # The chessboard-drawing variables
        self.squaresdict = {}
        self.squaresonly = False

        # The string that contains the board's current position
        self.string = \
        "r n b q k b n r p p p p p p p p . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . P P P P P P P P R N B Q K B N R".split()

        self.show_all()

    def _bound_method(self, widget):
        """The method called when a square is invoked."""

        # Call the method if it exists
        if self.square_function != None:
            self.square_function(
                {
                    "square": widget,
                    "location": widget.get_name(),
                    "piece": widget.get_piece()
                }
            )
        else:
            raise TypeError("Cannot call type 'None'.")

    def _convert_square_to_color(self, square):
        """SQUARE must be in "a4" format. Returns either BLACK2 or WHITE2."""
        c = square[0]
        r = square[1]
        if str(c) in ODD_LETTERS:
            if str(r) in ODD_NUMBERS:
                color = BLACK2
            else:
                color = WHITE2
        else:
            if str(r) in ODD_NUMBERS:
                color = WHITE2
            else:
                color = BLACK2
        return color

    def _convert_square_to_coords(self, square):
        """SQUARE must be in "a4" format. Returns a tuple (c, r)."""
        c = square[0]
        r = square[1]
        return (LETTERS.index(c), NUMBERS_REVERSED.index(r))
    
    def _convert_square_to_image(self, square):
        """SQUARE must be in "a4" format. Returns the file path."""
        c = square[0]
        r = square[1]
        piece = self.string[BOARD_ORDER.index(square)]
        image = IMAGE_EMPTY
        if piece == "K":
            image = IMAGE_K
        elif piece == "Q":
            image = IMAGE_Q
        elif piece == "R":
            image = IMAGE_R
        elif piece == "B":
            image = IMAGE_B
        elif piece == "N":
            image = IMAGE_N
        elif piece == "P":
            image = IMAGE_P

        elif piece == "k":
            image = IMAGE_k
        elif piece == "q":
            image = IMAGE_q
        elif piece == "r":
            image = IMAGE_r
        elif piece == "b":
            image = IMAGE_b
        elif piece == "n":
            image = IMAGE_n
        elif piece == "p":
            image = IMAGE_p
        return image, piece

    def _create_squares(self, event, cr, allocation):
        x, y, w, h = allocation
        cr.set_source_rgb(0.0, 0.0, 0.0)
        cr.rectangle(0, 0, w, h)
        cr.fill()
        for c in LETTERS:
            for r in NUMBERS:

                square = "%s%s" % (c, r)

                # Get the row/column numbers
                cindex, rindex = self._convert_square_to_coords(square)

                # Set the color of the square
                color = self._convert_square_to_color(square)

                # Set which piece is for this square
                image, image_name = self._convert_square_to_image(square)

                # Create the squares
                if self.squaresdict is not None:
                    try: color = self.squaresdict["%s%s" % (c, r)]
                    except:
                        pass
                exec(f"cr.set_source_rgb(*color)")
                exec(f"cr.rectangle(cindex * 70, rindex * 70, 70, 70)")
                exec("cr.fill()")
                if not self.squaresonly:
                    exec(f"cr.set_source_surface(cairo.ImageSurface.create_from_png(image), (cindex * 70) + 3, (rindex * 70) + 3)")
                    exec(f"cr.paint()")

        self.show_all()

    def from_string(self, string):
        """Rearrange the board according to STRING."""

        string = string.replace("\n", " ").split()
        self.squaresonly = False
        self.string = string

if __name__ == "__main__":
    window = Gtk.Window()
    window.connect("delete-event", Gtk.main_quit)
    box = Gtk.VBox()
    box2 = Gtk.HBox()
    box2.pack_start(box, False, False, 0)
    chessboard = ChessBoard(window)
    box.pack_start(chessboard, False, False, 0)
    window.add(box2)
    window.show_all()
    board = chess.Board("rnbqkb1r/ppp1pppp/5n2/3p4/3P1B2/2P5/PP2PPPP/RN1QKBNR")
    chessboard.from_string(str(board))
    Gtk.main()