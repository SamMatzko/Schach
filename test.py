import chess
import chessboard as cb
import game
import gi
import unittest

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

BOARD_STRING = "2b4r/p3p1pp/1p2q3/Q1pn2kP/2bPnp2/1P5p/P1PrBP1P/RN2KBNR w KQkq - 0 1"
CHECKMATE = "4k3/8/8/8/8/8/1r6/Kq6 w KQkq - 0 67"

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

class GameManagerTestCase(unittest.TestCase):
    """Test game.py."""

    def create_test_chessboard(self):
        """Create a chessboard.ChessBoard widget for testing."""
        window = Gtk.Window()
        chessboard = cb.ChessBoard(window)
        window.add(chessboard)
        return window, chessboard

    def create_test_environment(self):
        window, chessboard = self.create_test_chessboard()
        board_game = chess.Board(CHECKMATE)
        chessboard.from_string(str(board_game).replace("\n", " "))
        game_manager = game.Game(window, chessboard, None, None)
        game_manager.board = board_game
        game_manager.engine.quit()
        return game_manager, chessboard, window

    def test_board(self):
        game_manager, chessboard, window = self.create_test_environment()
        self.assertEqual(str(game_manager.board).replace("\n", " "), chessboard.get_board_string())
        window.destroy()

    def test_game_status(self):
        game_manager, chessboard, window = self.create_test_environment()
        self.assertEqual(game_manager.board.is_game_over(), True)
        self.assertEqual(game_manager.dialog_ok, False)
        self.assertEqual(game_manager.board.is_checkmate(), True)
        window.destroy()

if __name__ == "__main__":
    unittest.main()