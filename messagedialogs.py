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

"""The message dialogs."""

import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

def ask_yes_no_cancel(parent, title, text):
    dialog = Gtk.MessageDialog(
        transient_for=parent,
        message_type=Gtk.MessageType.QUESTION,
        text=title
    )
    dialog.format_secondary_text(text)
    buttons = (
        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL),
        (Gtk.STOCK_NO, Gtk.ResponseType.NO),
        (Gtk.STOCK_YES, Gtk.ResponseType.YES)
    )
    for button in buttons:
        dialog.add_button(button[0], button[1])
    dialog.set_default_response(Gtk.ResponseType.CANCEL)
    response = dialog.run()
    dialog.destroy()
    return response

def show_game_over(parent):
    dialog = Gtk.MessageDialog(
        transient_for=parent,
        message_type=Gtk.MessageType.INFO,
        text="Game over!"
    )
    dialog.format_secondary_text("The game ended in a draw.")
    buttons = (
        (Gtk.STOCK_OK, Gtk.ResponseType.OK),
    )
    for button in buttons:
        dialog.add_button(button[0], button[1])
    dialog.run()
    dialog.destroy()

def show_game_over_checkmate(parent, color="white"):
    dialog = Gtk.MessageDialog(
        transient_for=parent,
        message_type=Gtk.MessageType.INFO,
        text="Checkmate!"
    )
    dialog.format_secondary_markup(f"{color.title()} wins!")
    buttons = (
        (Gtk.STOCK_OK, Gtk.ResponseType.OK),
    )
    for button in buttons:
        dialog.add_button(button[0], button[1])
    dialog.run()
    dialog.destroy()

def show_game_over_fivefold_repetition(parent):
    dialog = Gtk.MessageDialog(
        transient_for=parent,
        message_type=Gtk.MessageType.INFO,
        text="Game over!"
    )
    dialog.format_secondary_text("The game ended in a draw due to fivefold repetition.")
    buttons = (
        (Gtk.STOCK_OK, Gtk.ResponseType.OK),
    )
    for button in buttons:
        dialog.add_button(button[0], button[1])
    dialog.run()
    dialog.destroy()

def show_game_over_seventyfive_moves(parent):
    dialog = Gtk.MessageDialog(
        transient_for=parent,
        message_type=Gtk.MessageType.INFO,
        text="Game over!"
    )
    dialog.format_secondary_text("The game ended in a draw due to the seventy-five move rule.")
    buttons = (
        (Gtk.STOCK_OK, Gtk.ResponseType.OK),
    )
    for button in buttons:
        dialog.add_button(button[0], button[1])
    dialog.run()
    dialog.destroy()

def show_game_over_stalemate(parent):
    dialog = Gtk.MessageDialog(
        transient_for=parent,
        message_type=Gtk.MessageType.INFO,
        text="Stalemate!"
    )
    dialog.format_secondary_text("The game ended in a stalemate.")
    buttons = (
        (Gtk.STOCK_OK, Gtk.ResponseType.OK),
    )
    for button in buttons:
        dialog.add_button(button[0], button[1])
    dialog.run()
    dialog.destroy()

def show_info(parent, text="Info", secondary_text="Here is some info."):
    dialog = Gtk.MessageDialog(
        transient_for=parent,
        message_type=Gtk.MessageType.INFO,
        text=text
    )
    dialog.format_secondary_text(secondary_text)
    buttons = (
        (Gtk.STOCK_OK, Gtk.ResponseType.OK),
    )
    for button in buttons:
        dialog.add_button(button[0], button[1])
    dialog.run()
    dialog.destroy()

if __name__ == "__main__":
    window = Gtk.Window()
    def show(*args):
        print(ask_yes_no_cancel(window, "File not saved", "File has not been saved. Save file?"))
        print(show_game_over_checkmate(window))
        print(show_game_over_fivefold_repetition(window))
        print(show_game_over_seventyfive_moves(window))
        print(show_game_over_stalemate(window))
    window.connect("delete-event", Gtk.main_quit)
    window.connect("key-press-event", show)
    window.show_all()
    Gtk.main()