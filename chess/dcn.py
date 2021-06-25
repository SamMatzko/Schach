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
import math

class Game:
    """A game created from a board that stores all the headers and other data
    for the dcn file."""

    def __init__(self, board=None):
        self.from_board(board)

    def __str__(self):
        return self.dcn

    def _create_dcn(self):
        self.dcn = ''
        self.dcn += '<game>\n'
        for header in self.headers:
            self.dcn += """    <header>
        <attribute name="name">%s</attribute>
        <attribute name="value">%s</attribute>
    </header>\n""" % (header, self.headers[header])

        self.dcn += """    <board>
        <attribute name="fen">%s</attribute>
    </board>\n""" % self.start_fen

        move_index = 1
        self.dcn += "    <moves>\n"
        for move in self.board.move_stack:
            if not self._is_odd(self.board.move_stack.index(move)):
                self.dcn += '        <move number="%s">%s...' % (move_index, move.uci())
            else:
                self.dcn += '%s</move>\n' % move.uci()
                move_index += 1
        if not self._is_odd(self.board.move_stack.index(move)):
            self.dcn +="</move>\n"
        self.dcn += "    </moves>\n"
    
        self.dcn += "</game>"

    def _is_odd(self, number):
        number = str(number)
        digit = number[len(number) - 1]
        if digit == "1" or digit == "3" or digit == "5" or digit == "7" or digit == "9":
            return True
        else:
            return False

    def from_board(self, board):
        self.moves = []
        self.board = board
        self.board = self.board
        while self.board.move_stack != []:
            self.moves.append(self.board.pop())
        self.start_fen = self.board.fen()
        self.moves.reverse()
        for move in self.moves:
            self.board.push(move)
        self.dcn = ''
        self.headers = {
            "Event": "?",
            "Site": "?",
            "Date": "????.??.??",
            "Round": "?",
            "White": "?",
            "Black": "?",
            "Result": "*"
        }
        self.supported_version = "1.0.0"
        if self.board is not None:
            self._create_dcn()

if __name__ == "__main__":
    board = chess.Board()
    board.push(chess.Move.from_uci("b1c3"))
    board.push(chess.Move.from_uci("d7d5"))
    board.push(chess.Move.from_uci("a2a3"))
    game = Game(board)
    print(str(game))