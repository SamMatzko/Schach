import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

def show_game_over_checkmate(parent, color="white"):
    dialog = Gtk.MessageDialog(
        transient_for=parent,
        message_type=Gtk.MessageType.INFO,
        title="Checkmate!",
        text=f"{color.title()} wins!"
    )
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
        title="Game over!",
        text="The game ended due to fivefold repetition."
    )
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
        title="Game over!",
        text="The game ended due to the seventy-five move rule."
    )
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
        title="Stalemate!",
        text="The game ended in a stalemate."
    )
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
        print(show_game_over_checkmate(window))
        print(show_game_over_fivefold_repetition(window))
        print(show_game_over_seventyfive_moves(window))
        print(show_game_over_stalemate(window))
    window.connect("delete-event", Gtk.main_quit)
    window.connect("key-press-event", show)
    window.show_all()
    Gtk.main()