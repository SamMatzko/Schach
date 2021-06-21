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

"""The main dialogs."""

import chess
import chess.pgn
import gi
import io
import json
import setup_chessboard
import string

gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")

from constants import *
from gi.repository import Gtk, Gdk, GdkPixbuf

class _Dialog(Gtk.Dialog):
    """The base class for the dialogs."""

    def __init__(self, *args, **kwargs):
        Gtk.Dialog.__init__(self, *args, **kwargs)
        self.set_resizable(False)

        # Connect "escape" so that the dialog closes
        self.connect("key-press-event", self._on_key_press)
        self.connect("delete-event", self._destroy)

    def _destroy(self, *args):
        """Destroy the dialog."""
        self.destroy()

    def _on_key_press(self, widget, event):
        """Close the dialog if the key pressed was "escape"."""
        if event.keyval == Gdk.KEY_Escape:
            self._destroy()

class AboutDialog:
    """The class that handles the about dialog."""

    def __init__(self, parent, info):
        self.dialog = Gtk.AboutDialog(
            transient_for=parent,
            modal=True
        )
        self.dialog.set_artists(info["artists"])
        self.dialog.set_authors(info["authors"])
        self.dialog.set_comments(info["comments"])
        self.dialog.set_copyright(info["copyright"])
        self.dialog.set_license(info["license"])
        pixbuf = GdkPixbuf.Pixbuf().new_from_file_at_size(info["logo"], 100, 100)
        pixbuf
        self.dialog.set_logo(pixbuf)
        self.dialog.set_program_name(info["program_name"])
        self.dialog.set_version(info["version"])
    
    def present(self):
        self.dialog.present()

