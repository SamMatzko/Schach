import chess
import chessboard as cb
import gi
import unittest

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

BOARD_STRING = "2b4r/p3p1pp/1p2q3/Q1pn2kP/2bPnp2/1P5p/P1PrBP1P/RN2KBNR w KQkq - 0 1"

class SchachTestCase(unittest.TestCase):
    """The TestCase for Schach."""

    def create_test_chessboard(self):
        """Create a chessboard.ChessBoard widget for testing."""
        window = Gtk.Window()
        chessboard = cb.ChessBoard(window)
        window.add(chessboard)
        return window, chessboard

    def test_chessboard(self):
        """Test that the board and the chessboard are the same."""
        
        # Create the test chessboard
        window, chessboard = self.create_test_chessboard()

        # Create the test game
        game = chess.Board(BOARD_STRING)
        chessboard.from_string(str(game))

        self.assertEqual(str(game).replace("\n", " "), chessboard.get_board_string())

        window.destroy()

if __name__ == "__main__":
    unittest.main()