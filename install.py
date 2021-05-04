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

"""Install Schach."""

import os
import sys

# Install only if we are on a linux-based system
if "linux" in sys.platform.lower():

    # Our location 
    CURRENT_DIR = os.path.dirname(__file__) + "/"

    # The install directory
    INSTALL_IN = os.environ["HOME"] + "/.local/share/"

    # The directory for the desktop file
    DESKTOP_DIR = os.environ["HOME"] + "/.local/share/applications/"

    # The contents of the desktop file
    f"""[Desktop Entry]
Name=Schach
Comment=A chess-playing app that uses the stockfish engine
GenericName=Schach chess app
Exec=python3 {INSTALL_IN}Schach/ %F
Icon={INSTALL_IN}Schach/icons/application/appicon.png
Type=Application
Terminal=True
StartupNotify=True
Keywords=chess;master;"""
    print("This does not install Schach yet.")


else:
    print("FATAL ERROR: This program can only install in Linux systems. Install aborted.")