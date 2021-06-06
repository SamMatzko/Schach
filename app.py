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

"""Schach main application."""

import chess
import chess.pgn
import chessboard
import dialogs
import filedialogs
import game
import gi
import io
import json
import os
import pgn
import random
import status_bar
import status_frame
import string
import sys
import time

gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")

from constants import *
from dialogs import messagedialog
from gi.repository import Gdk, Gio, GLib, Gtk, GObject
with open("%sapplication/menu.xml" % ROOT_PATH) as f:
    MENU_XML = f.read()
    f.close()

class App(Gtk.Application):
    """The main application."""

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            application_id="org.schach",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
            **kwargs
        )

        # Whether we have created the actions or not
        self.actions_created = False

        self.add_main_option(
            "open",
            ord("o"),
            GLib.OptionFlags.NONE,
            GLib.OptionArg.FILENAME,
            "File to open",
            None
        )
        self.add_main_option(
            "newWindow",
            ord("n"),
            GLib.OptionFlags.NONE,
            GLib.OptionFlags.NONE,
            "Create a new window",
            None
        )

        # The list of windows
        self.windows = []

        # The name of the currently focused window
        self.window = ""

    def create_actions(self):
        """Create all the actions for the application."""
        self.file_new = Gio.SimpleAction.new("file-new")
        self.file_new_window = Gio.SimpleAction.new("file-new_window")
        self.file_save = Gio.SimpleAction.new("file-save")
        self.file_save_append = Gio.SimpleAction.new("file-save_append")
        self.file_open = Gio.SimpleAction.new("file-open")
        self.file_quit = Gio.SimpleAction.new("file-quit")

        self.edit_undo = Gio.SimpleAction.new("edit-undo")
        self.edit_redo = Gio.SimpleAction.new("edit-redo")
        self.edit_copy_game = Gio.SimpleAction.new("edit-copy_game")
        self.edit_paste_game = Gio.SimpleAction.new("edit-paste_game")
        self.edit_settings = Gio.SimpleAction.new("edit-settings")
        self.edit_copy_game_fen = Gio.SimpleAction.new("edit-copy_game_fen")
        self.edit_paste_game_fen = Gio.SimpleAction.new("edit-paste_game_fen")

        self.view_toggle_status_frames = Gio.SimpleAction.new("view-toggle_status_frames")
        self.view_flip_chessboard = Gio.SimpleAction.new("view-flip_chessboard")

        self.game_engine_move = Gio.SimpleAction.new("game-engine_move")
        self.game_random_move = Gio.SimpleAction.new("game-random_move")
        self.game_type_move = Gio.SimpleAction.new("game-type_move")

        self.help_license = Gio.SimpleAction.new("help-license")
        self.help_about = Gio.SimpleAction.new("help-about")

        self.file_new.connect("activate", self.window_new_game)
        self.file_new_window.connect("activate", self.new_window)
        self.file_save.connect("activate", self.window_save_game)
        self.file_save_append.connect("activate", self.window_save_game_append)
        self.file_open.connect("activate", self.window_load_game)
        self.file_quit.connect("activate", self.window_quit)

        self.edit_undo.connect("activate", self.window_move_undo)
        self.edit_redo.connect("activate", self.window_move_redo)
        self.edit_copy_game.connect("activate", self.window_copy_game)
        self.edit_paste_game.connect("activate", self.window_paste_game)
        self.edit_copy_game_fen.connect("activate", self.window_copy_game_fen)
        self.edit_paste_game_fen.connect("activate", self.window_paste_game_fen)
        self.edit_settings.connect("activate", self.window_show_settings)

        self.view_toggle_status_frames.connect("activate", self.window_toggle_status_frames)
        self.view_flip_chessboard.connect("activate", self.window_flip_chessboard, True)

        self.game_engine_move.connect("activate", self.window_engine_move)
        self.game_random_move.connect("activate", self.window_random_move)
        self.game_type_move.connect("activate", self.window_focus_move_entry)

        self.help_license.connect("activate", self.show_license)
        self.help_about.connect("activate", self.window_show_about)

        self.set_accels_for_action("app.file-new", ["<control>N"])
        self.set_accels_for_action("app.file-new_window", ["<control><shift>N"])
        self.set_accels_for_action("app.file-save", ["<control>S"])
        self.set_accels_for_action("app.file-save_append", ["<control><shift>S"])
        self.set_accels_for_action("app.file-open", ["<control>O"])
        self.set_accels_for_action("app.file-quit", ["<control>Q"])

        self.set_accels_for_action("app.edit-undo", ["<control>Z"])
        self.set_accels_for_action("app.edit-redo", ["<control><shift>Z"])
        self.set_accels_for_action("app.edit-copy_game", ["<control>C"])
        self.set_accels_for_action("app.edit-paste_game", ["<control>V"])
        self.set_accels_for_action("app.edit-copy_game_fen", ["<control><shift>C"])
        self.set_accels_for_action("app.edit-paste_game_fen", ["<control><shift>V"])

        self.set_accels_for_action("app.view-flip_chessboard", ["<control>D"])

        self.set_accels_for_action("app.game-engine_move", ["<control>E"])
        self.set_accels_for_action("app.game-random_move", ["<control>R"])
        self.set_accels_for_action("app.game-type_move", ["<control>M"])

        self.set_accels_for_action("app.edit-undo", ["<control>Z"])

        self.add_action(self.file_new)
        self.add_action(self.file_new_window)
        self.add_action(self.file_save)
        self.add_action(self.file_save_append)
        self.add_action(self.file_open)
        self.add_action(self.file_quit)
        self.add_action(self.edit_undo)
        self.add_action(self.edit_redo)
        self.add_action(self.edit_copy_game)
        self.add_action(self.edit_paste_game)
        self.add_action(self.edit_copy_game_fen)
        self.add_action(self.edit_paste_game_fen)
        self.add_action(self.edit_settings)
        self.add_action(self.view_toggle_status_frames)
        self.add_action(self.view_flip_chessboard)
        self.add_action(self.game_engine_move)
        self.add_action(self.game_random_move)
        self.add_action(self.game_type_move)
        self.add_action(self.help_license)
        self.add_action(self.help_about)

        self.actions_created = True

    def do_activate(self):

        # If the window list is empty, dd a new window to the list of windows
        if len(self.windows) == 0:
            window = Window(application=self, title="Schach", name="%s" % len(self.windows))
            self.windows.append(window)
            self.window = window.name
            window.present()

            # Create the actions
            self.create_actions()

    def do_command_line(self, command_line):

        # Get the command dictionary
        options = command_line.get_options_dict()
        options = options.end().unpack()

        # If there was a file given, get the file path
        try: unicode_file = options["open"]
        except:
            unicode_file = None
        
        # Get if we were told to open a new window
        try: new_window = options["newWindow"]
        except:
            new_window = None

        # The variable containing the file path
        try:
            file = ""     
            for c in unicode_file:
                if chr(c) in string.printable:
                    file = file + chr(c)
            file.strip()
        except TypeError:
            file = "thisisnotafile"

        if os.path.isfile(file):

            if not self.actions_created:
                self.create_actions()

            # Create a new window
            self.new_window()
        
            # Activate the application
            self.activate()

            # Load the file
            self.window_load_game(file=file)

        elif new_window is not None:

            if not self.actions_created:
                self.create_actions()

            # Create a new window
            self.new_window()

            # Activate the application
            self.activate()

        else:

            # Activate the application
            self.activate()
        
        return 0

    def new_window(self, *args):
        """Create a new window."""
        window = Window(self, "Schach", "%s" % len(self.windows))
        self.windows.append(window)
        self.window = window.name
        window.present()
        
    def do_startup(self):
        """Start Schach."""
        Gtk.Application.do_startup(self)

        builder = Gtk.Builder.new_from_string(MENU_XML, -1)
        main_menubar = builder.get_object("app-menubar")
        self.set_menubar(main_menubar)

    def do_window_activated(self, window_name):
        """Set the current window to the window with the name WINDOW_NAME."""

        self.window = window_name

    def do_window_closed(self, window_name):
        """Remove the window with name WINDOW_NAME from the list."""

        # Remove the window
        self.windows.pop(int(window_name))

        # If there are any windows left...
        if len(self.windows) > 0:
            
            # ...reassign all the window names...
            for window in self.windows:
                window.name = str(self.windows.index(window))

        # ...but if not...
        else:
            
            # ...exit the app.
            self.quit()

    def get_current_window_instance(self):
        """Return the current window instance."""
        return self.windows[int(self.window)]

    def show_license(self, *args):
        """Show the dialog displaying GPU license."""
        dialogs.LicenseDialog(self.windows[int(self.window)]).show_dialog()

    def window_new_game(self, *args):
        """Invoke the current window's new game method."""
        self.get_current_window_instance().new_game()

    def window_save_game(self, *args):
        """Invoke the current window's save_game method."""
        self.get_current_window_instance().save_game(append=False)

    def window_save_game_append(self, *args):
        """Invoke the current window's save_game method."""
        self.get_current_window_instance().save_game(append=True)

    def window_load_game(self, *args, file=None):
        """Invoke the current window's load_game method."""
        self.get_current_window_instance().load_game(file)

    def window_quit(self, *args):
        """Invoke the current window's quit method."""
        self.get_current_window_instance().quit()

    def window_move_undo(self, *args):
        """Invoke the current window's move_undo method."""
        self.get_current_window_instance().move_undo()

    def window_move_redo(self, *args):
        """Invoke the current window's move_redo method."""
        self.get_current_window_instance().move_redo()

    def window_copy_game(self, *args):
        """Invoke the current window's copy_game method."""
        self.get_current_window_instance().copy_game()

    def window_paste_game(self, *args):
        """Invoke the current window's paste_game method."""
        self.get_current_window_instance().paste_game()

    def window_copy_game_fen(self, *args):
        """Invoke the current window's copy_fen method."""
        self.get_current_window_instance().copy_fen()

    def window_paste_game_fen(self, *args):
        """Invoke the current window's copy_fen method."""
        self.get_current_window_instance().paste_fen()

    def window_show_settings(self, *args):
        """Invoke the current window's show_settings method."""
        # Show the dialog
        response, settings = dialogs.SettingsDialog(self).show_dialog()

        # Set the settings if the user hit OK
        if response == Gtk.ResponseType.OK:
            
            for window in self.windows:
                # Set the settings to the variable
                window.settings = settings

                # Set the settings to the window
                window.set_settings()
        else:
            pass

    def window_toggle_status_frames(self, *args):
        """Invoke the current window's toggle_status_frames_method."""
        self.get_current_window_instance().toggle_status_frames()

    def window_flip_chessboard(self, parameter, *args):
        """Invoke the current window's flip_chessboard method."""
        self.get_current_window_instance().flip_chessboard(None, None, parameter)

    def window_engine_move(self, *args):
        """Invoke the current window's engine_move method."""
        self.get_current_window_instance().engine_move()

    def window_random_move(self, *args):
        """Invoke the current window's random_move method."""
        self.get_current_window_instance().random_move()

    def window_focus_move_entry(self, *args):
        """Invoke the current window's move_entry method."""
        self.get_current_window_instance().focus_move_entry()

    def window_show_about(self, *args):
        """Invoke the current window's show_about method."""
        self.get_current_window_instance().show_about()

