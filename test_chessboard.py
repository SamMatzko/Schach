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
import gi
import random

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
        image = cairo.ImageSurface.create_from_png("/home/sam/Pictures/Icons/idle.png")
        cr.set_source_surface(image, 200, 200)
        cr.paint()
        image = cairo.ImageSurface.create_from_png("/home/sam/Pictures/Icons/HappyLappyIcon.png")
        cr.set_source_surface(image, 200, 200)
        cr.paint()

class ChessBoard(cairoarea.CairoDrawableArea2):
    """The chessboard widget."""

    def __init__(self, parent=None, string=None, flipped=False):

        cairoarea.CairoDrawableArea2.__init__(self, 560, 560, self._draw)

        # Whether we are flipped or not
        self.flipped = flipped

        # Create the board
        self._create_squares()
        self.set_no_show_all(False)

        if string is not None:
            self.from_string(string)

        # The parent
        self.parent = parent

        # The fuction to call when a square is invoked
        self.square_function = None

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

    def _create_squares(self, flipped=False):
        LETTERS = LETTERS_REVERSED
        NUMBERS = NUMBERS_REVERSED
        LETTERS.reverse()
        NUMBERS.reverse()
        for c in LETTERS:
            for r in NUMBERS:

                # Get the row/column numbers
                cindex = LETTERS.index(c)
                NUMBERS.reverse()
                rindex = NUMBERS.index(r)
                NUMBERS.reverse()

                # Set the color of the square
                if str(c) in ODD_LETTERS:
                    if str(r) in ODD_NUMBERS:
                        color = BLACK
                    else:
                        color = WHITE
                else:
                    if str(r) in ODD_NUMBERS:
                        color = WHITE
                    else:
                        color = BLACK

                # Reset the image
                image = IMAGE_EMPTY
                image_name = "."

                # Set which piece is for this square
                if r == "1":
                    if c == "a" or c == "h":
                        image = IMAGE_R
                        image_name = "R"
                    elif c == "b" or c == "g":
                        image = IMAGE_N
                        image_name = "N"
                    elif c == "c" or c == "f":
                        image = IMAGE_B
                        image_name = "B"
                    elif c == "d":
                        image = IMAGE_Q
                        image_name = "Q"
                    elif c == "e":
                        image = IMAGE_K
                        image_name = "K"
                elif r == "2":
                    image = IMAGE_P
                    image_name = "P"
                elif r == "8":
                    if c == "a" or c == "h":
                        image = IMAGE_r
                        image_name = "r"
                    elif c == "b" or c == "g":
                        image = IMAGE_n
                        image_name = "n"
                    elif c == "c" or c == "f":
                        image = IMAGE_b
                        image_name = "b"
                    elif c == "d":
                        image = IMAGE_q
                        image_name = "q"
                    elif c == "e":
                        image = IMAGE_k
                        image_name = "k"
                elif r == "7":
                    image = IMAGE_p
                    image_name = "p"

                # Execute the squares' creation so that we don't have
                # to type 192 lines
                exec(f"iii = Gtk.Image.new_from_file(image)")
                exec(f"iii.set_name(image_name)")
                exec(f"self.{c}{r} = Square(color='{color}', name='{c}{r}', image=iii)")
                exec(f"self.{c}{r}.color = '{color}'")
                exec(f"self.attach(self.{c}{r}, {cindex + 1}, {rindex + 1}, 1, 1)")

        self.show_all()

    def _get_squares(self):
        """Return a list of the squares."""

        # The list
        l = []

        for c in LETTERS:
            for r in NUMBERS:
                exec(f"l.append(self.{c}{r})")

        return(l)

    def bind_squares(self, func):
        """Bind all the squares at a "clicked" event to a call of function FUNC."""

        # Set the square_function to be called by the squares
        self.square_function = func
        
        # Go through and bind all the squares to self._bound_method.
        # This method then calls func when it is called.
        for square in self._get_squares():
            square.connect("clicked", self._bound_method)

    def from_string(self, string):
        """Rearrange the board according to STRING."""

        string = string.replace("\n", " ").split()
        for sint in range(0, 64):
            s = BOARD_ORDER[sint]
            exec(f"square = self.{s}")
            if string[sint] == ".":
                exec("square.reload(Gtk.Image.new_from_file(IMAGE_EMPTY))")
            else:
                exec(f"iii = Gtk.Image.new_from_file(IMAGE_{string[sint]})")
                exec(f"iii.set_name('{string[sint]}')")
                exec(f"square.reload(iii)")
        self.show_all()

    def get_board_string(self):
        """Return a string giving the board layout."""
        s = ""
        for sq in BOARD_ORDER:          
            for sq2 in self._get_squares():
                if sq2.get_name() == sq:
                    s = s + (sq2.get_piece()) + " "
        if s[len(s) - 1] == " ":
            s = s[:len(s) - 1]
        return s

if __name__ == "__main__":
    window = Gtk.Window()
    window.connect("delete-event", Gtk.main_quit)
    window.add(Area().widget)
    window.show_all()
    Gtk.main()