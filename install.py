#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

"""Install Schach."""

import json
import os
import sys

# Install only if we are on a linux-based system
if "linux" in sys.platform.lower():

    # Check if we are installing or uninstalling
    try: uninstall = sys.argv[1]
    except:
        uninstall = False
    if not uninstall:

        # The directories
        APPLICATION = os.path.dirname(__file__)
        APPLICATION_DIR = APPLICATION + "/"
        CURRENT_DIR = os.path.dirname(APPLICATION_DIR)

        # Load our version info
        with open(APPLICATION_DIR + "json/appinfo.json") as f:
            current_appinfo = json.load(f)
            f.close()
        current_version = current_appinfo["version"]
        current_update = current_appinfo["nano_revision"]
        print("Starting install of Schach %s..." % current_version)

        # Create the desktop file from the template
        print("Creating desktop...", end="")
        with open(APPLICATION_DIR + "desktop.template") as f:
            template = f.read()
            f.close()
        template = template.replace("<ICON_PATH>", APPLICATION_DIR + "icons/application/appicon.png")
        template = template.replace("<APP_PATH>", APPLICATION)
        with open(APPLICATION_DIR + "schach-chess.desktop", "w") as f:
            f.write(template)
            f.close()
        print("Done")
        
        # Install the desktop
        print("Installing desktop...", end="")
        os.system("xdg-desktop-menu install %s" % APPLICATION_DIR + "schach-chess.desktop")
        os.system("xdg-desktop-icon install %s" % APPLICATION_DIR + "schach-chess.desktop")
        os.system("xdg-mime default schach-chess.desktop application/vnd.chess-pgn")
        print("Done")

    else:

        # The directories
        APPLICATION = os.path.dirname(__file__)
        APPLICATION_DIR = APPLICATION + "/"
        CURRENT_DIR = os.path.dirname(APPLICATION_DIR)

        # Load our version info
        with open(APPLICATION_DIR + "json/appinfo.json") as f:
            current_appinfo = json.load(f)
            f.close()
        current_version = current_appinfo["version"]
        current_update = current_appinfo["nano_revision"]
        print("Starting uninstall of Schach %s..." % current_version)
        
        # Uninstall the desktop
        print("Uninstalling desktop...", end="")
        os.system("xdg-desktop-menu uninstall %s" % APPLICATION_DIR + "schach-chess.desktop")
        os.system("xdg-desktop-icon uninstall %s" % APPLICATION_DIR + "schach-chess.desktop")
        print("Done")

else:
    print("FATAL ERROR: Your system is not a Linux. This install cannot run.")