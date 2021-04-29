"""The dialogs for Schach."""
import gi

gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")

from constants import *
from gi.repository import Gtk, Gdk, GdkPixbuf

class _Dialog(Gtk.Dialog):
    """The base class for the dialogs."""

    def __init__(self, *args, **kwargs):
        Gtk.Dialog.__init__(self, *args, **kwargs)
        self.set_resizable(False)

        # Connect "escape" so that the dialog closes
        self.connect("key-press-event", self._on_key_press)
        self.connect("delete-event", self._destroy)

    def _destroy(self, *args):
        """Destroy the dialog."""
        self.destroy()

    def _on_key_press(self, widget, event):
        """Close the dialog if the key pressed was "escape"."""
        if event.keyval == Gdk.KEY_Escape:
            self._destroy()

class AbouDialog:
    """The class that handles the about dialog."""

    def __init__(self, parent, info):
        self.dialog = Gtk.AboutDialog(
            transient_for=parent,
            modal=True
        )
        self.dialog.set_artists(info["artists"])
        self.dialog.set_authors(info["authors"])
        self.dialog.set_comments(info["comments"])
        self.dialog.set_copyright(info["copyright"])
        pixbuf = GdkPixbuf.Pixbuf().new_from_file_at_size(info["logo"], 100, 100)
        pixbuf
        self.dialog.set_logo(pixbuf)
        self.dialog.set_program_name(info["program_name"])
        self.dialog.set_version(info["version"])
    
    def present(self):
        self.dialog.present()

class NewGameDialog(_Dialog):
    """The dialog to set the settings for a new game."""

    def __init__(self, parent):
        _Dialog.__init__(
            self,
            title="New Game",
            transient_for=parent,
            modal=True
        )
        self.set_resizable(True)

        # The default settings
        self.settings = {
            "white_mode": "human",
            "black_mode": "human",
            "white_computer": 1, 
            "black_computer": 1
        }

        # The area to which we can add the grid
        self.area = self.get_content_area()

        # The grid
        self.main_box = Gtk.HBox()
        self.area.pack_start(self.main_box, True, True, 0)

        # The available modes
        self.modes = ["human", "computer"]
        self.mode_store = Gtk.ListStore(str)
        for mode in self.modes:
            self.mode_store.append([mode])

        # Draw the window
        self._create_window()

    def _create_black_frame(self):
        """Create the frame for black's settings."""

        # The main frame for black's settings
        self.black_frame = Gtk.Frame(label="Black")
        self.main_box.pack_start(self.black_frame, True, True, 5)

        # The spacer boxes
        self.black_spacer_vbox = Gtk.VBox()
        self.black_spacer_hbox = Gtk.HBox()
        self.black_frame.add(self.black_spacer_vbox)
        self.black_spacer_vbox.pack_start(self.black_spacer_hbox, True, True, 5)

        # The grid for the settings
        self.black_grid = Gtk.Grid()
        self.black_spacer_hbox.pack_start(self.black_grid, True, True, 5)

        # The computer level slider
        self.black_computer_scale = Gtk.Scale.new_with_range(
            Gtk.Orientation.HORIZONTAL,
            0.0,
            20.0,
            1.0
        )

        # The mode combobx
        self.black_mode_selector = Gtk.ComboBox.new_with_model(self.mode_store)
        self.black_grid.attach(self.black_mode_selector, 0, 0, 1, 1)
        self.black_mode_selector.connect("changed", self._on_black_mode_changed)
        renderer_text = Gtk.CellRendererText()
        self.black_mode_selector.pack_start(renderer_text, True)
        self.black_mode_selector.add_attribute(renderer_text, "text", 0)
        self.black_mode_selector.set_active(0)

        self.black_computer_scale.set_tooltip_text("Computer playing power")
        self.black_computer_scale.set_sensitive(False)
        self.black_grid.attach(self.black_computer_scale, 0, 1, 1, 1)

        # The spacer label to make things wider
        self.black_spacer_label = Gtk.Label(label=" "*80)
        self.black_grid.attach(self.black_spacer_label, 0, 2, 1, 1)

    def _create_white_frame(self):
        """Create the frame for white's settings."""

        # The main frame for white's settings
        self.white_frame = Gtk.Frame(label="White")
        self.main_box.pack_start(self.white_frame, True, True, 5)

        # The spacer boxes
        self.white_spacer_vbox = Gtk.VBox()
        self.white_spacer_hbox = Gtk.HBox()
        self.white_frame.add(self.white_spacer_vbox)
        self.white_spacer_vbox.pack_start(self.white_spacer_hbox, True, True, 5)

        # The grid for the settings
        self.white_grid = Gtk.Grid()
        self.white_spacer_hbox.pack_start(self.white_grid, True, True, 5)

        # The computer level slider
        self.white_computer_scale = Gtk.Scale.new_with_range(
            Gtk.Orientation.HORIZONTAL,
            0.0,
            20.0,
            1.0
        )

        # The mode combobx
        self.white_mode_selector = Gtk.ComboBox.new_with_model(self.mode_store)
        self.white_grid.attach(self.white_mode_selector, 0, 0, 1, 1)
        self.white_mode_selector.connect("changed", self._on_white_mode_changed)
        renderer_text = Gtk.CellRendererText()
        self.white_mode_selector.pack_start(renderer_text, True)
        self.white_mode_selector.add_attribute(renderer_text, "text", 0)
        self.white_mode_selector.set_active(0)

        self.white_computer_scale.set_tooltip_text("Computer playing power")
        self.white_computer_scale.set_sensitive(False)
        self.white_grid.attach(self.white_computer_scale, 0, 1, 1, 1)

        # The spacer label to make things wider
        self.white_spacer_label = Gtk.Label(label=" "*80)
        self.white_grid.attach(self.white_spacer_label, 0, 2, 1, 1)

    def _create_window(self):
        """Create all the elements of the window."""
        
        # Create the white frame
        self._create_white_frame()

        # Create the black frame
        self._create_black_frame()

        # Show everything
        self.show_all()

    def _destroy(self, *args):
        """Close the dialog properly."""

        # Get the settings from the sliders
        self.settings["white_computer"] = self.white_computer_scale.get_value()
        self.settings["black_computer"] = self.black_computer_scale.get_value()

        # Destroy the dialog
        self.destroy()

    def _on_black_mode_changed(self, combo):

        # Configure the combo
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            mode = model[tree_iter][0]
            self.settings["black_mode"] = mode
        
        # Configure the scale
        if mode == "computer":
            self.black_computer_scale.set_sensitive(True)
        else:
            self.black_computer_scale.set_sensitive(False)

    def _on_white_mode_changed(self, combo):

        # Configure the combo
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            mode = model[tree_iter][0]
            self.settings["white_mode"] = mode
        
        # Configure the scale
        if mode == "computer":
            self.white_computer_scale.set_sensitive(True)
        else:
            self.white_computer_scale.set_sensitive(False)

    def show_dialog(self):
        """Run the dilaog and return the user's response."""

        # Run the dialog
        self.run()

        # Destroy the dialog
        self.destroy()

        # Return the variable
        return self.settings

