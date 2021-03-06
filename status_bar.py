# Schach is a basic chess application that uses the Stockfish chess engine.
# Copyright (C) 2021  Samuel Matzko

# This file is part of Schach.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
# or see <http://www.gnu.org/licenses/>

"""The status bar to go at the bottom of the window."""

import gi
import json

gi.require_version("Gtk", "3.0")

from constants import *
from gi.repository import Gtk

class StatusBar(Gtk.Frame):
    """The status bar."""

    def __init__(self, *args, **kwargs):
        Gtk.Frame.__init__(self, *args, **kwargs)

        # Load the application info
        with open(APP_INFO) as f:
            self.app_info = json.load(f)
            f.close()

        # Our hbox
        self.box = Gtk.HBox()
        self.add(self.box)

        # The turn label
        self.turn_label = Gtk.Label(label="White")
        self.box.pack_start(self.turn_label, False, False, 3)

        # The status label
        self.status_label = Gtk.Label()
        self.box.pack_start(self.status_label, False, False, 20)

        # The Schach version label
        self.version_label = Gtk.Label(label=self.app_info["version"])
        self.box.pack_end(self.version_label, False, False, 3)

        # The fen label
        self.fen_label = Gtk.Label()
        self.box.pack_end(self.fen_label, False, False, 20)
        self.fen_label.set_selectable(True)

        self.box.show_all()
        self.show_all()

    def set_status(self, fen=None, turn=None, check=False, game_over="", thinking=False):
        """Set the status bar to the given game status."""
        if fen is not None:
            self.fen_label.set_label(fen)
        if turn is not None:
            if turn:
                self.turn_label.set_label("White")
            else:
                self.turn_label.set_label("Black")
        if thinking:
            self.turn_label.set_label("%s..." % self.turn_label.get_text())
        if check:
            self.status_label.set_label("Check")
        else:
            self.status_label.set_label("")
        if game_over != "":
            self.status_label.set_label(game_over)
        self.turn_label.show_all()
        self.status_label.show_all()