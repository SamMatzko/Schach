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

"""Schach test suite."""

import chess
import chess.dcn
import chess.pgn
import gi
import json
import unittest

import dcn
import game

gi.require_version("Gtk", "3.0")

from constants import *
from gi.repository import Gtk

BOARD_FEN = "2b4r/p3p1pp/1p2q3/Q1pn2kP/2bPnp2/1P5p/P1PrBP1P/RN2KBNR"
FEN = "2b4r/p3p1pp/1p2q3/Q1pn2kP/2bPnp2/1P5p/P1PrBP1P/RN2KBNR w KQkq - 0 1"
CHECKMATE = "4k3/8/8/8/8/8/1r6/Kq6 w KQkq - 0 67"
STATUS_LIST = {
    "board": "r n b q k b n r\np p p p p p p p\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\nP P P P P P P P\nR N B Q K B N R",
    "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "turn": True
}
DCN_FILE = """<game><header name="Event">A Test</header><header name="Site">This computer</header><header name="Date">1234.56.78</header><header name="Round">8</header><header name="White">A fake person</header><header name="Black">Dummy D. Dude</header><header name="Result">1-0</header><board fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" /><stack><move>a2a3</move><move>b8a6</move><move>e2e4</move></stack></game>\n\n\n"""
chessboard_method_tested = False
promote_method_tested = False
status_method_tested = False

class GameManagerTest(unittest.TestCase):
    """Tests for the Schach game manager (game.Game)."""

    def create_game_manager_instance(self):
        """Return a new game.Game instance."""
        game_manager = game.Game()
        game_manager.bind_status(self.test_status_method)
        return game_manager

    def bound_method(self):
        pass

    def test_bind_and_initialize(self):
        """Test the class's initialization and method binding."""
        game_manager = self.create_game_manager_instance()
        game_manager.engine.quit()
        game_manager.update_status()
        game_manager.promote_function = self.test_promote_function
        game_manager.bind_chessboard(self.test_chessboard_function)
        game_manager._promote()

    def test_chessboard_function(self, board=None):
        """Test the call to chessboard_function in game.Game._promote."""
        global chessboard_method_tested
        if not chessboard_method_tested:
            self.assertEqual(str(board), str(chess.Board()))
        chessboard_method_tested = True

    def test_engine_move(self):
        """Test the class's engine_move method."""
        global status_method_tested
        game_manager = self.create_game_manager_instance()
        game_manager.engine_move()
        game_manager.engine.quit()

    def test_method_binding(self):
        """Test the method binding for the game manager."""
        game_manager = self.create_game_manager_instance()
        game_manager.engine.quit()
        game_manager.bind_chessboard(self.bound_method)
        self.assertEqual(game_manager.chessboard_function, self.bound_method)
        game_manager.bind_status(self.bound_method)
        self.assertEqual(game_manager.status_function, self.bound_method)

    def test_move_redo(self):
        """Test the move_redo method."""
        game_manager = self.create_game_manager_instance()
        game_manager.engine.quit()
        game_manager._push_move(chess.Move.from_uci("a2a3"))
        game_manager.move_undo()
        # board_stack = game_manager.board.move_stack
        board_stack = []
        for item in game_manager.board.move_stack:
            board_stack.append(item)
        game_manager.move_redo()
        self.assertEqual(board_stack, [])
        self.assertEqual(game_manager.undo_stack, [])
        self.assertEqual(game_manager.board.move_stack, [chess.Move.from_uci("a2a3")])
    
    def test_move_undo(self):
        """Test the move_undo method."""
        game_manager = self.create_game_manager_instance()
        game_manager.engine.quit()
        board_stack = game_manager.board.move_stack
        game_manager._push_move(chess.Move.from_uci("a2a3"))
        self.assertEqual(game_manager.board.move_stack, [chess.Move.from_uci("a2a3")])
        self.assertEqual(game_manager.undo_stack, [])
        game_manager.move_undo()
        self.assertEqual(game_manager.board.move_stack, board_stack)
        self.assertEqual(game_manager.undo_stack, [chess.Move.from_uci("a2a3")])

    def test_new_game(self):
        """Test the new_game method."""
        game_manager = self.create_game_manager_instance()
        game_manager.engine.quit()
        game_manager._push_move(chess.Move.from_uci("a2a3"))
        game_manager.new_game()
        self.assertEqual(game_manager.undo_stack, [])
        self.assertEqual(game_manager.board, chess.Board())

    def test_new_game_from_dcn(self):
        """Test the new_game method, but give an argument."""
        game_manager = self.create_game_manager_instance()
        game_manager.engine.quit()
        dcn_game = chess.dcn.Game().from_file("%ssamples/game.dcn" % ROOT_PATH)
        game_manager.new_game(dcn_game)
        board = chess.Board()
        for move in dcn_game.moves:
            board.push(move)
        self.assertEqual(str(game_manager.board), str(board))
        game_manager.new_game()

    def test_new_game_from_fen(self):
        """Test the new_game_from_fen method."""
        game_manager = self.create_game_manager_instance()
        game_manager.engine.quit()
        board = chess.Board(BOARD_FEN)
        game_manager.new_game_from_fen(BOARD_FEN)
        self.assertEqual(str(game_manager.board), str(board))

    def test_new_game_from_pgn(self):
        """Test the new_game_from_pgn method."""
        game_manager = self.create_game_manager_instance()
        game_manager.engine.quit()
        with open("%ssamples/game.pgn" % ROOT_PATH) as f:
            pgn_game = chess.pgn.read_game(f)
            f.close()
        game_manager.new_game_from_pgn(pgn_game)
        board = chess.Board()
        for move in pgn_game.mainline_moves():
            board.push(move)
        self.assertEqual(game_manager.board, board)

    def test_promote_function(self, color=None):
        """Test the call to promote_function in the game.Game._promote method."""
        global promote_method_tested
        if not promote_method_tested:
            self.assertEqual(color, "white")
        promote_method_tested = True
        return "q"

    def test_push_move(self):
        """Test the _push_move method."""
        game_manager = self.create_game_manager_instance()
        game_manager.engine.quit()
        move = chess.Move.from_uci("a2a3")
        game_manager._push_move(move)
        self.assertEqual(game_manager.board.move_stack, [move])

    def test_status_method(self, *args, **kw):
        """The method to call when status is updated."""
        global status_method_tested
        if not status_method_tested:
            self.assertEqual(kw, STATUS_LIST)
        status_method_tested = True

