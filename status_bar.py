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

import gi
import json

gi.require_version("Gtk", "3.0")

from constants import *
from gi.repository import Gtk

class StatusBar(Gtk.VBox):
    """The bar to show status on the chess game."""
    
    def __init__(self, *args, **kwargs):
        Gtk.VBox.__init__(self, *args, **kwargs)

        # The application info for the version label
        with open(f"{ROOT_PATH}json/appinfo.json") as f:
            self.info = json.load(f)
            if not f.closed:
                f.close()

        # The separator
        self.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, True, 0)

        # The box to hold everything else
        self.hbox = Gtk.HBox()
        self.add(self.hbox)

        # The version label
        self.version_label = Gtk.Label(label=self.info["version"])
        self.hbox.pack_end(self.version_label, False, False, 3)

        self.show_all()