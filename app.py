import chessboard
import dialogs
import filedialogs
import game
import gi
import json
import os
import pgn
import status_frame
import time

gi.require_version("Gtk", "3.0")

from constants import *
from dialogs import messagedialog
from gi.repository import Gio, Gtk

class App(Gtk.Window):
    """The main window for the Scach."""

    def __init__(self):
        
        # The window and its settings and events
        Gtk.Window.__init__(self)
        self.connect("delete-event", self.quit)

        # The header bar
        self.header_bar = Gtk.HeaderBar()
        self.header_bar.set_show_close_button(True)
        self.header_bar.props.title = "Schach"
        self.set_titlebar(self.header_bar)
        self.maximize()

        # Create the header bar
        self.create_header_bar()

        # The main box that everything goes in
        self.main_box = Gtk.VBox()
        self.add(self.main_box)

        # Set up the ui stuff
        action_group = Gtk.ActionGroup(name="my_actions")
        self.add_file_menu_actions(action_group)

        # The ui manager
        self.uimanager = self.create_ui_manager()
        self.uimanager.insert_action_group(action_group)

        # The menubar
        self.menubar = self.uimanager.get_widget("/MenuBar")

        # The box for the menubar
        self.menu_box = Gtk.VBox()
        self.menu_box.pack_start(self.menubar, False, False, 0)
        self.menu_box.show_all()
        self.main_box.pack_start(self.menu_box, False, False, 0)

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

        self.show_all()

    def add_file_menu_actions(self, action_group):
        action_filemenu = Gtk.Action(name="FileMenu", label="File")
        action_group.add_action(action_filemenu)

        menu_actions = [
            ("File Menu", None, "File"),
            ("File New", None, "New game...", "<control>N", None, self.new_game),
            ("File Save", None, "Save game...", "<control>S", None, self.save_game),
            ("File Quit", None, "Quit", "<control>Q", None, self.quit),
            ("Help Menu", None, "Help"),
            ("Help About", None, "About Schach...", None, None, self.show_about)
        ]

        action_group.add_actions(menu_actions, user_data=None)

    def create_header_bar(self):
        """Create the header bar's contents."""

        # The game box
        self.game_settings_box = Gtk.HBox()
        Gtk.StyleContext.add_class(self.game_settings_box.get_style_context(), "linked")
        self.header_bar.pack_start(self.game_settings_box)

        # The play button
        self.play_button = Gtk.Button.new_from_icon_name("media-playback-start-symbolic", 1)
        self.play_button.set_tooltip_text("Have computer play this turn")
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

    def create_ui_manager(self):
        self.uimanager = Gtk.UIManager()

        # Open ui/menu.xml and load the menu from it
        with open(MENU_XML) as f:
            menu_xml = f.read()
            f.close()
        self.uimanager.add_ui_from_string(menu_xml)

        # Add the accelerator group to the toplevel window
        accelgroup = self.uimanager.get_accel_group()
        self.add_accel_group(accelgroup)
        return self.uimanager

    def engine_move(self, *args):
        """Have the computer play for the current turn."""
        self.game._engine_move()

    def exit(self):
        """Exit the app immediately."""

        # Stop the engine
        self.game.engine.quit()

        # Close the window and exit
        Gtk.main_quit()

    def new_game(self, *args):
        """Create a new game."""

        # Show the dialog
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
        response = messagedialog.ask_yes_no(
            self,
            "Game not saved",
            "The game has not been saved. Save game?"
        )

        if response == Gtk.ResponseType.NO:
            self.exit()
        else:
            self.save_game()
            self.exit()

    def save_game(self, *args):
        """Prompt the user for a file to save the game to."""

        # Get the file
        file = filedialogs.SaveAs(parent=self, initialdir=os.environ["HOME"]).show()
        
        # Save the file
        pgn.save_game(self.game.board, file)

    def show_about(self, *args):
        """Show the about dialog."""

        # Get the info from appinfo.json
        info = json.load(open(f"{ROOT_PATH}json/appinfo.json"))
        info["logo"] = IMAGE_APPLICATION
        dialogs.AbouDialog(self, info).present()