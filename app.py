import chessboard
import dialogs
import game
import gi
import json
import status_frame
import time

gi.require_version("Gtk", "3.0")

from constants import *
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
            ("File Quit", None, "Quit", "<control>Q", None, self.quit),
            ("Help Menu", None, "Help"),
            ("Help About", None, "About Schach...", None, None, self.show_about)
        ]

        action_group.add_actions(menu_actions, user_data=None)

    def create_header_bar(self):
        """Create the header bar's contents."""

        # The play button
        self.play_button = Gtk.Button.new_from_icon_name("media-playback-start-symbolic", 1)
        self.play_button.set_tooltip_text("Have computer play this turn")
        self.play_button.connect("clicked", self.engine_move)
        self.header_bar.pack_start(self.play_button)

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

    def new_game(self, *args):
        """Create a new game."""

        # Show the dialog
        self.game.new_game()

    def quit(self, *args):
        """Properly close the application."""

        # Stop the engine
        self.game.engine.quit()

        # Close the window and exit
        Gtk.main_quit()

    def show_about(self, *args):
        """Show the about dialog."""

        # Get the info from appinfo.json
        info = json.load(open(f"{ROOT_PATH}json/appinfo.json"))
        info["logo"] = IMAGE_APPLICATION
        dialogs.AbouDialog(self, info).present()