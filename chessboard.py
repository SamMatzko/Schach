import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")

from constants import *
from gi.repository import Gdk, Gtk

class ChessBoard(Gtk.Grid):
    """The chessboard widget."""

    def __init__(self, parent=None, string=None):

        Gtk.Grid.__init__(self)
        self._create_squares()
        self.set_no_show_all(False)

        if string is not None:
            self.from_string(string)

        # The parent
        self.parent = parent

        # The fuction to call when a square is invoked
        self.square_function = None

        self.show_all()

    def _bound_method(self, widget):
        """The method called when a square is invoked."""

        # Call the method if it exists
        if self.square_function != None:
            self.square_function(
                {
                    "square": widget,
                    "location": widget.get_name(),
                    "piece": widget.get_piece()
                }
            )
        else:
            raise TypeError("Cannot call type 'None'.")

    def _create_squares(self):
        for c in LETTERS:
            for r in NUMBERS:

                # Get the row/column numbers
                cindex = LETTERS.index(c)
                NUMBERS.reverse()
                rindex = NUMBERS.index(r)
                NUMBERS.reverse()

                # Set the color of the square
                if str(c) in ODD_LETTERS:
                    if str(r) in ODD_NUMBERS:
                        color = BLACK
                    else:
                        color = WHITE
                else:
                    if str(r) in ODD_NUMBERS:
                        color = WHITE
                    else:
                        color = BLACK

                # Reset the image
                image = IMAGE_EMPTY
                image_name = "."

                # Set which piece is for this square
                if r == "1":
                    if c == "a" or c == "h":
                        image = IMAGE_R
                        image_name = "R"
                    elif c == "b" or c == "g":
                        image = IMAGE_N
                        image_name = "N"
                    elif c == "c" or c == "f":
                        image = IMAGE_B
                        image_name = "B"
                    elif c == "d":
                        image = IMAGE_Q
                        image_name = "Q"
                    elif c == "e":
                        image = IMAGE_K
                        image_name = "K"
                elif r == "2":
                    image = IMAGE_P
                    image_name = "P"
                elif r == "8":
                    if c == "a" or c == "h":
                        image = IMAGE_r
                        image_name = "r"
                    elif c == "b" or c == "g":
                        image = IMAGE_n
                        image_name = "n"
                    elif c == "c" or c == "f":
                        image = IMAGE_b
                        image_name = "b"
                    elif c == "d":
                        image = IMAGE_q
                        image_name = "q"
                    elif c == "e":
                        image = IMAGE_k
                        image_name = "k"
                elif r == "7":
                    image = IMAGE_p
                    image_name = "p"

                # Execute the squares' creation so that we don't have
                # to type 192 lines
                exec(f"iii = Gtk.Image.new_from_file(image)")
                exec(f"iii.set_name(image_name)")
                exec(f"self.{c}{r} = Square(color='{color}', name='{c}{r}', image=iii)")
                exec(f"self.{c}{r}.color = '{color}'")
                exec(f"self.attach(self.{c}{r}, {cindex + 1}, {rindex + 1}, 1, 1)")

    def _get_squares(self):
        """Return a list of the squares."""

        # The list
        l = []

        for c in LETTERS:
            for r in NUMBERS:
                exec(f"l.append(self.{c}{r})")

        return(l)

    def bind_squares(self, func):
        """Bind all the squares at a "clicked" event to a call of function FUNC."""
        
        # Go through and bind all the squares to self._bound_method.
        # This method then calls func when it is called.
        for square in self._get_squares():
            square.connect("clicked", self._bound_method)

        # Set the square_function to be called by the squares
        self.square_function = func        

    def from_string(self, string):
        """Rearrange the board according to STRING."""

        string = string.replace("\n", " ").split()
        for sint in range(0, 64):
            s = BOARD_ORDER[sint]
            exec(f"square = self.{s}")
            if string[sint] == ".":
                exec("square.reload(Gtk.Image.new_from_file(IMAGE_EMPTY))")
            else:
                exec(f"iii = Gtk.Image.new_from_file(IMAGE_{string[sint]})")
                exec(f"iii.set_name('{string[sint]}')")
                exec(f"square.reload(iii)")
        self.show_all()

class Square(Gtk.Button):
    """A custom button for the chess squares."""

    def __init__(self, name, image, color="#ffffff"):
        Gtk.Button.__init__(self, name=name)

        self.rgba = Gdk.RGBA()
        self.rgba.parse(color)

        self.color = color

        self.image = image
        self.image.connect("draw", self._on_draw, {"color": self.rgba})

        self.add(image)

    def _on_draw(self, widget, cr, data):
        
        context = widget.get_style_context()
        self.cr = cr

        self.width = widget.get_allocated_width()
        self.height = widget.get_allocated_height()
        Gtk.render_background(context, self.cr, 0, 0, self.width, self.height)

        r, g, b, a = data["color"]
        self.cr.set_source_rgba(r, g, b, a)
        self.cr.rectangle(0, 0, self.width, self.height)
        self.cr.fill()

        self.set_tooltip_text(self.get_name())

    def get_piece(self):
        """Return a byte representing the chess piece that is currently
        on this square."""

        return self.image.get_name()

    def parse_color(self, color):
        """Return the Gdk.RGBA.parse(COLOR).to_string() string."""
        rgba = Gdk.RGBA()
        rgba.parse(color)
        return rgba.to_string()

    def reload(self, image):
        
        self.remove(self.image)
        self.image = image
        self.image.connect("draw", self._on_draw, {"color": self.rgba})
        self.add(self.image)

    def set_color(self, color):
        """Set the square's color to COLOR."""

        self.rgba = Gdk.RGBA()
        self.rgba.parse(color)

        self.reload(self.image)