class BoardSetupDialog(_Dialog):
    """A dialog to get a setup board from the user."""

    def __init__(self, parent):
        _Dialog.__init__(
            self,
            title="Board Setup",
            transient_for=parent,
            modal=True
        )

        # The area to which we can add everything
        self.area = self.get_content_area()

        # Add the buttons
        buttons = (
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL),
            (Gtk.STOCK_OK, Gtk.ResponseType.OK)
        )
        for button in buttons:
            self.add_button(*button)

        # The current piece to be adding to the board
        self.current_piece = "."

        # The board
        self.board = chess.Board()

        # Create the dialog
        self._create_dialog()

        self.show_all()

    def _create_board_settings(self):
        """Add all the settings widgets."""
        
        # The box
        self.board_settings_box = Gtk.VBox()
        self.secondary_box.pack_end(self.board_settings_box, True, True, 5)

        # The piece buttons and boxes
        self.b1 = Gtk.HBox()
        self.board_settings_box.pack_start(self.b1, False, True, 5)
        self.b2 = Gtk.HBox()
        self.board_settings_box.pack_start(self.b2, False, True, 5)
        self.b3 = Gtk.HBox()
        self.board_settings_box.pack_start(self.b3, False, True, 5)
        self.b4 = Gtk.HBox()
        self.board_settings_box.pack_start(self.b4, False, True, 5)
        self.b5 = Gtk.HBox()
        self.board_settings_box.pack_start(self.b5, False, True, 5)
        self.b6 = Gtk.HBox()
        self.board_settings_box.pack_start(self.b6, False, True, 5)

        self.pawn_w_button = Gtk.ToggleButton()
        self.pawn_w_button_image = Gtk.Image.new_from_file(IMAGE_P)
        self.pawn_w_button.set_image(self.pawn_w_button_image)
        self.pawn_w_button.connect("toggled", self._on_button_toggle, "P")
        self.b1.pack_start(self.pawn_w_button, False, False, 3)

        self.knight_w_button = Gtk.ToggleButton()
        self.knight_w_button_image = Gtk.Image.new_from_file(IMAGE_N)
        self.knight_w_button.set_image(self.knight_w_button_image)
        self.knight_w_button.connect("toggled", self._on_button_toggle, "N")
        self.b2.pack_start(self.knight_w_button, False, False, 3)

        self.bishop_w_button = Gtk.ToggleButton()
        self.bishop_w_button_image = Gtk.Image.new_from_file(IMAGE_B)
        self.bishop_w_button.set_image(self.bishop_w_button_image)
        self.bishop_w_button.connect("toggled", self._on_button_toggle, "B")
        self.b3.pack_start(self.bishop_w_button, False, False, 3)

        self.rook_w_button = Gtk.ToggleButton()
        self.rook_w_button_image = Gtk.Image.new_from_file(IMAGE_R)
        self.rook_w_button.set_image(self.rook_w_button_image)
        self.rook_w_button.connect("toggled", self._on_button_toggle, "R")
        self.b4.pack_start(self.rook_w_button, False, False, 3)

        self.queen_w_button = Gtk.ToggleButton()
        self.queen_w_button_image = Gtk.Image.new_from_file(IMAGE_Q)
        self.queen_w_button.set_image(self.queen_w_button_image)
        self.queen_w_button.connect("toggled", self._on_button_toggle, "Q")
        self.b5.pack_start(self.queen_w_button, False, False, 3)

        self.king_w_button = Gtk.ToggleButton()
        self.king_w_button_image = Gtk.Image.new_from_file(IMAGE_K)
        self.king_w_button.set_image(self.king_w_button_image)
        self.king_w_button.connect("toggled", self._on_button_toggle, "K")
        self.b6.pack_start(self.king_w_button, False, False, 3)

        self.pawn_b_button = Gtk.ToggleButton()
        self.pawn_b_button_image = Gtk.Image.new_from_file(IMAGE_p)
        self.pawn_b_button.set_image(self.pawn_b_button_image)
        self.pawn_b_button.connect("toggled", self._on_button_toggle, "p")
        self.b1.pack_start(self.pawn_b_button, False, False, 3)

        self.knight_b_button = Gtk.ToggleButton()
        self.knight_b_button_image = Gtk.Image.new_from_file(IMAGE_n)
        self.knight_b_button.set_image(self.knight_b_button_image)
        self.knight_b_button.connect("toggled", self._on_button_toggle, "n")
        self.b2.pack_start(self.knight_b_button, False, False, 3)

        self.bishop_b_button = Gtk.ToggleButton()
        self.bishop_b_button_image = Gtk.Image.new_from_file(IMAGE_b)
        self.bishop_b_button.set_image(self.bishop_b_button_image)
        self.bishop_b_button.connect("toggled", self._on_button_toggle, "b")
        self.b3.pack_start(self.bishop_b_button, False, False, 3)

        self.rook_b_button = Gtk.ToggleButton()
        self.rook_b_button_image = Gtk.Image.new_from_file(IMAGE_r)
        self.rook_b_button.set_image(self.rook_b_button_image)
        self.rook_b_button.connect("toggled", self._on_button_toggle, "r")
        self.b4.pack_start(self.rook_b_button, False, False, 3)

        self.queen_b_button = Gtk.ToggleButton()
        self.queen_b_button_image = Gtk.Image.new_from_file(IMAGE_q)
        self.queen_b_button.set_image(self.queen_b_button_image)
        self.queen_b_button.connect("toggled", self._on_button_toggle, "q")
        self.b5.pack_start(self.queen_b_button, False, False, 3)

        self.king_b_button = Gtk.ToggleButton()
        self.king_b_button_image = Gtk.Image.new_from_file(IMAGE_k)
        self.king_b_button.set_image(self.king_b_button_image)
        self.king_b_button.connect("toggled", self._on_button_toggle, "k")
        self.b6.pack_start(self.king_b_button, False, False, 3)

    def _create_dialog(self):
        """Add all the widgets to the dialog."""

        # The main box
        self.main_box = Gtk.VBox()
        self.area.add(self.main_box)

        # The secondary box
        self.secondary_box = Gtk.HBox()
        self.main_box.add(self.secondary_box)

        # The chessboard
        self.chessboard = setup_chessboard.ChessBoard(self)
        self.chessboard.bind_place(self._place_func)

        # The extra box for the chessboard
        self.chessboard_box = Gtk.VBox()
        self.secondary_box.pack_start(self.chessboard_box, False, False, 5)
        self.chessboard_box.pack_start(self.chessboard, False, False, 5)

        # The entry containing the fen
        self.fen_entry = Gtk.Entry()
        self.fen_entry.set_editable(False)
        self.fen_entry.set_tooltip_text("Board FEN")
        self.main_box.pack_end(self.fen_entry, False, True, 3)

        # The board settings buttons
        self._create_board_settings()

    def _get_chess_piece(self, piece):
        """Return a chess.Piece instance for string PIECE."""
        if piece == "K":
            return chess.Piece(chess.KING, chess.WHITE)
        elif piece == "Q":
            return chess.Piece(chess.QUEEN, chess.WHITE)
        elif piece == "R":
            return chess.Piece(chess.ROOK, chess.WHITE)
        elif piece == "B":
            return chess.Piece(chess.BISHOP, chess.WHITE)
        elif piece == "N":
            return chess.Piece(chess.KNIGHT, chess.WHITE)
        elif piece == "P":
            return chess.Piece(chess.PAWN, chess.WHITE)
        
        elif piece == "k":
            return chess.Piece(chess.KING, chess.BLACK)
        elif piece == "q":
            return chess.Piece(chess.QUEEN, chess.BLACK)
        elif piece == "r":
            return chess.Piece(chess.ROOK, chess.BLACK)
        elif piece == "b":
            return chess.Piece(chess.BISHOP, chess.BLACK)
        elif piece == "n":
            return chess.Piece(chess.KNIGHT, chess.BLACK)
        elif piece == "p":
            return chess.Piece(chess.PAWN, chess.BLACK)
        else:
            return chess.Piece(chess.BB_EMPTY, chess.WHITE)

    def _on_button_toggle(self, button, piece):
        """Handle events when a button is toggled."""
        print(button, piece)
        
    def _place_func(self, square):
        """The method to be called when the chessboard is clicked."""
        self.chessboard.place(self.current_piece, square)
        self.board.set_piece_at(BOARD_ORDER.index(square), self._get_chess_piece(self.current_piece))

    def _update(self):
        """Update everything."""
        self.fen_entry.set_text(self.board.fen())

    def show_dialog(self):
        """Show the dilaog."""
        response = self.run()
        self.destroy()
        return response

