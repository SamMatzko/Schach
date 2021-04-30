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

class AboutDialog:
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

class HeadersDialog(_Dialog):
    """The dialog in which users can edit the game's headers.
    
    Valid results for OVERRIDE_RESULT are:
        1 - 0, 0 - 1, 1/2 - 1/2, and *"""

    def __init__(self, parent, override_result=None):
        _Dialog.__init__(
            self,
            title="Save: Add New Game",
            transient_for=parent,
            modal=True)

        # The area to which we can add everything
        self.area = self.get_content_area()

        # The box containing the headers
        self.headers_box = Gtk.VBox()

        # The dictionary containing the headers given by the user
        self.headers = None

        # Whether the result of the game has already been determined
        self.override_result = override_result

        # Create the headers box
        self._create_headers_box()

        # Set the buttons
        self._create_buttons()

        self.show_all()

    def _create_buttons(self):
        """Create the buttons of the dialog."""

        # The buttons
        buttons = (
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL),
            (Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
        )

        # Add the buttons
        for button in buttons:
            self.add_button(button[0], button[1])

    def _create_headers_box(self):
        """Create all the header editing elements and add them to the header box."""

        # The event header
        self.event_header_box = Gtk.HBox()
        self.area.pack_start(self.event_header_box, True, True, 2)
        self.event_header_label = Gtk.Label(label="Event: ")
        self.event_header_entry = Gtk.Entry()
        self.event_header_box.pack_start(self.event_header_label, False, False, 2)
        self.event_header_box.pack_end(self.event_header_entry, False, False, 2)

        # The site header
        self.site_header_box = Gtk.HBox()
        self.area.pack_start(self.site_header_box, True, True, 2)
        self.site_header_label = Gtk.Label(label="Site: ")
        self.site_header_entry = Gtk.Entry()
        self.site_header_box.pack_start(self.site_header_label, False, False, 2)
        self.site_header_box.pack_end(self.site_header_entry, False, False, 2)

        # The date header
        self.date_header_box = Gtk.HBox()
        self.area.pack_start(self.date_header_box, True, True, 2)
        self.date_header_label = Gtk.Label(label="Date:")
        self.date_header_box.pack_start(self.date_header_label, False, False, 2)

        # The date header entries
        self.date_header_entry_box = Gtk.HBox()
        Gtk.StyleContext.add_class(self.date_header_entry_box.get_style_context(), "linked")
        self.date_header_box.pack_end(self.date_header_entry_box, False, False, 2)

        self.date_header_year_entry = Gtk.Entry()
        self.date_header_year_entry.set_width_chars(4)
        self.date_header_year_entry.set_max_length(4)
        self.date_header_year_entry.insert_text("????", 0)
        self.date_header_entry_box.pack_start(self.date_header_year_entry, False, False, 0)

        self.date_header_entry_box.pack_start(Gtk.Label(label="/"), False, False, 1)

        self.date_header_month_entry = Gtk.Entry()
        self.date_header_month_entry.set_width_chars(2)
        self.date_header_month_entry.set_max_length(2)
        self.date_header_month_entry.insert_text("??", 0)
        self.date_header_entry_box.pack_start(self.date_header_month_entry, False, False, 0)

        self.date_header_entry_box.pack_start(Gtk.Label(label="/"), False, False, 1)

        self.date_header_day_entry = Gtk.Entry()
        self.date_header_day_entry.set_width_chars(2)
        self.date_header_day_entry.set_max_length(2)
        self.date_header_day_entry.insert_text("??", 0)
        self.date_header_entry_box.pack_start(self.date_header_day_entry, False, False, 0)

        # The calnedar button
        self.calendar_button = Gtk.Button.new_from_icon_name("x-office-calendar-symbolic", 1)
        self.date_header_entry_box.pack_start(self.calendar_button, False, False, 0)

        # The round header
        self.round_header_box = Gtk.HBox()
        self.area.pack_start(self.round_header_box, True, True, 2)
        self.round_header_label = Gtk.Label(label="Round: ")
        self.round_header_entry = Gtk.Entry()
        self.round_header_box.pack_start(self.round_header_label, False, False, 2)
        self.round_header_box.pack_end(self.round_header_entry, False, False, 2)

        # The white header
        self.white_header_box = Gtk.HBox()
        self.area.pack_start(self.white_header_box, True, True, 2)
        self.white_header_label = Gtk.Label(label="White: ")
        self.white_header_entry = Gtk.Entry()
        self.white_header_box.pack_start(self.white_header_label, False, False, 2)
        self.white_header_box.pack_end(self.white_header_entry, False, False, 2)

        # The black header
        self.black_header_box = Gtk.HBox()
        self.area.pack_start(self.black_header_box, True, True, 2)
        self.black_header_label = Gtk.Label(label="Black: ")
        self.black_header_entry = Gtk.Entry()
        self.black_header_box.pack_start(self.black_header_label, False, False, 2)
        self.black_header_box.pack_end(self.black_header_entry, False, False, 2)
        
        # The result header
        self.result_header_box = Gtk.HBox()
        self.area.pack_start(self.result_header_box, True, True, 2)
        self.result_header_label = Gtk.Label(label="Result: ")
        self.result_header_box.pack_start(self.result_header_label, False, False, 2)

        # The result options
        self.results_box = Gtk.HBox()
        self.result_header_box.pack_end(self.results_box, True, True, 2)
        self.result_w_b = Gtk.RadioButton.new_with_label_from_widget(None, "1 - 0")
        self.result_w_b.connect("toggled", self._on_result_set, "0")
        self.results_box.pack_start(self.result_w_b, False, False, 2)
        self.result_b_w = Gtk.RadioButton.new_from_widget(self.result_w_b)
        self.result_b_w.set_label("0 - 1")
        self.result_b_w.connect("toggled", self._on_result_set, "1")
        self.results_box.pack_start(self.result_b_w, False, False, 2)
        self.result_1_2 = Gtk.RadioButton.new_from_widget(self.result_w_b)
        self.result_1_2.set_label("1/2 - 1/2")
        self.result_1_2.connect("toggled", self._on_result_set, "2")
        self.results_box.pack_start(self.result_1_2, False, False, 2)
        self.result_unfinished = Gtk.RadioButton.new_from_widget(self.result_w_b)
        self.result_unfinished.set_label("*")
        self.result_unfinished.connect("toggled", self._on_result_set, "3")
        self.results_box.pack_start(self.result_unfinished, False, False, 2)

        # Set whether the user is allowed to set the result
        if self.override_result is not None:
            self.result = self.override_result

            # Set the result radiobutton
            if self.result == "1 - 0":
                self.result_w_b.set_active(True)
            elif self.result == "0 - 1":
                self.result_b_w.set_active(True)
            elif self.result == "1/2 - 1/2":
                self.result_1_2.set_active(True)
            else:
                self.result_unfinished.set_active(True)

            # Set the radiobuttons insensitive
            self.result_header_box.set_sensitive(False)

    def _destroy(self, *args):
        """Close the dialog properly."""

        if self.headers == None:
    
            # Set the headers variable to a dictionary
            self.headers = {}

            # Get all the info for the headers
            self.headers["Event"] = self.event_header_entry.get_text()
            self.headers["Site"] = self.site_header_entry.get_text()
            self.headers["Date"] = "%s.%s.%s" % (
                self.date_header_year_entry.get_text(),
                self.date_header_month_entry.get_text(),
                self.date_header_day_entry.get_text()
            )
            self.headers["Round"] = self.round_header_entry.get_text()
            self.headers["White"] = self.white_header_entry.get_text()
            self.headers["Black"] = self.black_header_entry.get_text()
            self.headers["Result"] = self.result
        
        # Destroy us
        self.destroy()
        
    def _on_result_set(self, radio, name):
        
        if radio.get_active():
            if name == "0":
                self.result = "1 - 0"
            elif name == "1":
                self.result = "0 - 1"
            elif name == "2":
                self.result = "1/2 1/2"
            elif name == "3":
                self.result = "*"

    def show_dialog(self):
        """Run the dilaog and return the user's response."""

        # Run the dialog
        response = self.run()

        # Destroy the dialog
        self.destroy()

        # Return the reply
        return response, self.headers

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
        print(HeadersDialog(window, "1/2 - 1/2").show_dialog())
        # print(PromotionDialog(window).show_dialog())
        # print(PromotionDialog(window, "black").show_dialog())
        # print(NewGameDialog(window).show_dialog())

    window.connect("delete-event", Gtk.main_quit)
    window.connect("key-press-event", sd)
    Gtk.main()