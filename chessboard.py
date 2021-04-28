import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from constants import *
from gi.repository import Gdk, Gtk

class ChessBoard(Gtk.Grid):
    """The chessboard widget."""

    def __init__(self):

        Gtk.Grid.__init__(self)

        self._define_icons()
        self._create_squares()

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
                        image = IMAGE_ROOK_W
                    elif c == "b" or c == "g":
                        image = IMAGE_KNIGHT_W
                    elif c == "c" or c == "f":
                        image = IMAGE_BISHOP_W
                    elif c == "d":
                        image = IMAGE_QUEEN_W
                    elif c == "e":
                        image = IMAGE_KING_W
                elif r == "2":
                    image = IMAGE_PAWN_W
                elif r == "8":
                    if c == "a" or c == "h":
                        image = IMAGE_ROOK_B
                    elif c == "b" or c == "g":
                        image = IMAGE_KNIGHT_B
                    elif c == "c" or c == "f":
                        image = IMAGE_BISHOP_B
                    elif c == "d":
                        image = IMAGE_QUEEN_B
                    elif c == "e":
                        image = IMAGE_KING_B
                elif r == "7":
                    image = IMAGE_PAWN_B

                # Execute the squares' creation so that we don't have
                # to type 192 lines
                exec(f"self.{c}{r} = Square(color='{color}', image=Gtk.Image.new_from_file(image))")
                exec(f"self.{c}{r}.color = '{color}'")
                exec(f"self.attach(self.{c}{r}, {cindex + 1}, {rindex + 1}, 1, 1)")

    def _define_icons(self):
        
        self.empty = Gtk.Image.new_from_file(IMAGE_EMPTY)
        self.K = Gtk.Image.new_from_file(IMAGE_KING_W)
        self.k = Gtk.Image.new_from_file(IMAGE_KING_B)
        self.Q = Gtk.Image.new_from_file(IMAGE_QUEEN_W)
        self.q = Gtk.Image.new_from_file(IMAGE_QUEEN_B)
        self.B = Gtk.Image.new_from_file(IMAGE_BISHOP_W)
        self.b = Gtk.Image.new_from_file(IMAGE_BISHOP_B)
        self.N = Gtk.Image.new_from_file(IMAGE_KNIGHT_W)
        self.n = Gtk.Image.new_from_file(IMAGE_KNIGHT_B)
        self.R = Gtk.Image.new_from_file(IMAGE_ROOK_W)
        self.r = Gtk.Image.new_from_file(IMAGE_ROOK_B)
        self.P = Gtk.Image.new_from_file(IMAGE_PAWN_W)
        self.p = Gtk.Image.new_from_file(IMAGE_PAWN_B)

class Square(Gtk.Button):
    """A custom button for the chess squares."""

    def __init__(self, image, color="#ffffff"):
        Gtk.Button.__init__(self)

        self.rgba = Gdk.RGBA()
        self.rgba.parse(color)

        self.color = color

        self.image = image
        self.image.connect("draw", self._on_draw, {"color": self.rgba})

        self.add(image)

    def _on_draw(self, widget, cr, data):
        
        context = widget.get_style_context()

        width = widget.get_allocated_width()
        height = widget.get_allocated_height()
        Gtk.render_background(context, cr, 0, 0, width, height)

        r, g, b, a = data["color"]
        cr.set_source_rgba(r, g, b, a)
        cr.rectangle(0, 0, width, height)
        cr.fill()