class Window(Gtk.ApplicationWindow):
    """The main window for the Scach."""

    def __init__(self, application, title, name):
        
        # The window and its settings and events
        Gtk.ApplicationWindow.__init__(self, application=application, title=title)
        self.connect("delete-event", self.quit)

        # The application
        self.application = application

        # The window's name
        self.name = name

        # This is so that the application can keep track of the current window
        self.connect("event", self.window_focused)

        # The clipboard
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        # The header bar
        self.header_bar = Gtk.HeaderBar()
        self.header_bar.set_show_close_button(True)
        self.header_bar.props.title = "Schach"
        self.set_titlebar(self.header_bar)

        # Create the header bar
        self.create_header_bar()

        # The main box that everything goes in
        self.main_box = Gtk.VBox()
        self.add(self.main_box)

        # The box to hold all the game-related stuff (i.e., the status labels 
        # and the chessboard)
        self.game_box = Gtk.HBox()
        self.main_box.pack_start(self.game_box, True, False, 10)

        # The chessboard widget
        self.chessboard = chessboard.ChessBoard(parent=self, flipped=True)

        # The status frames
        self.white_status_frame = status_frame.WhiteStatusFrame()
        self.black_status_frame = status_frame.BlackStatusFrame()

        # The status bar
        self.status_bar = status_bar.StatusBar()
        self.main_box.pack_start(self.status_bar, False, True, 0)

        # Add the board, the status frames, and the status bar to the window
        self.game_box.pack_start(self.white_status_frame, True, True, 5)
        self.game_box.pack_start(self.chessboard, True, False, 5)
        self.game_box.pack_start(self.black_status_frame, True, True, 5)

        # The game manager instance
        self.game = game.Game(
            self,
            self.chessboard,
            self.white_status_frame,
            self.black_status_frame,
            self.status_bar
        )
        self.game.update_status()

        # Load the settings
        self.settings = json.load(open(f"{ROOT_PATH}json/settings.json"))
        if self.settings["maximize_on_startup"]:
            self.maximize()
        self.set_settings()

        # Load the theme
        if self.settings["use_app_theme"]:
            self.load_theme()

        self.set_position(Gtk.WindowPosition.CENTER)

        self.show_all()

    def copy_fen(self, *args):
        """Copy the current game to the clipboard as a fen."""

        self.clipboard.set_text(str(self.game.board.board_fen()), -1)

    def copy_game(self, *args):
        """Copy the current game to the clipboard."""

        self.clipboard.set_text(str(chess.pgn.Game.from_board(self.game.board)), -1)

    def create_application_popover(self):
        """Create the application popover and its contents."""

        # The menu model
        builder = Gtk.Builder.new_from_string(MENU_XML, -1)
        popover_menu = builder.get_object("app-popover")

        # The button
        self.app_popover_button = Gtk.MenuButton(menu_model=popover_menu)
        self.app_popover_image = Gtk.Image.new_from_icon_name("open-menu-symbolic", 1)
        self.app_popover_button.set_image(self.app_popover_image)
        self.header_bar.pack_end(self.app_popover_button)

    def create_engine_popover(self):
        """Create the engine popover and its contents."""

        # The scales for the popover
        self.white_computer_scale = Gtk.Scale.new_with_range(
            Gtk.Orientation.HORIZONTAL,
            0.0,
            20.0,
            1.0
        )
        self.white_computer_scale.connect("value-changed", self.on_white_computer_scale)
        self.white_computer_box = Gtk.HBox()
        self.white_computer_frame = Gtk.Frame(label="White computer power")
        self.white_computer_box.pack_start(self.white_computer_frame, True, True, 5)
        self.white_computer_frame.add(self.white_computer_scale)

        self.black_computer_scale = Gtk.Scale.new_with_range(
            Gtk.Orientation.HORIZONTAL,
            0.0,
            20.0,
            1.0
        )
        self.black_computer_scale.connect("value-changed", self.on_black_computer_scale)
        self.black_computer_box = Gtk.HBox()
        self.black_computer_frame = Gtk.Frame(label="Black computer power")
        self.black_computer_box.pack_start(self.black_computer_frame, True, True, 5)
        self.black_computer_frame.add(self.black_computer_scale)

        # A label to make the popover wider
        self.engine_popover_label = Gtk.Label(label=" "*50)

        # The popover
        self.engine_popover = Gtk.Popover()
        self.engine_popover_box = Gtk.VBox()
        self.engine_popover_box.pack_start(self.white_computer_box, False, False, 5)
        self.engine_popover_box.pack_start(self.black_computer_box, False, False, 5)
        self.engine_popover_box.pack_start(self.engine_popover_label, False, False, 0)

        self.engine_popover.add(self.engine_popover_box)
        self.engine_popover_box.show_all()

        # The popover button
        self.engine_popover_button = Gtk.MenuButton(popover=self.engine_popover)
        self.game_settings_box.pack_start(self.engine_popover_button, False, False, 0)

    def create_header_bar(self):
        """Create the header bar's contents."""

        # The game box
        self.game_settings_box = Gtk.HBox()
        Gtk.StyleContext.add_class(self.game_settings_box.get_style_context(), "linked")
        self.header_bar.pack_start(self.game_settings_box)

        # The play button
        self.play_button = Gtk.Button.new_from_icon_name("media-playback-start-symbolic", 1)
        self.play_button.set_tooltip_text("Engine move (Ctrl+E)")
        self.play_button.connect("clicked", self.engine_move)

        # The random move button
        self.random_button = Gtk.Button.new_from_icon_name("mail-send-receive-symbolic", 1)
        self.random_button.set_tooltip_text("Random move (Ctrl+R)")
        self.random_button.connect("clicked", self.random_move)

        # The undo and redo buttons
        self.undo_button = Gtk.Button.new_from_icon_name("media-seek-backward-symbolic", 1)
        self.undo_button.set_tooltip_text("Undo (Ctrl+Z)")
        self.undo_button.connect("clicked", self.move_undo)

        self.redo_button = Gtk.Button.new_from_icon_name("media-seek-forward-symbolic", 1)
        self.redo_button.set_tooltip_text("Redo (Shift+Ctrl+Z)")
        self.redo_button.connect("clicked", self.move_redo)

        # Add the buttons
        self.game_settings_box.pack_start(self.undo_button, False, False, 0)
        self.game_settings_box.pack_start(self.play_button, False, False, 0)
        self.game_settings_box.pack_start(self.random_button, False, False, 0)
        self.game_settings_box.pack_start(self.redo_button, False, False, 0)

        # The move entry box
        self.move_entry_box = Gtk.HBox()
        self.header_bar.pack_start(self.move_entry_box)

        # The move entry
        self.move_entry = Gtk.Entry()
        self.move_entry_box.pack_start(self.move_entry, True, True, 3)
        self.move_entry.set_max_length(5)
        self.move_entry.set_placeholder_text("Type a move...")
        self.move_entry.set_tooltip_text("Type a move (Ctrl+M)")
        self.move_entry.connect("activate", self.on_move_entry_activate)

        self.move_entry.show_all()
        self.move_entry_box.show_all()

        # Create the engine popover
        self.create_engine_popover()

        # Create the application popover
        self.create_application_popover()

    def engine_move(self, *args):
        """Have the computer play for the current turn."""
        self.game.engine_move()

    def exit(self):
        """Exit the app immediately."""

        # Stop the engine
        self.game.engine.quit()

        # Close the window and give the application the name of the closed window
        self.application.do_window_closed(self.name)
        self.destroy()

    def flip_chessboard(self, one, two, menu_trigger):
        """Flip the chessboard."""

        # Set the chessboard flipped or not
        self.game_box.remove(self.chessboard)
        for square in self.chessboard._get_squares():
            del square
        del self.chessboard
        self.chessboard = chessboard.ChessBoard(self, flipped=True)

        # Remove and replace the frames and chessboard
        self.game_box.remove(self.white_status_frame)
        self.game_box.remove(self.black_status_frame)
        
        self.game_box.pack_start(self.white_status_frame, True, True, 5)
        self.game_box.pack_start(self.chessboard, True, False, 10)
        self.game_box.pack_start(self.black_status_frame, True, True, 5)

        # Set up the board and bind the squares
        self.chessboard.from_string(str(self.game.board))
        self.chessboard.bind_squares(self.game._assert_move)
        self.game.chessboard = self.chessboard

        self.chessboard.show_all()
        while Gtk.events_pending():
            Gtk.main_iteration()

    def focus_move_entry(self, *args):
        """Set the focus to the move entry."""
        self.move_entry.grab_focus()

    def load_game(self, file=None, *args):
        """Load a game from a pgn file."""
        
        # Get the file to load the game from

        if file is not None:
            file = file
        else:
            file = filedialogs.Open(parent=self, title="Load a Game").show()
        if file is not None:

            # Get the contents of the file
            with open(file) as f:
                games = f.read()
                f.close()
            
            # Show the game selection dialog
            response, game = dialogs.GameSelectorDialog(self, games).show_dialog()
            
            # Load the selected game if the user clicked OK
            if response == Gtk.ResponseType.OK:
                
                self.game.new_game(game.mainline_moves())

    def load_theme(self):
        """Load the theme."""

        provider = Gtk.CssProvider.new()
        display = Gdk.Display.get_default()
        screen = display.get_default_screen()
        Gtk.StyleContext.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        provider.load_from_path(ROOT_PATH + "application/schach.css")

    def move_redo(self, *args):
        """Redo the last undone move."""
        self.game.move_redo()

    def move_undo(self, *args):
        """Undo the last move on the stack."""
        self.game.move_undo()

    def new_game(self, *args):
        """Create a new game."""

        # Ask the user if they want to save the current game before exiting
        response = dialogs.messagedialog.ask_yes_no_cancel(
            self,
            "Save game?",
            "Save the current game before creating a new one?"
        )
        if response == Gtk.ResponseType.OK:
            self.save_game(append=True)
            self.game.new_game()
        elif response == Gtk.ResponseType.NO:
            self.game.new_game()
        else:
            pass

    def on_black_computer_scale(self, scale):
        """Set the black computer's playing power to the scale's value."""
        self.game.set_limit(black_limit=scale.get_value())

    def on_move_entry_activate(self, entry):
        """Move the move in the entry, if it is valid."""

        uci = entry.get_text()
        move_failed = False

        try: move = chess.Move.from_uci(uci)
        except:
            move_failed = True

        if not move_failed and move in self.game.board.legal_moves:
            self.game._push_move(move)
            self.game.update_status()
            self.chessboard.from_string(str(self.game.board))
            entry.get_buffer().delete_text(0, 5)
        else:
            dialogs.messagedialog.show_info(
                self,
                "Invalid Move",
                "The given move was invalid. Please try a different one."
            )
            entry.get_buffer().delete_text(0, 5)

    def on_white_computer_scale(self, scale):
        """Set the white computer's playing power to the scale's value."""
        self.game.set_limit(white_limit=scale.get_value())

    def paste_fen(self, *args):
        """Paste a game from a copied fen string."""

        # Get the game stuff
        fen = self.clipboard.wait_for_text()

        # Make sure that the user wants to quit the current game
        response = dialogs.messagedialog.ask_yes_no_cancel(
            self,
            "Save game?",
            "Save the current game before pasting a new one?"
        )
        if response == Gtk.ResponseType.NO:
            self.game.new_game_from_fen(fen)
        elif response == Gtk.ResponseType.YES:
            self.save_game(append=True)
            self.game.new_game_from_fen(fen)
        else:
            pass

    def paste_game(self, *args):
        """Paste a game that was copied to the clipboard."""
        
        # Get the game stuff
        game = self.clipboard.wait_for_text()
        game_instance = chess.pgn.read_game(io.StringIO(game))

        # Make sure that the user wants to quit the current game
        response = dialogs.messagedialog.ask_yes_no_cancel(
            self,
            "Save game?",
            "Save the current game before pasting a new one?"
        )
        if response == Gtk.ResponseType.NO:
            self.game.new_game(game_instance.mainline_moves())
        elif response == Gtk.ResponseType.YES:
            self.save_game(append=True)
            self.game.new_game(game_instance.mainline_moves())
        else:
            pass

    def quit(self, *args):
        """Properly close the application."""

        # Ask the user if they want to save the game
        response = messagedialog.ask_yes_no_cancel(
            self,
            "Save game?",
            "Save the current game before exiting?"
        )

        if response == Gtk.ResponseType.NO:
            self.exit()
        elif response == Gtk.ResponseType.YES:
            if self.save_game(append=True):
                return True
            else:
                self.exit()
        else:
            return True # This keeps the window from closing anyway

    def random_move(self, *args):
        """Make a random move."""
        
        if not self.game.board.is_game_over():
            legal_moves = []
            for move in self.game.board.legal_moves:
                legal_moves.append(move.uci())
            random_move = random.choice(legal_moves)
            self.game._push_move(chess.Move.from_uci(random_move))
            self.chessboard.from_string(str(self.game.board))
            self.game.update_status()

    def save_game(self, action=None, something_else=None, append=None):
        """Prompt the user for a file to save the game to and the headers for the game."""

        # If the game has ended, set the override the result in the headers
        if self.game.board.is_game_over():
            status = self.game.get_game_status()
            if status["is_checkmate"]:
                if status["turn"]:
                    override_result = "0 - 1"
                else:
                    override_result = "1 - 0"
            else:
                override_result = "1/2 - 1/2"
        else:
            override_result = None

        # Set the title for the dialog
        if append:
            title = "Save: Add Game"
        else:
            title = "Save: Replace Game"

        # Get the headers
        response, headers = dialogs.HeadersDialog(
            self,
            title=title,
            override_result=override_result
        ).show_dialog()

        if response == Gtk.ResponseType.OK:

            # Get the file
            file = filedialogs.SaveAs(parent=self, initialdir=os.environ["HOME"]).show()
            if file is not None:

                # Save the file
                if append:
                    pgn.save_game_append(self.game.board, file, headers)
                else:
                    pgn.save_game(self.game.board, file, headers)
            else:
                return True
        else:
            return True

    def set_settings(self):
        """Set the window to the current settings in self.settings."""

        if self.settings["show_status_frames"]:
            self.white_status_frame.set_no_show_all(False)
            self.white_status_frame.show_all()
            self.black_status_frame.set_no_show_all(False)
            self.black_status_frame.show_all()
        else:
            self.white_status_frame.hide()
            self.white_status_frame.set_no_show_all(True)
            self.black_status_frame.hide()
            self.black_status_frame.set_no_show_all(True)

        # Write the file
        json.dump(self.settings, open(f"{ROOT_PATH}json/settings.json", "w"))

    def show_about(self, *args):
        """Show the about dialog."""

        # Get the info from appinfo.json
        info = json.load(open(APP_INFO))
        info["logo"] = IMAGE_APPLICATION
        dialogs.AboutDialog(self, info).present()

    def toggle_status_frames(self, *args):
        
        self.settings["show_status_frames"] = not self.settings["show_status_frames"]
        self.set_settings()

    def window_focused(self, widget, event):
        if self.has_toplevel_focus():
            self.application.do_window_activated(self.name)