class CalendarDialog(_Dialog):
    """A dialog to get a date response from the user using a calendar."""
    
    def __init__(self, parent):
        _Dialog.__init__(
            self,
            title="Choose a date",
            transient_for=parent,
            modal=True
        )

        # The area to which we can add the calendar
        self.area = self.get_content_area()

        # The calendar
        self.calendar = Gtk.Calendar()
        self.area.add(self.calendar)

        # The buttons
        buttons = (
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL),
            (Gtk.STOCK_OK, Gtk.ResponseType.OK)
        )

        # Add the buttons
        for button in buttons:
            self.add_button(button[0], button[1])

        self.show_all()

    def show_dialog(self):
        """Show the dialog."""

        # Run the dialog
        response = self.run()

        # Get the date from the calendar
        dateorg = self.calendar.get_date()

        # Set the month to one ahead, because the calendar returns
        # January as 0, February as 1, etc.
        date = (dateorg[0], dateorg[1] + 1, dateorg[2])

        # Destory us
        self.destroy()

        # Return the response and date
        return response, date

class FileOpen:
    """An Open File dialog
    
    Valid options: initialdir, parent, title"""

    def __init__(self, **kw):

        try: self.title = kw["title"]
        except:
            self.title = "Open File"

        try: self.initialdir = kw["initialdir"]
        except:
            self.initialdir = None

        try: self.parent = kw["parent"]
        except:
            self.parent = None

        try: self.filters = kw["filters"]
        except:
            self.filters = None
        
        # The dialog
        self.dialog = Gtk.FileChooserDialog(title=self.title, parent=self.parent, transient_for=self.parent,
            modal=True, action=Gtk.FileChooserAction.OPEN)
        self.dialog.add_buttons("Cancel", Gtk.ResponseType.CANCEL, "OK", Gtk.ResponseType.ACCEPT)
        self.dialog.set_action(Gtk.FileChooserAction.OPEN)
        if self.initialdir:
            self.dialog.set_current_folder(self.initialdir)
        if self.filters:
            for f in self.filters:
                self.dialog.add_filter(f)
        self.dialog.set_select_multiple(False)
        self.dialog.connect("response", self.callback)

    def callback(self, dialog=None, response=None, whoknows=None):
        """The method to be called when the user responds to the file dialog."""
        self.filenames = self.dialog.get_filenames()
        self.response = response
        self.dialog.destroy()

    def show(self):
        """Show the dialog."""
        self.dialog.show()
        while self.dialog.get_mapped():
            Gtk.main_iteration()
        if self.response == Gtk.ResponseType.ACCEPT:
            return self.filenames[0]
        else:
            return None

