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
import chessboard
import dialogs
import filedialogs
import game
import gi
import io
import json
import os
import pgn
import status_frame
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
            **kwargs
        )

        self.window = None

    def _create_actions(self):
        """Create all the actions for the application."""
        self.file_new = Gio.SimpleAction.new("file-new")
        self.file_save = Gio.SimpleAction.new("file-save")
        self.file_save_append = Gio.SimpleAction.new("file-save-append")
        self.file_open = Gio.SimpleAction.new("file-open")
        self.file_quit = Gio.SimpleAction.new("file-quit")

        self.edit_undo = Gio.SimpleAction.new("edit-undo")
        self.edit_redo = Gio.SimpleAction.new("edit-redo")
        self.edit_copy_game = Gio.SimpleAction.new("edit-copy_game")
        self.edit_paste_game = Gio.SimpleAction.new("edit-paste_game")
        self.edit_settings = Gio.SimpleAction.new("edit-settings")

        self.game_engine_move = Gio.SimpleAction.new("game-engine_move")

        self.help_about = Gio.SimpleAction.new("help-about")

        self.file_new.connect("activate", self.window.new_game)
        self.file_save.connect("activate", self.window.save_game, False)
        self.file_save_append.connect("activate", self.window.save_game, True)
        self.file_open.connect("activate", self.window.load_game)
        self.file_quit.connect("activate", self.window.quit)

        self.edit_undo.connect("activate", self.window.move_undo)
        self.edit_redo.connect("activate", self.window.move_redo)
        self.edit_copy_game.connect("activate", self.window.copy_game)
        self.edit_paste_game.connect("activate", self.window.paste_game)
        self.edit_settings.connect("activate", self.window.show_settings)

        self.game_engine_move.connect("activate", self.window.engine_move)

        self.help_about.connect("activate", self.window.show_about)

        self.set_accels_for_action("app.file-new", ["<control>N"])
        self.set_accels_for_action("app.file-save", ["<control>S"])
        self.set_accels_for_action("app.file-save-append", ["<control><shift>S"])
        self.set_accels_for_action("app.file-open", ["<control>O"])
        self.set_accels_for_action("app.file-quit", ["<control>Q"])

        self.set_accels_for_action("app.edit-undo", ["<control>Z"])
        self.set_accels_for_action("app.edit-redo", ["<control><shift>Z"])
        self.set_accels_for_action("app.edit-copy_game", ["<control>C"])
        self.set_accels_for_action("app.edit-paste_game", ["<control>V"])

        self.set_accels_for_action("app.game-engine_move", ["<control>E"])

        self.set_accels_for_action("app.edit-undo", ["<control>Z"])

        self.add_action(self.file_new)
        self.add_action(self.file_save)
        self.add_action(self.file_save_append)
        self.add_action(self.file_open)
        self.add_action(self.file_quit)
        self.add_action(self.edit_undo)
        self.add_action(self.edit_redo)
        self.add_action(self.edit_copy_game)
        self.add_action(self.edit_paste_game)
        self.add_action(self.edit_settings)
        self.add_action(self.game_engine_move)
        self.add_action(self.help_about)

    def do_startup(self):
        """Start Schach."""
        Gtk.Application.do_startup(self)

        builder = Gtk.Builder.new_from_string(MENU_XML, -1)
        main_menu = builder.get_object("app-menu")
        self.set_menubar(main_menu)

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = Window(application=self, title="Schach")

            self.window.present()

        # Create the actions
        self._create_actions()