class PromotionDialog(_Dialog):
    """The dialog that shows when a piece is promoted."""

    def __init__(self, parent, color="white"):
        _Dialog.__init__(
            self,
            title="Promotion!",
            transient_for=parent,
            modal=True
        )
        self.set_resizable(False)

        # The color of the piece we are promoting
        self.color = color

        # The area to which we can add the button box
        self.area = self.get_content_area()

        # The variable to return, containing the piece to promote to.
        # Default is queen.
        if self.color == "white":
            self.variable_to_return = "Q"
        else:
            self.variable_to_return = "q"

        # The button box
        self.box = Gtk.HBox()
        self.area.add(self.box)

        # Create the buttons and their images
        self._create_buttons()

        # Show all
        self.show_all()

    def _create_buttons(self):
        """Create the buttons and assign their images."""

        if self.color == "white":
            queen_image = IMAGE_Q
            rook_image = IMAGE_R
            bishop_image = IMAGE_B
            knight_image = IMAGE_N
        else:
            queen_image = IMAGE_q
            rook_image = IMAGE_r
            bishop_image = IMAGE_b
            knight_image = IMAGE_n

        # The queen_button
        self.queen_button = Gtk.Button()
        self.queen_button.connect("clicked", self._on_click, "q")
        self.queen_image = Gtk.Image.new_from_file(queen_image)
        self.queen_button.set_image(self.queen_image)
        self.box.add(self.queen_button)

        # The rook_button
        self.rook_button = Gtk.Button()
        self.rook_button.connect("clicked", self._on_click, "r")
        self.rook_image = Gtk.Image.new_from_file(rook_image)
        self.rook_button.set_image(self.rook_image)
        self.box.add(self.rook_button)

        # The bishop_button
        self.bishop_button = Gtk.Button()
        self.bishop_button.connect("clicked", self._on_click, "b")
        self.bishop_image = Gtk.Image.new_from_file(bishop_image)
        self.bishop_button.set_image(self.bishop_image)
        self.box.add(self.bishop_button)

        # The knight_button
        self.knight_button = Gtk.Button()
        self.knight_button.connect("clicked", self._on_click, "n")
        self.knight_image = Gtk.Image.new_from_file(knight_image)
        self.knight_button.set_image(self.knight_image)
        self.box.add(self.knight_button)

    def _on_click(self, widget, peice):
        """Set the varaible-to-return to the piece that was clicked."""

        # Destroy the dilaog
        self.destroy()

        # Set the variable-to-return
        if self.color == "white":
            self.variable_to_return = peice.upper()
        else:
            self.variable_to_return = peice.lower()

    def show_dialog(self):
        """Run the dilaog and return the user's response."""

        # Run the dialog
        self.run()
        self.destroy()

        # Return the variable
        return self.variable_to_return

if __name__ == "__main__":
    window = Gtk.Window()
    window.add(Gtk.Label(label="Press a key to see the dialogs."))
    window.show_all()
    def sd(*args):
        # print(PromotionDialog(window).show_dialog())
        # print(PromotionDialog(window, "black").show_dialog())
        print(NewGameDialog(window).show_dialog())

    window.connect("delete-event", Gtk.main_quit)
    window.connect("key-press-event", sd)
    Gtk.main()