class FileSaveAs:
    """A Save File As dialog.
    
    Valid options: initialdir, parent"""

    def __init__(self, **kw):

        try: self.initialdir = kw["initialdir"]
        except:
            self.initialdir = None

        try: self.parent = kw["parent"]
        except:
            self.parent = None

        try: self.filters = kw["filters"]
        except:
            self.filters = None

        self.dialog = Gtk.FileChooserDialog(parent=self.parent, transient_for=self.parent,
            modal=True, action=Gtk.FileChooserAction.SAVE)
        self.dialog.add_buttons("Cancel", Gtk.ResponseType.CANCEL, "Save", Gtk.ResponseType.ACCEPT)
        self.dialog.set_action(Gtk.FileChooserAction.SAVE)
        self.dialog.set_do_overwrite_confirmation(True)
        if self.initialdir:
            self.dialog.set_current_folder(self.initialdir)
        if self.filters:
            for f in self.filters:
                self.dialog.add_filter(f)
        self.dialog.set_select_multiple(False)
        self.dialog.connect('response', self.callback)
        self.dialog.show()

    def callback(self, dialog=None, response=None, whoknows=None):
        """The method to be called when the user responds to the file dialog."""
        self.filenames = self.dialog.get_filenames()
        self.response = response
        self.dialog.destroy()

    def show(self):
        """Show the dialog."""
        self.dialog.show()
        while self.dialog.get_mapped():
            Gtk.main_iteration()
        if self.response == Gtk.ResponseType.ACCEPT:
            return self.filenames[0]
        else:
            return None

class GameSelectorDialog(_Dialog):
    """The dialog to prompt the user to choose a game from a loaded file."""

    def __init__(self, parent, games):
        _Dialog.__init__(
            self,
            title="Select a Game",
            transient_for=parent,
            modal=True
        )
        self.set_default_size(500, 300)

        # The area to which we can add the list of games in the file
        self.area = self.get_content_area()

        # The games file
        self.games_file = games

        # The list of the games' strings
        self.game_strings = self.games_file.split("\n\n\n")

        # The list of chess.pgn.Game instances
        self.games = []
        for game in self.game_strings:
            game_instance = chess.pgn.read_game(io.StringIO(game))
            if game_instance is not None:
                self.games.append(game_instance)

        # The listbox for the games
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.listbox.connect("row-activated", self._on_row_activated)

        self.listbox_box = Gtk.ScrolledWindow()
        self.listbox_box.add(self.listbox)
        self.area.pack_start(self.listbox_box, True, True, 0)

        # The list of rows
        self.rows = []

        # Add the games to the listbox
        for game in self.games:
            row = Gtk.ListBoxRow()
            self.rows.append(row)
            row.game_instance = game
            hbox = Gtk.HBox()
            hbox.add(
                Gtk.Label(
                    label="%s vs. %s" % (game.headers["White"], game.headers["Black"])
                )
            )
            hbox.show_all()
            row.add(hbox)
            self.listbox.add(row)

        self.listbox.select_row(self.rows[0])
        self.game_selected = self.games[0]

        # Add the buttons
        buttons = (
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL),
            (Gtk.STOCK_OK, Gtk.ResponseType.OK)
        )
        for button in buttons:
            self.add_button(button[0], button[1])

        self.show_all()

    def _on_row_activated(self, listbox, row):
        self.game_selected = row.game_instance

    def show_dialog(self):
        
        # Run us
        response = self.run()

        # Destroy us
        self.destroy()

        return response, self.game_selected

