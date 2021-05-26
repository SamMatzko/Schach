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

        # The Schach version label
        self.version_label = Gtk.Label(label=self.app_info["version"])

        self.hbox.show_all()