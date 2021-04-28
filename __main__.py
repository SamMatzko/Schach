import chessboard
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gio, Gtk

class App(Gtk.Window):
    """The main window for the Scach."""

    def __init__(self):
        
        Gtk.Window.__init__(self, title="Schach")
        self.connect("delete-event", Gtk.main_quit)

        cb = chessboard.ChessBoard()
        self.add(cb)

        self.show_all()

if __name__ == "__main__":
    window = App()
    Gtk.main()