class HeadersDialog(_Dialog):
    """The dialog in which users can edit the game's headers.
    
    Valid results for OVERRIDE_RESULT are:
        1 - 0, 0 - 1, 1/2 - 1/2, and *"""

    def __init__(self, parent, title, override_result=None):
        _Dialog.__init__(
            self,
            title=title,
            transient_for=parent,
            modal=True)

        # The area to which we can add everything
        self.area = self.get_content_area()

        # The box containing the headers
        self.headers_box = Gtk.VBox()

        # The dictionary containing the headers given by the user
        self.headers = None

        # The default result vaule; this is to prevent errors
        self.result = "*"

        # Whether the result of the game has already been determined
        self.override_result = override_result

        # Create the headers box
        self._create_headers_box()

        # Set the buttons
        self._create_buttons()

        self.show_all()

    def _create_buttons(self):
        """Create the buttons of the dialog."""

        # The buttons
        buttons = (
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL),
            (Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
        )

        # Add the buttons
        for button in buttons:
            self.add_button(button[0], button[1])

    def _create_headers_box(self):
        """Create all the header editing elements and add them to the header box."""

        # The event header
        self.event_header_box = Gtk.HBox()
        self.area.pack_start(self.event_header_box, True, True, 2)
        self.event_header_label = Gtk.Label(label="Event: ")
        self.event_header_entry = Gtk.Entry()
        self.event_header_box.pack_start(self.event_header_label, False, False, 2)
        self.event_header_box.pack_end(self.event_header_entry, False, False, 2)

        # The site header
        self.site_header_box = Gtk.HBox()
        self.area.pack_start(self.site_header_box, True, True, 2)
        self.site_header_label = Gtk.Label(label="Site: ")
        self.site_header_entry = Gtk.Entry()
        self.site_header_box.pack_start(self.site_header_label, False, False, 2)
        self.site_header_box.pack_end(self.site_header_entry, False, False, 2)

        # The date header
        self.date_header_box = Gtk.HBox()
        self.area.pack_start(self.date_header_box, True, True, 2)
        self.date_header_label = Gtk.Label(label="Date:")
        self.date_header_box.pack_start(self.date_header_label, False, False, 2)

        # The date header entries
        self.date_header_entry_box = Gtk.HBox()
        Gtk.StyleContext.add_class(self.date_header_entry_box.get_style_context(), "linked")
        self.date_header_box.pack_end(self.date_header_entry_box, False, False, 2)

        self.date_header_year_entry = Gtk.Entry()
        self.date_header_year_entry.set_width_chars(4)
        self.date_header_year_entry.set_max_length(4)
        self.date_header_year_entry.insert_text("????", 0)
        self.date_header_year_entry.connect("event", self._on_entry_edit)
        self.date_header_entry_box.pack_start(self.date_header_year_entry, False, False, 0)

        self.date_header_entry_box.pack_start(Gtk.Label(label="/"), False, False, 1)

        self.date_header_month_entry = Gtk.Entry()
        self.date_header_month_entry.set_width_chars(2)
        self.date_header_month_entry.set_max_length(2)
        self.date_header_month_entry.insert_text("??", 0)
        self.date_header_month_entry.connect("event", self._on_entry_edit)
        self.date_header_entry_box.pack_start(self.date_header_month_entry, False, False, 0)

        self.date_header_entry_box.pack_start(Gtk.Label(label="/"), False, False, 1)

        self.date_header_day_entry = Gtk.Entry()
        self.date_header_day_entry.set_width_chars(2)
        self.date_header_day_entry.set_max_length(2)
        self.date_header_day_entry.insert_text("??", 0)
        self.date_header_day_entry.connect("event", self._on_entry_edit)
        self.date_header_entry_box.pack_start(self.date_header_day_entry, False, False, 0)

        # The calendar button
        self.calendar_button = Gtk.Button.new_from_icon_name("x-office-calendar-symbolic", 1)
        self.calendar_button.connect("clicked", self._on_calendar_clicked)
        self.date_header_entry_box.pack_start(self.calendar_button, False, False, 0)

        # The round header
        self.round_header_box = Gtk.HBox()
        self.area.pack_start(self.round_header_box, True, True, 2)
        self.round_header_label = Gtk.Label(label="Round: ")
        self.round_header_entry = Gtk.Entry()
        self.round_header_box.pack_start(self.round_header_label, False, False, 2)
        self.round_header_box.pack_end(self.round_header_entry, False, False, 2)

        # The white header
        self.white_header_box = Gtk.HBox()
        self.area.pack_start(self.white_header_box, True, True, 2)
        self.white_header_label = Gtk.Label(label="White: ")
        self.white_header_entry = Gtk.Entry()
        self.white_header_box.pack_start(self.white_header_label, False, False, 2)
        self.white_header_box.pack_end(self.white_header_entry, False, False, 2)

        # The black header
        self.black_header_box = Gtk.HBox()
        self.area.pack_start(self.black_header_box, True, True, 2)
        self.black_header_label = Gtk.Label(label="Black: ")
        self.black_header_entry = Gtk.Entry()
        self.black_header_box.pack_start(self.black_header_label, False, False, 2)
        self.black_header_box.pack_end(self.black_header_entry, False, False, 2)
        
        # The result header
        self.result_header_box = Gtk.HBox()
        self.area.pack_start(self.result_header_box, True, True, 2)
        self.result_header_label = Gtk.Label(label="Result: ")
        self.result_header_box.pack_start(self.result_header_label, False, False, 2)

        # The result options
        self.results_box = Gtk.HBox()
        self.result_header_box.pack_end(self.results_box, True, True, 2)
        self.result_w_b = Gtk.RadioButton.new_with_label_from_widget(None, "1 - 0")
        self.result_w_b.connect("toggled", self._on_result_set, "0")
        self.results_box.pack_start(self.result_w_b, False, False, 2)
        self.result_b_w = Gtk.RadioButton.new_from_widget(self.result_w_b)
        self.result_b_w.set_label("0 - 1")
        self.result_b_w.connect("toggled", self._on_result_set, "1")
        self.results_box.pack_start(self.result_b_w, False, False, 2)
        self.result_1_2 = Gtk.RadioButton.new_from_widget(self.result_w_b)
        self.result_1_2.set_label("1/2 - 1/2")
        self.result_1_2.connect("toggled", self._on_result_set, "2")
        self.results_box.pack_start(self.result_1_2, False, False, 2)
        self.result_unfinished = Gtk.RadioButton.new_from_widget(self.result_w_b)
        self.result_unfinished.set_label("*")
        self.result_unfinished.connect("toggled", self._on_result_set, "3")
        self.results_box.pack_start(self.result_unfinished, False, False, 2)

        # Set whether the user is allowed to set the result
        if self.override_result is not None:
            self.result = self.override_result

            # Set the result radiobutton
            if self.result == "1 - 0":
                self.result_w_b.set_active(True)
            elif self.result == "0 - 1":
                self.result_b_w.set_active(True)
            elif self.result == "1/2 - 1/2":
                self.result_1_2.set_active(True)
            else:
                self.result_unfinished.set_active(True)

            # Set the radiobuttons insensitive
            self.result_header_box.set_sensitive(False)

    def _destroy(self, *args):
        """Close the dialog properly."""

        if self.headers == None:
    
            # Set the headers variable to a dictionary
            self.headers = {}

            # Get all the info for the headers
            self.headers["Event"] = self.event_header_entry.get_text()
            self.headers["Site"] = self.site_header_entry.get_text()
            self.headers["Date"] = "%s.%s.%s" % (
                self.date_header_year_entry.get_text(),
                self.date_header_month_entry.get_text(),
                self.date_header_day_entry.get_text()
            )
            self.headers["Round"] = self.round_header_entry.get_text()
            self.headers["White"] = self.white_header_entry.get_text()
            self.headers["Black"] = self.black_header_entry.get_text()
            self.headers["Result"] = self.result
        
        # Destroy us
        self.destroy()

    def _on_calendar_clicked(self, button):
        """Get the date from the calendar."""

        # The calendar dialog
        dialog = CalendarDialog(self)
        response, date = dialog.show_dialog()

        # Set the date labels
        self.date_header_year_entry.set_text(str(date[0]))
        self.date_header_month_entry.set_text(str(date[1]))
        self.date_header_day_entry.set_text(str(date[2]))

    def _on_entry_edit(self, w, e):
        """Remove invalid characters from the date entries."""

        # If the user has left the entry...
        if e.type == Gdk.EventType.LEAVE_NOTIFY or e.type == Gdk.EventType.FOCUS_CHANGE:
            
            # ...for each character in the entry's text...
            for l in w.get_text():
                # ...if the character is not a digit...
                if l not in string.digits and l != "?":

                    # ...set the entry to the default question marks
                    w.set_text("?" *w.get_max_length())
                    break
        
    def _on_result_set(self, radio, name):
        
        if radio.get_active():
            if name == "0":
                self.result = "1 - 0"
            elif name == "1":
                self.result = "0 - 1"
            elif name == "2":
                self.result = "1/2 1/2"
            elif name == "3":
                self.result = "*"

    def show_dialog(self):
        """Run the dilaog and return the user's response."""

        # Run the dialog
        response = self.run()

        # Destroy the dialog
        self._destroy()

        # Return the reply
        return response, self.headers

