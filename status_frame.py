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

"""The status frames."""

import gi

import chess

gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")

from constants import *
from gi.repository import Gdk, Gtk, Pango

class _KingLabel(Gtk.HBox):
    """A label with an image and a spinner."""
    
    def __init__(self, image, reverse=False):
        Gtk.HBox.__init__(self)

        # The image
        self.image = image

        # The spinner
        self.spinner = Gtk.Spinner()
        self.spinner.set_size_request(50, 50)

        if not reverse:
            self.pack_start(self.image, False, False, 5)
            self.pack_end(self.spinner, False, False, 5)
        else:
            self.pack_end(self.image, False, False, 5)
            self.pack_start(self.spinner, False, False, 5)

        self.show_all()

class _PieceLabel(Gtk.HBox):
    """A label with an image and text."""

    def __init__(self, image, label, reverse=False):
        Gtk.HBox.__init__(self)

        # The image
        self.image = image

        # The font for the label
        self.font = Pango.FontDescription("30")
        
        # The label
        self.label = Gtk.Label(label=label)
        self.label.modify_font(self.font)

        if not reverse:
            self.pack_start(self.image, False, False, 5)
            self.pack_end(self.label, False, False, 5)
        else:
            self.pack_end(self.image, False, False, 5)
            self.pack_start(self.label, False, False, 5)

        self.show_all()

class _Row(Gtk.ListBoxRow):
    """The base class for the move listbox rows."""

    def __init__(self, *args, move="MOVE", index=0, **kwargs):
        Gtk.ListBoxRow.__init__(self, *args, **kwargs)

        # The move to display in the label, and the move's index in the board's
        # move stack
        self.move = move
        self.index = index

        # The main box
        self.box = Gtk.HBox()
        self.add(self.box)

        # The label
        self.label = Gtk.Label(label=move)
        self.box.pack_start(self.label, True, True, 0)

        self.show_all()
        self.box.show_all()

