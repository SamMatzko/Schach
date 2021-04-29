import chess
import chess.engine
import dialogs

from constants import *
from dialogs import messagedialog

class Game:
    """The class that manages the chess game."""

    def __init__(self, window, chessboard, white_frame, black_frame):
    
        # The last square that was clicked
        self.move_from = None
        self.move_to = None

        # The parent window for the dialogs
        self.window = window

        # The chessboard widget
        self.chessboard = chessboard
        
        # The status widgets
        self.white_frame = white_frame
        self.black_frame = black_frame

        # The limits for the computer
        self.white_limit = None
        self.black_limit = None

        # The board
        self.board = chess.Board()

        # The variable telling whether the game over dialogs have been aknowledged
        self.dialog_ok = False

        print("Configuring the chess engine...")

        # The chess engine. Set it as an executable if it is not already
        try:
            self.engine = chess.engine.SimpleEngine.popen_uci(f"{ROOT_PATH}stockfish")
        except PermissionError:
            print("Setting stockfish to be executable...")
            os.system(f"chmod +x {ROOT_PATH}stockfish")
            self.engine = chess.engine.SimpleEngine.popen_uci(f"{ROOT_PATH}stockfish")

        # Bind the chessboard to the move assertion method
        self.chessboard.bind_squares(self._assert_move)

    def _assert_move(self, info):
        """Check all the move's stats, and if it's legal, move it."""

        # The square that was clicked
        square = info["square"]
        square_name = info["location"]
        square_piece = info["piece"]


        # Only respond if the widget is not disabled
        if square.get_sensitive():

            # Check if we are on the starting square or the ending square of the move
            if self.move_from == None:
                self.move_from = square_name
                move = None
            else:
                self.move_to = square_name
                move = f"{self.move_from}{self.move_to}"
                move_from = self.move_from
                self.move_from = None

            # Check if the move is legal
            if move != None:
                legal = self._move_is_legal(move)
            else:
                legal = None
                
            # If we are on the starting square, make sure that one of our pieces is 
            # actually on it
            if move == None:
                
                # Get the piece (if there is any) on the starting square
                # and the color of that piece
                piece_at_square = str(self.board.piece_at(chess.parse_square(self.move_from)))
                color_at_square = str(self.board.color_at(chess.parse_square(self.move_from)))

                # Is there a piece here?
                if piece_at_square != "None":

                    # If so, is it ours?
                    if str(color_at_square) == str(self.board.turn):
                        pass
                    else:
                        self.move_from = None
                else:
                    self.move_from = None

            # If we are on the last square of the move...
            else:

                # Is the move legal? If so, move it.
                if legal:

                    # Make the move in the chess.Board
                    self.board.push(chess.Move.from_uci(move))

                # If the move is not legal, it may be a promotion. Check if this
                # is so, and if so, promote it.
                else:
                    piece_at_square = str(self.board.piece_at(chess.parse_square(move_from)))
                    color_at_square = self.board.color_at(chess.parse_square(move_from))

                    # If we're a black piece in rank 1 or a white one in rank 8...
                    if (
                            color_at_square == chess.WHITE and "8" in self.move_to or
                            color_at_square == chess.BLACK and "1" in self.move_to):

                        # ...and if we are a pawn...
                        if piece_at_square.lower() == "p":
                            if color_at_square == chess.WHITE:
                                color = "white"
                            else:
                                color = "black"

                            # ...promote us!
                            promote_to = dialogs.PromotionDialog(self.chessboard.parent, color=color).show_dialog()
                            self.board.push(chess.Move.from_uci(move + (promote_to.lower())))
                            self.chessboard.from_string(str(self.board))
                
                # Check if the game is over, and if so, handle all endgame stuff
                if self.board.is_game_over():
                    self._game_over()

                # Update the board and status
                self.chessboard.from_string(str(self.board))
                self._update_status()

    def _engine_move(self):
        """Make the engine this turn."""

        if not self.board.is_game_over():

            # Move the right time for the right turn
            if self.board.turn:
                limit = self.white_limit
            else:
                limit = self.black_limit
            # Get the move from the engine
            if limit == None:
                engine_move = self.engine.play(self.board, chess.engine.Limit())
            else:
                engine_move = self.engine.play(self.board, limit)

            # Move the engine's move
            self.board.push(engine_move.move)

            # Set the move_to setting so we can update the last-moved square
            self.move_to = engine_move.move.uci()[2:]
            self.chessboard.from_string(str(self.board))

            # Update the status labels
            self._update_status()

    def _game_over(self):
        """Handle the status and dialogs for the game's end."""

        if self.board.is_checkmate():
            if self.board.turn:
                self.black_frame.set_status(we_won=True)
                self.white_frame.set_status(we_won=False)
                # Show the dialog
                if not self.dialog_ok:
                    messagedialog.show_game_over_checkmate(self.window, "black")
                    self.dialog_ok = True
            else:
                self.white_frame.set_status(we_won=True)
                self.black_frame.set_status(we_won=False)
                # Show the dialog
                if not self.dialog_ok:
                    messagedialog.show_game_over_checkmate(self.window, "white")
                    self.dialog_ok = True
        elif self.board.is_fivefold_repetition():
            if not self.dialog_ok:
                messagedialog.show_game_over_fivefold_repetition(self.window)
                self.dialog_ok = True
        elif self.board.is_seventyfive_moves():
            if not self.dialog_ok:
                messagedialog.show_game_over_seventyfive_moves(self.window)
                self.dialog_ok = True
        elif self.board.is_stalemate():
            if not self.dialog_ok:
                messagedialog.show_game_over_stalemate(self.window)
                self.dialog_ok = True

    def _move_is_legal(self, move):
        """Return True if MOVE is legal."""

        if chess.Move.from_uci(move) in self.board.legal_moves:
            return True
        else:
            return False

    def _update_status(self):
        """Update the status labels."""

        self.white_frame.set_status(board=str(self.board))
        self.black_frame.set_status(board=str(self.board))
        if self.board.is_check():
            if self.board.turn:
                self.white_frame.set_status(check=True)
            else:
                self.black_frame.set_status(check=True)
        else:
            self.white_frame.set_status(check=False)
            self.black_frame.set_status(check=False)

            if self.board.is_game_over():
                self._game_over()
            else:
                self.white_frame.set_status(we_won=False)
                self.black_frame.set_status(we_won=False)

        if self.board.is_game_over():
            self._game_over()

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

    def move_undo(self):
        """Undo the last move on the stack."""

        # Undo the game's move
        self.board.pop()

        # Update the board
        self.chessboard.from_string(str(self.board))

    def new_game(self):
        """Create a new game."""

        # Reset the game
        self.board.reset()

        # Reset the chessboard
        self.chessboard.from_string(str(self.board))

        # Update the status
        self._update_status()

    def set_limit(self, white_limit=None, black_limit=None):
        """Set the limits for the computer."""

        if white_limit is not None:
            self.white_limit = chess.engine.Limit(depth=white_limit)
        if black_limit is not None:
            self.black_limit = chess.engine.Limit(depth=black_limit)