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

class ChessBoard(cairoarea.CairoDrawableArea2):
    """The chessboard widget."""

    def __init__(self, parent=None):

        cairoarea.CairoDrawableArea2.__init__(self, 616, 616, self._draw_board)

        # The variables for board-drawing
        self.LETTERS = LETTERS
        self.NUMBERS = NUMBERS
        self.NUMBERS_REVERSED = NUMBERS_REVERSED
        self.BOARD_ORDER = BOARD_ORDER

        # The event-handling methods
        self.enter_notify_func = self._func_enter_notify
        self.leave_notify_func = self._func_leave_notify
        self.motion_notify_func = self._func_motion_notify
        self.mouse_scroll_func = self._func_mouse_scroll
        self.press_func = self._func_press
        self.release_func = self._func_release

        # The methods to call on piece placement
        self._bound_place_method = None

        # The size of the squares
        self.square_size = 77

        # Whether we are flipped or not
        self.flipped = False

        # The parent
        self.parent = parent

        # Move data
        self.move = None
        self.move_from = None
        self.move_to = None

        # The chessboard-drawing variables
        self.squaresdict = {}
        self.squaresonly = False

        # The string that contains the board's current position
        self.string = STARTING_POSITION

        self.show_all()

    def _draw_board(self, event, cr, allocation):
        x, y, w, h = allocation
        cr.set_source_rgb(0.0, 0.0, 0.0)
        cr.rectangle(0, 0, w, h)
        cr.fill()
        for c in self.LETTERS:
            for r in self.NUMBERS:

                square = "%s%s" % (c, r)

                # Get the row/column numbers
                cindex, rindex = self.convert_square_to_coords(square)

                # Set the color of the square
                color = self.convert_square_to_color(square)

                # Set which piece is for this square
                image, image_name = self.convert_square_to_image(square)

                # Create the squares
                if self.squaresdict is not None:
                    try: color = self.squaresdict["%s%s" % (c, r)]
                    except:
                        pass
                exec(f"cr.set_source_rgb(*color)")
                exec(f"cr.rectangle(cindex * self.square_size, rindex * self.square_size, self.square_size, self.square_size)")
                exec("cr.fill()")
                if not self.squaresonly:
                    exec(f"cr.set_source_surface(cairo.ImageSurface.create_from_png(image), (cindex * self.square_size) + 5, (rindex * self.square_size) + 5)")
                    exec(f"cr.paint()")

        self.show_all()

    def _func_enter_notify(self, event):
        """Event handler for enter notifications."""
        pass

    def _func_leave_notify(self, event):
        """Event handler for leave notifications."""
        pass

    def _func_motion_notify(self, x, y, state):
        """Event handler for motion notifications."""
        pass

    def _func_mouse_scroll(self, event):
        """Event handler for mouse scrolls."""
        pass
    
    def _func_press(self, event):
        """Event handler for button presses."""
        
        square = self.convert_screen_coords_to_square((event.x, event.y))
        self._bound_place_method(square)
        self.update()

    def _func_release(self, event):
        """Event handler for buttons releases."""
        pass

    def bind_place(self, func):
        """Bind the board to a call of FUNC when a move is made."""
        self._bound_place_method = func

    def convert_row_column_to_square(self, coords):
        """COORDS must be a tuple of (row, column). Returns a square, "a2" for example."""
        row = coords[0]
        column = coords[1]
        return "%s%s" % (self.LETTERS[column], self.NUMBERS_REVERSED[row])

    def convert_screen_coords_to_square(self, coords):
        """COORDS must be a tuple of (x, y). Returns a square, "a2" for example."""
        x, y = coords
        c, r = int(str(x / self.square_size)[0]), int(str(y / self.square_size)[0])
        return self.convert_row_column_to_square((r, c))

    def convert_square_to_color(self, square):
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

    def convert_square_to_coords(self, square):
        """SQUARE must be in "a4" format. Returns a tuple (c, r)."""
        c = square[0]
        r = square[1]
        return (self.LETTERS.index(c), self.NUMBERS_REVERSED.index(r))
    
    def convert_square_to_image(self, square):
        """SQUARE must be in "a4" format. Returns the file path."""
        c = square[0]
        r = square[1]
        piece = self.string[self.BOARD_ORDER.index(square)]
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

    def flip(self):
        """Flip the chessboard."""
        if self.flipped:
            self.LETTERS = LETTERS
            self.NUMBERS = NUMBERS
            self.NUMBERS_REVERSED = NUMBERS_REVERSED
        else:
            self.LETTERS = LETTERS_REVERSED
            self.NUMBERS = NUMBERS_REVERSED
            self.NUMBERS_REVERSED = NUMBERS
        self.flipped = not self.flipped
        self.update()

    def from_board(self, board):
        """Rearrange the board according to BOARD."""
        string = str(board).replace("\n", " ").split()
        self.squaresonly = False
        self.string = string
        self.update()

    def place(self, piece, square):
        """Place PIECE at SQUARE."""
        self.string[self.BOARD_ORDER.index(square)] = piece
        self.update()

    def update(self):
        """Update the chessboard."""
        self.hide()
        self.show_all()

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
    board = chess.Board()
    def m(*args):
        print(args)
        return board
    chessboard.bind_place(m)
    Gtk.main()