class _StatusFrame(Gtk.Frame):
    """The base class for the status frames."""

    def __init__(self, *args, color="white", **kwargs):
        Gtk.Frame.__init__(self, *args, **kwargs)

        # The color
        self.color = color

        # The main box
        self.box = Gtk.VBox()
        self.add(self.box)

        # The list of listbox rows
        self.rows = []

        # The number of moves played at the point displayed in the listbox
        self.moves_so_far = 0

        # Set all the variables depending on the color
        if self.color == "white":
            
            # The images
            self.king = Gtk.Image.new_from_file(IMAGE_K)
            self.queen = Gtk.Image.new_from_file(IMAGE_Q)
            self.rook = Gtk.Image.new_from_file(IMAGE_R)
            self.bishop = Gtk.Image.new_from_file(IMAGE_B)
            self.knight = Gtk.Image.new_from_file(IMAGE_N)
            self.pawn = Gtk.Image.new_from_file(IMAGE_P)

            # Whether to reverse the labels and such
            self.reverse = False
        
        else:

            # The images
            self.king = Gtk.Image.new_from_file(IMAGE_k)
            self.queen = Gtk.Image.new_from_file(IMAGE_q)
            self.rook = Gtk.Image.new_from_file(IMAGE_r)
            self.bishop = Gtk.Image.new_from_file(IMAGE_b)
            self.knight = Gtk.Image.new_from_file(IMAGE_n)
            self.pawn = Gtk.Image.new_from_file(IMAGE_p)

            # Whether to reverse the labels and such
            self.reverse = True

        # Create the frame
        self._create_frame()

    def _create_frame(self):
        """Create all the elements of the frame."""

        # The main label
        self.king_label = _KingLabel(self.king, reverse=self.reverse)
        self.box.pack_start(self.king_label, False, False, 5)

        # The status label
        self.status_label = Gtk.Label()
        self.status_label.modify_font(Pango.FontDescription("30"))
        self.status_label.modify_fg(Gtk.StateType.NORMAL, Gdk.Color.from_floats(1.0, 0.0, 0.0))
        self.status_label_box = Gtk.HBox()
        self.box.pack_start(self.status_label_box, False, False, 5)
        if self.reverse:
            self.status_label_box.pack_end(self.status_label, False, False, 5)
        else:
            self.status_label_box.pack_start(self.status_label, False, False, 5)

        # The move listbox and it's ScrolledWindow
        self.move_window = Gtk.ScrolledWindow()
        self.box.pack_start(self.move_window, True, True, 0)
        self.move_listbox = Gtk.ListBox()
        self.move_listbox.connect("event", self._event_handler)
        self.move_window.add(self.move_listbox)

        # The separator
        self.separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.box.pack_start(self.separator, True, False, 5)

        # The labels
        self.queen_label = _PieceLabel(self.queen, "0", reverse=self.reverse)
        self.box.pack_start(self.queen_label, False, False, 1)
        self.rook_label = _PieceLabel(self.rook, "0", reverse=self.reverse)
        self.box.pack_start(self.rook_label, False, False, 1)
        self.bishop_label = _PieceLabel(self.bishop, "0", reverse=self.reverse)
        self.box.pack_start(self.bishop_label, False, False, 1)
        self.knight_label = _PieceLabel(self.knight, "0", reverse=self.reverse)
        self.box.pack_start(self.knight_label, False, False, 1)
        self.pawn_label = _PieceLabel(self.pawn, "0", reverse=self.reverse)
        self.box.pack_start(self.pawn_label, False, False, 1)

        self.show_all()

    def _event_handler(self, listbox, event):
        if event.type == Gdk.EventType.DOUBLE_BUTTON_PRESS:
            index = self.move_listbox.get_selected_row().index
            self.undo_to_move_function(index)

    def bind_undo_to_move(self, func):
        """Bind a row-item double-click to a call of FUNC."""
        self.undo_to_move_function = func

    def set_status(self, board=None, thinking=None, check=None, we_won=None):
        """Set the status of the labels based on the information given."""

        # The board
        if self.color == "white":
            q = "Q"
            r = "R"
            b = "B"
            n = "N"
            p = "P"
        else:
            q = "q"
            r = "r"
            b = "b"
            n = "n"
            p = "p"

        if board is not None:
            self.queen_label.label.set_label(str(str(board).count(q)))
            self.rook_label.label.set_label(str(str(board).count(r)))
            self.bishop_label.label.set_label(str(str(board).count(b)))
            self.knight_label.label.set_label(str(str(board).count(n)))
            self.pawn_label.label.set_label(str(str(board).count(p)))

            # Set the move listbox
            board2 = chess.Board()
            for row in self.rows:
                self.move_listbox.remove(row)
            self.rows = []
            self.moves_so_far = 0
            for move in board.move_stack:
                if (board2.turn and self.color == "white" or
                    not board2.turn and self.color == "black"):
                    row = _Row(move=board2.san(move), index=self.moves_so_far)
                    self.rows.append(row)
                    self.move_listbox.insert(row, 0)
                    self.move_window.do_scroll_child(self.move_window, Gtk.ScrollType.START, False)
                self.moves_so_far += 1
                board2.push(move)
        if thinking is not None:
            if thinking:
                self.king_label.spinner.start()
            else:
                self.king_label.spinner.stop()
        if we_won is not None:
            if we_won:
                self.status_label.set_label("Victory!")
            else:
                self.status_label.set_label("")
        if check is not None:
            if check:
                self.status_label.set_label("Check!")
            else:
                self.status_label.set_label("")

    # In case it wasn't bound
    def undo_to_move_function(self, *args):
        pass

class WhiteStatusFrame(_StatusFrame):
    """The status frame for white."""

    def __init__(self):
        _StatusFrame.__init__(self, color="white")

class BlackStatusFrame(_StatusFrame):
    """The status frame for black."""

    def __init__(self):
        _StatusFrame.__init__(self, color="black")

if __name__ == "__main__":
    window = Gtk.Window()
    window.connect("delete-event", Gtk.main_quit)
    board = chess.Board()
    board.push(chess.Move.from_uci("a2a3"))
    print(board)
    print()
    board.push(chess.Move.from_uci("a7a6"))
    print(board)
    print()
    board.push(chess.Move.from_uci("a3a4"))
    print(board)
    print()
    board.push(chess.Move.from_uci("a6a5"))
    print(board)
    print()
    hbox = Gtk.HBox()
    vbox = Gtk.VBox()
    window.add(hbox)
    hbox.pack_start(vbox, True, True, 5)
    wsf = BlackStatusFrame()
    vbox.pack_start(wsf, True, True, 5)
    wsf.set_status(board=board, thinking=True, we_won=True)
    window.show_all()
    Gtk.main()