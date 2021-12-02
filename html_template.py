#!/usr/bin/python3

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

"""Uses the template to update all the html files in help/."""

import os

from constants import *

if __name__ == "__main__":

    # Load the template
    with open(HTML_TEMPLATE) as f:
        template = f.read()
        f.close()

    # Find all the files that in help/
    files = os.listdir(HELP_DIR)

    # Go through all the files and check if they start with "_"
    for file in files:
        abs_path = HELP_DIR + file

        if file.startswith("_") and os.path.isfile(abs_path):
            
            # Read the contents of the file
            with open(abs_path) as f:
                file_contents = f.read()
                f.close()
            
            # Replace "__BODY__" in the template with the file, and write that
            # to a new file under the same name, just without the "_".
            new_file_contents = template.replace("__BODY__", file_contents)

            new_file = HELP_DIR + file[1:]
            
            with open(new_file, "w") as f:
                f.write(new_file_contents)
                f.close()