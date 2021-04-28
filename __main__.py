import chessboard
import game
import gi
import time

gi.require_version("Gtk", "3.0")

from gi.repository import Gio, Gtk

class App(Gtk.Window):
    """The main window for the Scach."""

    def __init__(self):
        
        # The window and its settings and events
        Gtk.Window.__init__(self, title="Schach")
        self.connect("delete-event", self.quit)

        # The chessboard widget
        self.chessboard = chessboard.ChessBoard()
        self.add(self.chessboard)

        # The game manager instance
        self.game = game.Game(self.chessboard)

        self.show_all()

    def quit(self, *args):
        """Properly close the application."""

        # Stop the engine
        self.game.engine.quit()

        # Close the window and exit
        Gtk.main_quit()

if __name__ == "__main__":
    window = App()
    Gtk.main()