class LicenseDialog(_Dialog):
    """The dialog that show the license."""

    def __init__(self, parent):
        _Dialog.__init__(
            self,
            title="License",
            transient_for=parent,
            modal=True
        )
        self.set_resizable(True)
        self.set_default_size(500, 500)

        # The area to which we can add the text box
        self.area = self.get_content_area()

        # The scrolled window for the text box
        self.scrolledwindow = Gtk.ScrolledWindow()
        self.textview = Gtk.TextView()

        # Open the lisense file
        with open("%sGPL-license.txt" % ROOT_PATH) as f:
            text = f.read()
            f.close()
        
        self.area.pack_start(self.scrolledwindow, True, True, 0)
        self.scrolledwindow.add(self.textview)
        self.textview.do_insert_at_cursor(self.textview, text)
        self.textview.set_editable(False)
        self.textview.show_all()
        self.show_all()

    def show_dialog(self):
        """Show the dialog."""
        response = self.run()
        self.destroy()
        return response

class PromotionDialog(_Dialog):
    """The dialog that shows when a piece is promoted."""

    def __init__(self, parent, color="white"):
        _Dialog.__init__(
            self,
            title="Promotion!",
            transient_for=parent,
            modal=True
        )
        self.set_resizable(False)

        # The color of the piece we are promoting
        self.color = color

        # The area to which we can add the button box
        self.area = self.get_content_area()

        # The variable to return, containing the piece to promote to.
        # Default is queen.
        if self.color == "white":
            self.variable_to_return = "Q"
        else:
            self.variable_to_return = "q"

        # The button box
        self.box = Gtk.HBox()
        self.area.add(self.box)

        # Create the buttons and their images
        self._create_buttons()

        # Show all
        self.show_all()

    def _create_buttons(self):
        """Create the buttons and assign their images."""

        if self.color == "white":
            queen_image = IMAGE_Q
            rook_image = IMAGE_R
            bishop_image = IMAGE_B
            knight_image = IMAGE_N
        else:
            queen_image = IMAGE_q
            rook_image = IMAGE_r
            bishop_image = IMAGE_b
            knight_image = IMAGE_n

        # The queen_button
        self.queen_button = Gtk.Button()
        self.queen_button.connect("clicked", self._on_click, "q")
        self.queen_image = Gtk.Image.new_from_file(queen_image)
        self.queen_button.set_image(self.queen_image)
        self.box.add(self.queen_button)

        # The rook_button
        self.rook_button = Gtk.Button()
        self.rook_button.connect("clicked", self._on_click, "r")
        self.rook_image = Gtk.Image.new_from_file(rook_image)
        self.rook_button.set_image(self.rook_image)
        self.box.add(self.rook_button)

        # The bishop_button
        self.bishop_button = Gtk.Button()
        self.bishop_button.connect("clicked", self._on_click, "b")
        self.bishop_image = Gtk.Image.new_from_file(bishop_image)
        self.bishop_button.set_image(self.bishop_image)
        self.box.add(self.bishop_button)

        # The knight_button
        self.knight_button = Gtk.Button()
        self.knight_button.connect("clicked", self._on_click, "n")
        self.knight_image = Gtk.Image.new_from_file(knight_image)
        self.knight_button.set_image(self.knight_image)
        self.box.add(self.knight_button)

    def _on_click(self, widget, peice):
        """Set the varaible-to-return to the piece that was clicked."""

        # Destroy the dilaog
        self.destroy()

        # Set the variable-to-return
        if self.color == "white":
            self.variable_to_return = peice.upper()
        else:
            self.variable_to_return = peice.lower()

    def show_dialog(self):
        """Run the dilaog and return the user's response."""

        # Run the dialog
        self.run()
        self.destroy()

        # Return the variable
        return self.variable_to_return

