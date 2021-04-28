import os

# The parent directory
ROOT_PATH = f"{os.path.dirname(__file__)}/"

# The lists of LETTERS and numbers
LETTERS = ["a", "b", "c", "d", "e", "f", "g", "h"]
NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8"]

# The lists of the odd LETTERS and numbers
ODD_LETTERS = ["a", "c", "e", "g"]
ODD_NUMBERS = ["1", "3", "5", "7"]

# The list of the order in which to write the pieces to the board
BOARD_ORDER = []

# The order in which to write the pieces to the board
for rank in ["8", "7", "6", "5", "4", "3", "2", "1"]:
    for file in ["a", "b", "c", "d", "e", "f", "g", "h"]:
        BOARD_ORDER.append(f"{file}{rank}")

# The colors
BLACK = "#222222"
WHITE = "#ffffff"

# The images
IMAGE_EMPTY = f"{ROOT_PATH}icons/pieces/base.png"
IMAGE_K = f"{ROOT_PATH}icons/pieces/king_w.png"
IMAGE_k = f"{ROOT_PATH}icons/pieces/king_b.png"
IMAGE_KING_W_LARGE = f"{ROOT_PATH}icons/pieces/king_w_large.png"
IMAGE_KING_B_LARGE = f"{ROOT_PATH}icons/pieces/king_b_large.png"
IMAGE_Q = f"{ROOT_PATH}icons/pieces/queen_w.png"
IMAGE_q = f"{ROOT_PATH}icons/pieces/queen_b.png"
IMAGE_B = f"{ROOT_PATH}icons/pieces/bishop_w.png"
IMAGE_b = f"{ROOT_PATH}icons/pieces/bishop_b.png"
IMAGE_N = f"{ROOT_PATH}icons/pieces/knight_w.png"
IMAGE_n = f"{ROOT_PATH}icons/pieces/knight_b.png"
IMAGE_R = f"{ROOT_PATH}icons/pieces/rook_w.png"
IMAGE_r = f"{ROOT_PATH}icons/pieces/rook_b.png"
IMAGE_P = f"{ROOT_PATH}icons/pieces/pawn_w.png"
IMAGE_p = f"{ROOT_PATH}icons/pieces/pawn_b.png"

IMAGE_APPLICATION = f"{ROOT_PATH}icons/application/appicon.png"
IMAGE_ERROR = f"{ROOT_PATH}icons/application/error.png"
IMAGE_INFO = f"{ROOT_PATH}icons/application/info.png"
IMAGE_QUESTION = f"{ROOT_PATH}icons/application/question.png"
IMAGE_SEARCH = f"{ROOT_PATH}icons/application/search.png"
IMAGE_WARNING = f"{ROOT_PATH}icons/application/warning.png"

# The audio file
AUDIO_FILE_1 = f"{ROOT_PATH}audio/move1.wav"
AUDIO_FILE_2 = f"{ROOT_PATH}audio/move2.wav"