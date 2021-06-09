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

"""Create a version of the application ready for unpacking."""

import os
import random
import shutil
import string
import sys

DIRNAME = ""

if "linux" in sys.platform.lower():

    APP_DIR = os.path.dirname(__file__)
    PARENT_DIR = os.path.dirname(APP_DIR) + "/"
    APP_DIR = APP_DIR + "/"
    os.system("mkdir %s" % PARENT_DIR + "schach")
    os.system("cp -r %sSchach/* %s/" % (PARENT_DIR, PARENT_DIR + "schach"))
    shutil.make_archive("%sschach" % PARENT_DIR, "zip", "%s%s/schach" % (PARENT_DIR, DIRNAME))
    shutil.rmtree("%sschach" % PARENT_DIR)

else:
    print("Your system is not a Linux. Zip aborted.")