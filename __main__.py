import chessboard
import gi
import time

gi.require_version("Gtk", "3.0")
from gi.repository import Gio, Gtk

class App(Gtk.Window):
    """The main window for the Scach."""

    def __init__(self):
        
        Gtk.Window.__init__(self, title="Schach")
        self.connect("delete-event", Gtk.main_quit)
        self.connect("key-press-event", self.update)

        self.cb = chessboard.ChessBoard()
        self.add(self.cb)
        self.cb.bind_squares(self.method)

        self.show_all()

    def method(self, *args):
        print(args)

    def update(self, *args):
        self.cb.from_string(". . b . . . . r p . . . p . p p . p . . q . . . Q . p n . . k P . . b P n p . . . P . . . . . p P . P r B P . P R N . . K B N R")

if __name__ == "__main__":
    window = App()
    Gtk.main()