class GameSaverTestCase(unittest.TestCase):
    """A test case for dcn and pgn game saving."""

    def create_chess_game(self):
        """Create a chess.Board instance to work with."""

        board = chess.Board()
        board.push_uci("a2a3")
        board.push_uci("b8a6")
        board.push_uci("e2e4")
        return board

    def test_parse_dcn(self):
        """Test dcn parsing by first writing a dcn to a file from a board, and
        then load it again and compare the data stored in the original game."""

        game_instance = chess.dcn.Game().from_board(self.create_chess_game())
        game_instance.write("%ssamples/game_.dcn" % ROOT_PATH)
        game_instance2 = chess.dcn.Game().from_file("%ssamples/game_.dcn" % ROOT_PATH)
        self.assertEqual(game_instance.moves, game_instance2.moves)
    
    def test_save_dcn(self):
        """Test dcn saving by writing a game to a file and then comparing it to
        a string that is what the file should look like."""

        # Create the game and write it to the file
        board = self.create_chess_game()
        game_instance = chess.dcn.Game().from_board(board)
        game_instance.set_headers(
            {
                "Event": "A Test",
                "Site": "This computer",
                "Date": "1234.56.78",
                "Round": "8",
                "White": "A fake person",
                "Black": "Dummy D. Dude",
                "Result": "1-0"
            }
        )
        dcn.save_game(game_instance, "%ssamples/game_.dcn" % ROOT_PATH)

        # Compare the file with what it should look like
        with open("%ssamples/game_.dcn" % ROOT_PATH) as f:
            file = f.read()
            f.close()
        self.assertEqual(file, DCN_FILE)

if __name__ == "__main__":
    unittest.main()