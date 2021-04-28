import chessboard
import game
import gi
import time

gi.require_version("Gtk", "3.0")

from constants import *
from gi.repository import Gio, Gtk

class App(Gtk.Window):
    """The main window for the Scach."""

    def __init__(self):
        
        # The window and its settings and events
        Gtk.Window.__init__(self, title="Schach")
        self.connect("delete-event", self.quit)

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

        # The chessboard widget
        self.chessboard = chessboard.ChessBoard(parent=self)
        self.main_box.pack_start(self.chessboard, False, False, 10)

        # The game manager instance
        self.game = game.Game(self.chessboard)

        self.show_all()

    def add_file_menu_actions(self, action_group):
        action_filemenu = Gtk.Action(name="FileMenu", label="File")
        action_group.add_action(action_filemenu)

        menu_actions = [
            ("File Menu", None, "File"),
            ("File New", None, "New game...", "<control>N", None, self.new_game),
            ("File Quit", None, "Quit", "<control>Q", None, self.quit)
        ]

        action_group.add_actions(menu_actions, user_data=None)

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

    def new_game(self, *args):
        """Create a new game."""
        self.game.new_game()

    def quit(self, *args):
        """Properly close the application."""

        # Stop the engine
        self.game.engine.quit()

        # Close the window and exit
        Gtk.main_quit()