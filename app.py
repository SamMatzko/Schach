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
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA."""

import chessboard
import dialogs
import filedialogs
import game
import gi
import json
import os
import pgn
import status_frame
import sys
import time

gi.require_version("Gtk", "3.0")

from constants import *
from dialogs import messagedialog
from gi.repository import Gio, GLib, Gtk, GObject
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
        self.file_quit = Gio.SimpleAction.new("file-quit")

        self.edit_undo = Gio.SimpleAction.new("edit-undo")
        self.edit_redo = Gio.SimpleAction.new("edit-redo")
        self.edit_settings = Gio.SimpleAction.new("edit-settings")

        self.game_engine_move = Gio.SimpleAction.new("game-engine_move")

        self.help_about = Gio.SimpleAction.new("help-about")

        self.file_new.connect("activate", self.window.new_game)
        self.file_save.connect("activate", self.window.save_game)
        self.file_quit.connect("activate", self.window.quit)

        self.edit_undo.connect("activate", self.window.move_undo)
        self.edit_redo.connect("activate", self.window.move_redo)
        self.edit_settings.connect("activate", self.window.show_settings)

        self.game_engine_move.connect("activate", self.window.engine_move)

        self.help_about.connect("activate", self.window.show_about)

        self.set_accels_for_action("app.file-new", ["<control>N"])
        self.set_accels_for_action("app.file-save", ["<control>S"])
        self.set_accels_for_action("app.file-quit", ["<control>Q"])

        self.set_accels_for_action("app.edit-undo", ["<control>Z"])
        self.set_accels_for_action("app.edit-redo", ["<control><shift>Z"])

        self.set_accels_for_action("app.game-engine_move", ["<control>E"])

        self.set_accels_for_action("app.edit-undo", ["<control>Z"])

        self.add_action(self.file_new)
        self.add_action(self.file_save)
        self.add_action(self.file_quit)
        self.add_action(self.edit_undo)
        self.add_action(self.edit_redo)
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
        self.game_settings_box.pack_start(self.play_button, False, False, 0)

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
        self.popover_label = Gtk.Label(label=" "*50)

        # The popover
        self.popover = Gtk.Popover()
        self.popover_box = Gtk.VBox()
        self.popover_box.pack_start(self.white_computer_box, False, False, 5)
        self.popover_box.pack_start(self.black_computer_box, False, False, 5)
        self.popover_box.pack_start(self.popover_label, False, False, 0)

        self.popover.add(self.popover_box)
        self.popover_box.show_all()

        # The popover button
        self.popover_button = Gtk.MenuButton(popover=self.popover)
        self.game_settings_box.pack_start(self.popover_button, False, False, 0)

    def engine_move(self, *args):
        """Have the computer play for the current turn."""
        self.game._engine_move()

    def exit(self):
        """Exit the app immediately."""

        # Stop the engine
        self.game.engine.quit()

        # Close the window and exit
        self.application.quit()

    def move_redo(self, *args):
        """Redo the last undone move."""
        self.game.move_redo()

    def move_undo(self, *args):
        """Undo the last move on the stack."""
        self.game.move_undo()

    def new_game(self, *args):
        """Create a new game."""

        self.game.new_game()

    def on_black_computer_scale(self, scale):
        """Set the black computer's playing power to the scale's value."""
        self.game.set_limit(black_limit=scale.get_value())

    def on_white_computer_scale(self, scale):
        """Set the white computer's playing power to the scale's value."""
        self.game.set_limit(white_limit=scale.get_value())

    def quit(self, *args):
        """Properly close the application."""

        # Ask the user if they want to save the game
        response = messagedialog.ask_yes_no_cancel(
            self,
            "Game not saved",
            "The game has not been saved. Save game?"
        )

        if response == Gtk.ResponseType.NO:
            self.exit()
        elif response == Gtk.ResponseType.YES:
            if self.save_game():
                return True
            else:
                self.exit()
        else:
            return True # This keeps the window from closing anyway

    def save_game(self, *args):
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

        # Get the headers
        response, headers = dialogs.HeadersDialog(self, override_result).show_dialog()
        if response == Gtk.ResponseType.OK:

            # Get the file
            file = filedialogs.SaveAs(parent=self, initialdir=os.environ["HOME"]).show()
            if file is not None:

                # Save the file
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