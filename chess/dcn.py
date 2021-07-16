# This file is part of the python-chess library.
# Copyright (C) 2012-2021 Niklas Fiekas <niklas.fiekas@backscattering.de>
# This file created by Samuel Matzko
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import chess
import io
import xml
import xml.etree.ElementTree as etree

class Game:
    """A game created from a board that stores all the headers and other data
    for the dcn file."""

    def __init__(self, board=None):
        self.moves = []
        self.board = chess.Board()
        self.game_element = etree.Element("game")
        self.tree = etree.ElementTree(self.game_element)
        self.headers = {
            "Event": "?",
            "Site": "?",
            "Date": "????.??.??",
            "Round": "?",
            "White": "?",
            "Black": "?",
            "Result": "*"
        }
        if board is not None:
            self.from_board(board)

    def _is_odd(self, number):
        number = str(number)
        digit = number[len(number) - 1]
        if digit == "1" or digit == "3" or digit == "5" or digit == "7" or digit == "9":
            return True
        else:
            return False

    def create_dcn(self):
        self.game_element = etree.Element("game")
        self.tree = etree.ElementTree(self.game_element)
        for header in self.headers:
            header_element = etree.Element("header", name=header)
            header_element.text = self.headers[header]
            self.game_element.append(header_element)
        self.board_element = etree.Element("board", fen=self.start_fen)
        self.game_element.append(self.board_element)

        self.stack_element = etree.Element("stack")
        self.game_element.append(self.stack_element)
        for move in self.board.move_stack:
            move_element = etree.Element("move")
            move_element.text = move.uci()
            self.stack_element.append(move_element)
        return self

    def from_board(self, board):
        self.moves = []
        self.board = board
        while self.board.move_stack != []:
            self.moves.append(self.board.pop())
        self.start_fen = self.board.fen()
        self.moves.reverse()
        for move in self.moves:
            self.board.push(move)
        if self.board is not None:
            if (self.board.turn and not self._is_odd(len(self.board.move_stack) - 1) or
                not self.board.turn and self._is_odd(len(self.board.move_stack) - 1)):
                self.board.move_stack.insert(0, chess.Move.from_uci("0000"))
            self.create_dcn()
        return self
    
    def from_file(self, file):
        self.tree = etree.ElementTree().parse(file)
        self.update_dcn()
        return self

    def from_string(self, string):
        self.from_file(io.StringIO(string))
        return self
    
    def set_headers(self, headers):
        self.headers = headers
        self.create_dcn()

    def update_dcn(self):
        """Updage the elements and all the other data variables from self.tree."""
        self.moves = []
        self.game_element = self.tree
        self.board_element = self.tree.find("board")
        self.stack_element = self.tree.find("stack")
        for move in self.stack_element.findall("move"):
            self.moves.append(chess.Move.from_uci(move.text))
        self.start_fen = self.board_element.get("fen")
        self.board = chess.Board(self.start_fen.split(" ")[0])
        for move in self.moves:
            self.board.push(move)
        for header in self.game_element.findall("header"):
            self.headers[header.get("name")] = header.text

    def write(self, file):
        """Write the game to a file."""
        self.tree.write(file)

if __name__ == "__main__":
    board = chess.Board()
    board.turn = False
    # board.push(chess.Move.from_uci("b1c3"))
    board.push(chess.Move.from_uci("d7d5"))
    board.push(chess.Move.from_uci("a2a3"))
    game = Game(board)
    game.write("/home/sam/text.dcn")
    print(str(game))
    print()
    game = Game()
    game.from_file("/home/sam/text.dcn")
    print(str(game))