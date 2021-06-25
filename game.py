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

import chess
import chess.engine
import dialogs
import gi
import messagedialogs
import os
import sys

from constants import *
from gi.repository import Gtk

class Game:
    """The class that manages the chess game."""

    def __init__(self, window, chessboard, white_frame, black_frame, status_bar):
    
        # The last square that was clicked
        self.move_from = None
        self.move_to = None

        # The parent window for the dialogs
        self.window = window

        # The chessboard widget
        self.chessboard = chessboard
        self.chessboard.bind_move(self._push_move)
        self.chessboard.bind_promotion(self._promote)
        
        # The status widgets
        self.white_frame = white_frame
        self.black_frame = black_frame
        self.status_bar = status_bar

        # The limits for the computer
        self.white_limit = None
        self.black_limit = None

        # The board
        self.board = chess.Board()
        self.chessboard.from_board(self.board)

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

    def _assert_move(self, event):
        """Check all the move's stats, and if it's legal, move it."""

        # The square that was clicked
        square_name = self.chessboard.convert_screen_coords_to_square((event.x, event.y))
        ignore, square_piece = self.chessboard.convert_square_to_image(square_name)

        self.chessboard.update()

    def _game_over(self):
        """Handle the status and dialogs for the game's end."""

        if self.board.is_checkmate():
            self.status_bar.set_status(game_over="Checkmate")
            if self.board.turn:
                self.black_frame.set_status(we_won=True)
                self.white_frame.set_status(we_won=False)
                # Show the dialog
                if not self.dialog_ok:
                    messagedialogs.show_game_over_checkmate(self.window, "black")
                    self.dialog_ok = True
            else:
                self.white_frame.set_status(we_won=True)
                self.black_frame.set_status(we_won=False)
                # Show the dialog
                if not self.dialog_ok:
                    messagedialogs.show_game_over_checkmate(self.window, "white")
                    self.dialog_ok = True
        elif self.board.is_fivefold_repetition():
            self.status_bar.set_status(game_over="Draw (fivefold repetition)")
            if not self.dialog_ok:
                messagedialogs.show_game_over_fivefold_repetition(self.window)
                self.dialog_ok = True
        elif self.board.is_seventyfive_moves():
            self.status_bar.set_status(game_over="Draw (seventy-five moves)")
            if not self.dialog_ok:
                messagedialogs.show_game_over_seventyfive_moves(self.window)
                self.dialog_ok = True
        elif self.board.is_stalemate():
            self.status_bar.set_status(game_over="Stalemate")
            if not self.dialog_ok:
                messagedialogs.show_game_over_stalemate(self.window)
                self.dialog_ok = True
        else:
            self.status_bar.set_status(game_over="Draw")
            if not self.dialog_ok:
                messagedialogs.show_game_over(self.window)
                self.dialog_ok = True
        self.chessboard.set_sensitive(False)

    def _get_square_is_ours(self, square):
        """Return True if the piece at the square is ours, False otherwise.
        If there is no piece, return None."""
        piece_at_square = str(self.board.piece_at(chess.parse_square(self.move_from)))
        color_at_square = str(self.board.color_at(chess.parse_square(self.move_from)))

        # Is there a piece here?
        if piece_at_square != "None":

            # If so, is it ours?
            if str(color_at_square) == str(self.board.turn):
                return True
            else:
                return False
        else:
            return None

    def _move_is_legal(self, move):
        """Return True if MOVE is legal."""

        try:
            if chess.Move.from_uci(move) in self.board.legal_moves:
                return True
            else:
                return False
        except ValueError:
            return False

    def _promote(self):
        """Promote the current pawn."""
        if self.board.turn:
            color = "white"
        else:
            color = "black"
        promote_to = dialogs.PromotionDialog(self.window, color=color).show_dialog()
        self.chessboard.from_board(self.board)
        self.update_status()
        return promote_to

    def _push_move(self, move):
        """Push the move to the board and highlight the ending square of the move."""
        self.chessboard.from_board(self.board)
        self.board.push(move)
        self.chessboard.set_square_color(move.uci()[2:], COLOR_MOVETO)
        self.update_status()

    def _reset_square_colors(self):
        """Set the colors of the squares back to their default."""

        self.chessboard.squaresdict = {}

    def _set_square_color(self, color, square_name, isolate=True):
        """Set the SQUARE to COLOR, and all the other squares 
        to their default colors if ISOLATE == True"""
        
        # Configure that square and set it's color
        if isolate:
            self.chessboard.squaresdict = {}
        self.chessboard.squaresdict[square_name] = color

    def engine_move(self):
        """Make the engine this turn."""

        if not self.board.is_game_over():

            # Set the spinner going
            while Gtk.events_pending():
                Gtk.main_iteration()

            # Move the right time for the right turn
            if self.board.turn:
                limit = self.white_limit
                self.white_frame.set_status(thinking=True)
                self.status_bar.set_status(turn=self.board.turn, thinking=True)
            else:
                limit = self.black_limit
                self.black_frame.set_status(thinking=True)
                self.status_bar.set_status(turn=self.board.turn, thinking=True)

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
            self.chessboard.from_board(self.board)

            # Hide the spinners
            self.white_frame.set_status(thinking=False)
            self.black_frame.set_status(thinking=False)

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
                    self.chessboard.from_board(self.board)
                    self.chessboard.set_square_color(move.uci()[2:], COLOR_MOVETO)
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
            self.chessboard.from_board(self.board)
            self.chessboard.set_square_color(move.uci()[:2], COLOR_MOVETO)
        except IndexError:
            pass
        self.update_status()

    def new_game(self, game=None):
        """Create a new game."""

        # Reset the game
        self.board.reset()

        # Reset the chessboard
        self.chessboard.set_sensitive(True)
        self._reset_square_colors()
        self.chessboard.from_board(self.board)
        self.dialog_ok = False

        # Make the moves in the chess.dcn.Game instance, if one was given
        if game is not None:
            self.board = game.board
            self.chessboard.from_board(self.board)

        # Update the status
        self.update_status()

    def new_game_from_pgn(self, game):
        """Create a new game from a chess.pgn.Game instance."""

        # Reset the game
        self.board.reset()

        # Reset the chessboard
        self.chessboard.set_sensitive(True)
        self._reset_square_colors()
        self.chessboard.from_board(self.board)
        self.dialog_ok = False

        # Make the moves in the chess.dcn.Game instance, if one was given
        if game is not None:
            for move in game.mainline_moves():
                self.board.push(move)
            self.chessboard.from_board(self.board)

        # Update the status
        self.update_status()

    def new_game_from_fen(self, fen=None):
        """Create a new game from a fen string."""

        # Reset the game
        self.board.reset()

        # Reset the chessboard
        self.chessboard.set_sensitive(True)
        self._reset_square_colors()
        self.chessboard.from_board(self.board)
        self.dialog_ok = False

        # Make the board
        self.board.set_board_fen(fen)
        self.chessboard.from_board(self.board)

        # Update the status
        self.update_status()

    def set_limit(self, white_limit=None, black_limit=None):
        """Set the limits for the computer."""

        if white_limit is not None:
            self.white_limit = chess.engine.Limit(depth=white_limit)
        if black_limit is not None:
            self.black_limit = chess.engine.Limit(depth=black_limit)

    def update_status(self):
        """Update the status labels."""

        self.white_frame.set_status(board=str(self.board))
        self.black_frame.set_status(board=str(self.board))
        
        self.status_bar.set_status(fen=self.board.board_fen(), turn=self.board.turn)

        if self.board.is_game_over():
            self._game_over()
        else:
            self.white_frame.set_status(we_won=False)
            self.black_frame.set_status(we_won=False)
            if self.board.turn:
                if self.board.is_check():
                    self.white_frame.set_status(check=True)
                    self.status_bar.set_status(check=True)
                else:
                    self.white_frame.set_status(check=False)
                    self.status_bar.set_status(check=False)
            else:
                if self.board.is_check():
                    self.black_frame.set_status(check=True)
                    self.status_bar.set_status(check=True)
                else:
                    self.black_frame.set_status(check=False)
                    self.status_bar.set_status(check=False)