class Window(Gtk.ApplicationWindow):
    """The main window for the Scach."""

    def __init__(self, application, title):
        
        # The window and its settings and events
        Gtk.ApplicationWindow.__init__(self, application=application, title=title)
        self.connect("delete-event", self.quit)

        # The application
        self.application = application

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
        self.chessboard = chessboard.ChessBoard(parent=self)

        # The status frames
        self.white_status_frame = status_frame.WhiteStatusFrame()
        self.black_status_frame = status_frame.BlackStatusFrame()

        # Add the board and the status frames to the window
        self.game_box.pack_start(self.white_status_frame, True, True, 5)
        self.game_box.pack_start(self.chessboard, True, False, 10)
        self.game_box.pack_start(self.black_status_frame, True, True, 5)

        # The game manager instance
        self.game = game.Game(
            self,
            self.chessboard,
            self.white_status_frame,
            self.black_status_frame
        )
        self.game._update_status()

        # Load the settings
        self.settings = json.load(open(f"{ROOT_PATH}json/settings.json"))
        if self.settings["maximize_on_startup"]:
            self.maximize()
        self.set_settings()

        self.show_all()

    def copy_game(self, *args):
        """Copy the current game to the clipboard."""

        self.clipboard.set_text(str(chess.pgn.Game.from_board(self.game.board)), -1)

    def create_application_popover(self):
        """Create the application popover and its contents."""

        # The popover
        self.app_popover = Gtk.Popover()
        self.app_popover_base_box = Gtk.VBox()
        self.app_popover_hbox = Gtk.HBox()
        self.app_popover_vbox = Gtk.VBox()
        self.app_popover_base_box.pack_start(self.app_popover_hbox, True, True, 3)
        self.app_popover_hbox.pack_start(self.app_popover_vbox, True, True, 3)
        self.app_popover.add(self.app_popover_base_box)

        # The View expander
        self.app_popover_view_expander = Gtk.Expander(label="View")
        self.app_popover_vbox.add(self.app_popover_view_expander)

        # The view expander's elements
        self.create_view_expander()

        # The Preferences button
        self.app_popover_settings_button = Gtk.ModelButton(label=("Preferences".ljust(50, " ")))
        self.app_popover_settings_button.connect("clicked", self.show_settings)
        self.app_popover_vbox.add(self.app_popover_settings_button)

        self.app_popover_vbox.add(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL))

        # The about button
        self.app_popover_about_button = Gtk.ModelButton(label=("About Schach".ljust(50, " ")))
        self.app_popover_about_button.connect("clicked", self.show_about)
        self.app_popover_vbox.add(self.app_popover_about_button)

        self.app_popover_base_box.show_all()
        self.app_popover_hbox.show_all()
        self.app_popover_vbox.show_all()

        # The button
        self.app_popover_button = Gtk.MenuButton(popover=self.app_popover)
        self.app_popover_image = Gtk.Image.new_from_icon_name("open-menu-symbolic", 1)
        self.app_popover_button.set_image(self.app_popover_image)
        self.header_bar.pack_end(self.app_popover_button)

    def create_engine_popover(self):
        """Create the engine popover and its contents."""

        # Add the buttons
        self.game_settings_box.pack_start(self.undo_button, False, False, 0)
        self.game_settings_box.pack_start(self.play_button, False, False, 0)
        self.game_settings_box.pack_start(self.redo_button, False, False, 0)

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

        # The undo and redo buttons
        self.undo_button = Gtk.Button.new_from_icon_name("media-seek-backward-symbolic", 1)
        self.undo_button.set_tooltip_text("Undo (Ctrl+Z)")
        self.undo_button.connect("clicked", self.move_undo)

        self.redo_button = Gtk.Button.new_from_icon_name("media-seek-forward-symbolic", 1)
        self.redo_button.set_tooltip_text("Redo (Shift+Ctrl+Z)")
        self.redo_button.connect("clicked", self.move_redo)

        # Create the engine popover
        self.create_engine_popover()

        # Create the application popover
        self.create_application_popover()

    def create_view_expander(self):
        """Create and add all the items of the View expander."""

        # The show status frames checkbutton
        self.view_show_status_frames_checkbutton = Gtk.CheckButton(label="Show status frames")
        self.view_show_status_frames_checkbutton.connect("toggled", self.set_settings_from_popover)
        self.app_popover_view_expander.add(self.view_show_status_frames_checkbutton)

    def engine_move(self, *args):
        """Have the computer play for the current turn."""
        self.game._engine_move()

    def exit(self):
        """Exit the app immediately."""

        # Stop the engine
        self.game.engine.quit()

        # Close the window and exit
        self.application.quit()

    def load_game(self, *args):
        """Load a game from a pgn file."""
        
        # Get the file to load the game from
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
            "Game not saved.",
            "The current game has not been saved. Save before creating a new one?"
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

    def on_white_computer_scale(self, scale):
        """Set the white computer's playing power to the scale's value."""
        self.game.set_limit(white_limit=scale.get_value())

    def paste_game(self, *args):
        """Paste a game that was copied to the clipboard."""
        
        # Get the game stuff
        game = self.clipboard.wait_for_text()
        game_instance = chess.pgn.read_game(io.StringIO(game))

        # Make sure that the user wants to quit the current game
        response = dialogs.messagedialog.ask_yes_no_cancel(
            self,
            "Game not saved.",
            "The current game has not been saved. Save before pasting a new one?"
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
            "Game may not be saved",
            "Do you want to save the game before exiting?"
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

        self.view_show_status_frames_checkbutton.set_active(self.settings["show_status_frames"])

        # Write the file
        json.dump(self.settings, open(f"{ROOT_PATH}json/settings.json", "w"))

    def set_settings_from_popover(self, *args):
        """Set the settings based on the checkbuttons in the app_popover."""

        self.settings["show_status_frames"] = self.view_show_status_frames_checkbutton.get_active()
        self.set_settings()

    def show_about(self, *args):
        """Show the about dialog."""

        # Get the info from appinfo.json
        info = json.load(open(f"{ROOT_PATH}json/appinfo.json"))
        info["logo"] = IMAGE_APPLICATION
        dialogs.AboutDialog(self, info).present()

    def show_settings(self, *args):
        """Show the settings dialog."""
        
        # Show the dialog
        response, settings = dialogs.SettingsDialog(self).show_dialog()

        # Set the settings if the user hit OK
        if response == Gtk.ResponseType.OK:

            # Set the settings to the variable
            self.settings = settings

            # Set the settings to the window
            self.set_settings()
        else:
            pass