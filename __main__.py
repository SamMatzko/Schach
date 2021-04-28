import app
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

if __name__ == "__main__":
    window = app.App()
    Gtk.main()