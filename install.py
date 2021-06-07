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

    # The directories
    APPLICATION = os.path.dirname(__file__)
    APPLICATION_DIR = APPLICATION + "/"
    CURRENT_DIR = os.path.dirname(APPLICATION_DIR)
    INSTALL_IN = os.environ["HOME"] + "/.local/share/"

    # Load our version info
    with open(APPLICATION_DIR + "json/appinfo.json") as f:
        current_appinfo = json.load(f)
        f.close()
    current_version = current_appinfo["version"]
    current_update = current_appinfo["nano_revision"]

    # Install the app in the directory
    os.rename(APPLICATION, "%sSchach %s" % (CURRENT_DIR, ("%s.%s" % (current_version, str(current_update)))))

    # # Load the version info from the already-installed Schach, if it exists
    # if os.path.exists(INSTALL_IN + "Schach/json/appinfo.json"):
    #     with open(INSTALL_IN + "Schach/json/appinfo.json") as f:
    #         old_appinfo = json.load(f)
    #         f.close()
    #     old_version = old_appinfo["version"]
    #     old_update = old_appinfo["nano_revision"]

    #     if old_version == current_version:
    #         if old_update == current_update:
    #             print("You already have this version of Schach installed.")
    #             exit()

else:
    print("FATAL ERROR: Your system is not a Linux. This install cannot run.")