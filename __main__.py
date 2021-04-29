import app
import gi
import json

gi.require_version("Gtk", "3.0")

from constants import *
from gi.repository import Gtk

# Print the Scach version
appinfo = json.load(open(f"{ROOT_PATH}json/appinfo.json"))
print(f"Schach {appinfo['version']}")

if __name__ == "__main__":
    window = app.App()
    Gtk.main()