class SettingsDialog(_Dialog):
    """The settings dialog."""

    def __init__(self, parent):
        _Dialog.__init__(
            self,
            title="Schach Preferences"
        )
        self.set_default_size(500, 500)

        # The area to which we can add stuff
        self.area = self.get_content_area()

        # Create the window
        self._create_window()

        # Add the buttons
        self._create_buttons()

        self.show_all()

    def _create_buttons(self):
        """Add the buttons to the window."""

        # The buttons
        buttons = (
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL),
            (Gtk.STOCK_OK, Gtk.ResponseType.OK),
        )

        for button in buttons:
            self.add_button(button[0], button[1])

    def _create_window(self):
        """Add all the elements to the window."""

        # The notebook
        self.notebook = Gtk.Notebook()
        self.area.pack_start(self.notebook, True, True, 3)

        # The tabs of the notebook

        # The window tab
        self.window_box = Gtk.VBox()
        self._create_window_box()
        self.notebook.insert_page(self.window_box, Gtk.Label(label="Window"), 0)

    def _create_window_box(self):
        """Add all the elements to the window box."""

        # The status frames checkbutton
        self.status_frames_checkbutton = Gtk.CheckButton(label="Show status frames")
        self.window_box.pack_start(self.status_frames_checkbutton, False, False, 3)

        # The use custom Schach theme button
        self.use_app_theme_checkbutton = Gtk.CheckButton(label="Use custom Schach theme (change requires restart)")
        self.window_box.pack_start(self.use_app_theme_checkbutton, False, False, 3)

        # Set the window to the settings
        self._set_to_settings()

    def _destroy(self, *args):
        """Close the dialog properly."""

        self.destroy()

    def _save_settings(self):
        """Save the settings in the window to the json file."""

        # Get the settings from the window
        self.settings["show_status_frames"] = self.status_frames_checkbutton.get_active()
        self.settings["use_app_theme"] = self.use_app_theme_checkbutton.get_active()

        # Write the file
        json.dump(self.settings, open(f"{ROOT_PATH}json/settings.json", "w"))

    def _set_to_settings(self):
        """Set all the window's settings widgets to the settings from settings.json."""

        # Get the settings from settings.json
        self.settings = json.load(open(f"{ROOT_PATH}/json/settings.json"))

        # Set the widgets
        self.status_frames_checkbutton.set_active(self.settings["show_status_frames"])
        self.use_app_theme_checkbutton.set_active(self.settings["use_app_theme"])

    def show_dialog(self):

        # Run the dialog
        response = self.run()

        # Save the changes if the user hit OK
        if response == Gtk.ResponseType.OK:
            self._save_settings()

        # Destroy the dialog
        self._destroy()

        return response, self.settings

if __name__ == "__main__":
    window = Gtk.Window()
    window.add(Gtk.Label(label="Press a key to see the dialogs."))
    window.show_all()
    def sd(*args):
        print(BoardSetupDialog(window).show_dialog())
        # print(CalendarDialog(window).show_dialog())
        # print(GameSelectorDialog(window).show_dialog())
        # print(HeadersDialog(window, "1/2 - 1/2").show_dialog())
        # print(LicenseDialog(window).show_dialog())
        # print(PromotionDialog(window).show_dialog())
        # print(PromotionDialog(window, "black").show_dialog())
        # print(NewGameDialog(window).show_dialog())
        # print(SettingsDialog(window).show_dialog())

    window.connect("delete-event", Gtk.main_quit)
    window.connect("key-press-event", sd)
    Gtk.main()