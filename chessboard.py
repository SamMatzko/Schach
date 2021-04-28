import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from constants import *
from gi.repository import Gdk, Gtk

class ChessBoard(Gtk.Grid):
    """The chessboard widget."""

    def __init__(self, string=None):

        Gtk.Grid.__init__(self)
        self._create_squares()
        self.set_no_show_all(False)

        if string is not None:
            self.from_string(string)

        self.show_all()

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

                # Set which piece is for this square
                if r == "1":
                    if c == "a" or c == "h":
                        image = IMAGE_R
                    elif c == "b" or c == "g":
                        image = IMAGE_N
                    elif c == "c" or c == "f":
                        image = IMAGE_B
                    elif c == "d":
                        image = IMAGE_Q
                    elif c == "e":
                        image = IMAGE_K
                elif r == "2":
                    image = IMAGE_P
                elif r == "8":
                    if c == "a" or c == "h":
                        image = IMAGE_r
                    elif c == "b" or c == "g":
                        image = IMAGE_n
                    elif c == "c" or c == "f":
                        image = IMAGE_b
                    elif c == "d":
                        image = IMAGE_q
                    elif c == "e":
                        image = IMAGE_k
                elif r == "7":
                    image = IMAGE_p

                # Execute the squares' creation so that we don't have
                # to type 192 lines
                exec(f"self.{c}{r} = Square(color='{color}', name='{c}{r}', image=Gtk.Image.new_from_file(image))")
                exec(f"self.{c}{r}.color = '{color}'")
                exec(f"self.attach(self.{c}{r}, {cindex + 1}, {rindex + 1}, 1, 1)")

    def from_string(self, string):
        """Rearrange the board according to STRING."""

        string = string.replace("\n", " ").split()
        for sint in range(0, 64):
            s = BOARD_ORDER[sint]
            exec(f"square = self.{s}")
            if string[sint] == ".":
                exec("square.reload(Gtk.Image.new_from_file(IMAGE_EMPTY))")
            else:
                exec(f"square.reload(Gtk.Image.new_from_file(IMAGE_{string[sint]}))")

        self.hide()
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

    def reload(self, image):
        
        self.remove(self.image)
        self.image = image
        self.image.connect("draw", self._on_draw, {"color": self.rgba})
        self.add(self.image)