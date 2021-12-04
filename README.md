<h1>Schach</h1>

Schach is a chess app written in Python, that uses Gtk and the powerful Stockfish chess engine. It has full undo-redo functionality, 21 different playing levels for
each side including a random move feature, and help docs that are still in progress. See the Issues tab for all known errors and todos, and please add to that list
if you think something can be improved.

<h2>Installation</h2>

<h3>For Linux</h3>

For now, the install file only works for Linux. If you have a Linux, just unzip the Schach directory wherever you want it, and then run the install file 
(either `install.sh` or `install.py`).

<h3>For other Operating Systems</h3>

I haven't been able to write install scripts for Windows or Mac, because I don't have ready access to, or use, either OS. So, unfortunately, installing Schach on
another operating system requires you to manually install Schach. This takes a bit of work, so if any of you want to help me write an install program (preferably in
Python) for Windows and/or Mac, that'd be great!

You can use the template (`data/desktop.template`) to set up your own desktop file on your OS. To set up the settings file, create a new directory in your home
directory named `.schach`. Copy `data/settings-default.json` into `HOME.schach/`, and rename it to `settings.json`.
