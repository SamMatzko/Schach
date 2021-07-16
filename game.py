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

"""The game manager."""

import gi
import os
import random
import sys

import chess
import chess.engine
import dialogs
import messagedialogs

from constants import *
from gi.repository import Gtk

class Game:
    """The class that manages the chess game."""

    def __init__(self):
    
        # The last square that was clicked
        self.move_from = None
        self.move_to = None

        # The limits for the computer
        self.white_limit = None
        self.black_limit = None

        # The board
        self.board = chess.Board()
        try: self.chessboard_function(board=self.board)
        except TypeError:
            pass

        # The stack of undone moves
        self.undo_stack = []

        # The variable telling whether the game over dialogs have been aknowledged
        self.dialog_ok = False

        # The chess engine. Set it as an executable if it is not already
        try:
            self.engine = chess.engine.SimpleEngine.popen_uci(f"{ROOT_PATH}stockfish")
        except PermissionError:

            # Do this command only if the system is LINUX-related, just to be safe.
            if "linux" in sys.platform.lower():
                os.system(f"chmod +x {ROOT_PATH}stockfish")
                self.engine = chess.engine.SimpleEngine.popen_uci(f"{ROOT_PATH}stockfish")
            else:
                print("FATAL ERROR: Cannot set up engine: engine is not executable.")
                print(f"Please set {ROOT_PATH}stockfish to be executable.")
                exit()

    def _game_over(self):
        """Handle the status and dialogs for the game's end."""

        if self.board.is_checkmate():
            self.status_function(game_over="Checkmate")
            if self.board.turn:
                self.status_function(winner="black")
                # Show the dialog
                if not self.dialog_ok:
                    self.show_game_over_checkmate("black")
                    self.dialog_ok = True
            else:
                self.status_function(winner="white")
                # Show the dialog
                if not self.dialog_ok:
                    self.show_game_over_checkmate("white")
                    self.dialog_ok = True
        elif self.board.is_fivefold_repetition():
            self.status_function(game_over="Draw (fivefold repetition)")
            if not self.dialog_ok:
                self.show_game_over_fivefold_repetition()
                self.dialog_ok = True
        elif self.board.is_seventyfive_moves():
            self.status_function(game_over="Draw (seventy-five moves)")
            if not self.dialog_ok:
                self.show_game_over_seventyfive_moves()
                self.dialog_ok = True
        elif self.board.is_stalemate():
            self.status_function(game_over="Stalemate")
            if not self.dialog_ok:
                self.show_game_over_stalemate()
                self.dialog_ok = True
        else:
            self.status_function(game_over="Draw")
            if not self.dialog_ok:
                self.show_game_over()
                self.dialog_ok = True
        self.chessboard_function(sensitive=False)

    def _promote(self):
        """Promote the current pawn."""
        if self.board.turn:
            color = "white"
        else:
            color = "black"
        promote_to = self.promote_function(color)
        self.chessboard_function(board=self.board)
        self.update_status()
        return promote_to

    def _push_move(self, move):
        """Push uci move MOVE"""
        self.board.push(move)
        self.chessboard_function(square_color=(move.uci()[2:], COLOR_MOVETO))
        self.chessboard_function(board=self.board)
        self.update_status()

    def _reset_square_colors(self):
        """Set the colors of the squares back to their default."""

        self.chessboard_function(square_color=False)

    def _set_square_color(self, color, square_name):
        """Set the SQUARE to COLOR."""
        
        self.chessboard_function(square_color=(square_name, color))

    def bind_chessboard(self, func):
        """Bind chessboard updates to a call of FUNC, giving parameters for it."""
        self.chessboard_function = func

    def bind_status(self, func):
        """Bind status updates to a call of FUNC, giving parameters for game status."""
        self.status_function = func

    def engine_move(self):
        """Make the engine this turn."""

        if not self.board.is_game_over():

            # Set the spinner going
            while Gtk.events_pending():
                Gtk.main_iteration()

            # Move the right time for the right turn
            if self.board.turn:
                limit = self.white_limit
                self.status_function(thinking="white")
            else:
                limit = self.black_limit
                self.status_function(thinking="black")

            # Show the spinners
            while Gtk.events_pending():
                Gtk.main_iteration()

            # Get the move from the engine
            if limit == None:
                engine_move = self.engine.play(self.board, chess.engine.Limit())
            else:
                engine_move = self.engine.play(self.board, limit)

            # Move the engine's move
            self._push_move(engine_move.move)

            # Clear the undo stack
            self.undo_stack = []

            # Set the move_to setting so we can update the last-moved square
            self.move_to = engine_move.move.uci()[2:]
            self.chessboard_function(board=self.board)

            # Hide the spinners
            self.status_function(thinking=False)

            # Update the status labels
            self.update_status()

    def get_game_status(self):
        """Return various status stuff about the game, like the number of each
        peice on the board, whether there is a check, whether the game has 
        ended, and if so, who has won."""

        return {
            "is_check": self.board.is_check(),
            "is_checkmate": self.board.is_checkmate(),
            "is_fivefold_repetition": self.board.is_fivefold_repetition(),
            "is_game_over": self.board.is_game_over(),
            "is_seventyfive_moves": self.board.is_seventyfive_moves(),
            "is_stalemate": self.board.is_stalemate(),
            "turn": self.board.turn,
            "board": str(self.board)
        }

    def move_redo(self):
        """Redo the last undone move."""
        
        try:
            if self.undo_stack != []:
                move = self.undo_stack.pop()
                try:
                    self._push_move(move)
                    self.chessboard_function(board=self.board)
                    self.chessboard_function(square_color=(move.uci()[2:], COLOR_MOVETO))
                except AssertionError:
                    pass
        except IndexError:
            pass
        self.update_status()

    def move_undo(self):
        """Undo the last move on the stack."""
        
        try:
            move = self.board.pop()
            # Undo the game's move
            self.undo_stack.append(move)

            # Update the board
            self.chessboard_function(board=self.board)
            self.chessboard_function(square_color=(move.uci()[:2], COLOR_MOVETO))
        except IndexError:
            pass
        self.update_status()

    def new_game(self, game=None):
        """Create a new game."""

        # Reset the game
        self.board.reset()

        # Reset the chessboard
        self.chessboard_function(sensitive=True)
        self._reset_square_colors()
        self.chessboard_function(board=self.board)
        self.dialog_ok = False

        # Make the moves in the chess.dcn.Game instance, if one was given
        if game is not None:
            self.board = game.board
            self.chessboard_function(board=self.board)

        self.status_function(white_move="")
        self.status_function(black_move="")

        # Update the status
        self.update_status()

    def new_game_from_pgn(self, game):
        """Create a new game from a chess.pgn.Game instance."""

        # Reset the game
        self.board.reset()

        # Reset the chessboard
        self.chessboard_function(sensitive=True)
        self._reset_square_colors()
        self.chessboard_function(board=self.board)
        self.dialog_ok = False

        # Make the moves in the chess.dcn.Game instance, if one was given
        if game is not None:
            for move in game.mainline_moves():
                self.board.push(move)
            self.chessboard_function(board=self.board)

        # Update the status
        self.update_status()

    def new_game_from_fen(self, fen=None):
        """Create a new game from a fen string."""

        # Reset the game
        self.board.reset()

        # Reset the chessboard
        self.chessboard_function(sensitive=True)
        self._reset_square_colors()
        self.chessboard_function(board=self.board)
        self.dialog_ok = False

        # Make the board
        self.board.set_board_fen(fen)
        self.chessboard_function(board=self.board)

        # Update the status
        self.update_status()

    def random_move(self):
        """Play a random move."""

        if not self.board.is_game_over():
            self._push_move(random.choice(self.board.legal_moves))

    def set_limit(self, white_limit=None, black_limit=None):
        """Set the limits for the computer."""

        if white_limit is not None:
            self.white_limit = chess.engine.Limit(depth=white_limit)
        if black_limit is not None:
            self.black_limit = chess.engine.Limit(depth=black_limit)

    def update_status(self):
        """Update the status labels."""

        self.status_function(board=str(self.board), fen=self.board.fen(), turn=self.board.turn)

        if self.board.is_game_over():
            self._game_over()
        else:
            self.status_function(winner=False, game_over=False)
            if self.board.turn:
                if self.board.is_check():
                    self.status_function(check="white")
                else:
                    self.status_function(check=False)
            else:
                if self.board.is_check():
                    self.status_function(check="black")
                else:
                    self.status_function(check=False)
        if self.board.turn:
            try:
                move = self.board.pop()
                self.status_function(black_move=self.board.san(move))
                self.board.push(move)
            except IndexError:
                pass
        else:
            try:
                move = self.board.pop()
                self.status_function(white_move=self.board.san(move))
                self.board.push(move)
            except IndexError:
                pass

    # ------ Methods for unbound stuff ------ 
    def chessboard_function(self, **kw):
        pass

    def promote_function(self, color="white"):
        return "q"

    def show_game_over(self):
        pass

    def show_game_over_checkmate(self, winner):
        pass

    def show_game_over_fivefold_repetition(self):
        pass

    def show_game_over_seventyfive_moves(self):
        pass
    
    def show_game_over_stalemate(self):
        pass

    def status_function(self, **kwargs):
        pass