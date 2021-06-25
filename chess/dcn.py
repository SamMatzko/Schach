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

class Game:
    """A game created from a board that stores all the headers and other data
    for the dcn file."""

    def __init__(self, board=None):
        self.moves = []
        self.board = chess.Board()
        self.supported_version = "1.0.0"
        self.dcn = ""
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

    def __str__(self):
        return self.dcn

    def _create_dcn(self):
        self.dcn = ''
        self.dcn += '<?dcn version="%s">\n<game>\n' % self.supported_version
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

    def _get_contents_of(self, tag):
        """Get the contents of TAG."""
        return tag[
            tag.find(">") + 1:tag.find("<", tag.find(">"))
        ]

    def _get_tag(self, tag, dcn):
        """Get the contents of TAG from string DCN."""
        return dcn[
            dcn.find(f"<{tag}"):dcn.find(f"</{tag}>") + len(f"</{tag}>")
        ]

    def _get_value_of(self, value_of, tag_contents):
        """Get the value of TAG_CONTENTS's attribute VALUE_OF."""
        return tag_contents[
            tag_contents.find(value_of) + len(value_of) + 2:tag_contents.find('"', tag_contents.find(value_of) + len(value_of) + 2)
        ]

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
        while self.board.move_stack != []:
            self.moves.append(self.board.pop())
        self.start_fen = self.board.fen()
        self.moves.reverse()
        for move in self.moves:
            self.board.push(move)
        self.dcn = ''
        if self.board is not None:
            if (self.board.turn and not self._is_odd(len(self.board.move_stack) - 1) or
                not self.board.turn and self._is_odd(len(self.board.move_stack) - 1)):
                self.board.move_stack.insert(0, chess.Move.from_uci("0000"))
                self._create_dcn()
        return self
    
    def from_file(self, file):
        with open(file) as f:
            self.dcn = f.read()
            f.close()
        self.from_string(self.dcn)
        return self

    def from_string(self, string):
        self.dcn = string
        dcn = self.dcn
        dcnlines = dcn.splitlines()
        if 'version="%s"' % self.supported_version in dcnlines[0]:
            pass
        else:
            raise TypeError("DCN version %s is not supported." % dcnlines[0].replace('<?dcn version="', "").replace('">', ""))

        dcn = self.dcn.replace("    ", "")
        dcn = dcn.replace("\n", "")

        # Get the headers        
        game = self._get_tag("game", dcn)
        while "<header>" in game:
            header = self._get_tag("header", game)
            game = game.replace(header, "")
            while "<attribute" in header:
                attribute = self._get_tag("attribute", header)
                if self._get_value_of("name", attribute) == "name":
                    header_name = self._get_contents_of(attribute)
                elif self._get_value_of("name", attribute) == "value":
                    header_value = self._get_contents_of(attribute)
                header = header.replace(attribute, "")
            self.headers[header_name] = header_value

        # Get the board
        while "<board>" in game:
            board = self._get_tag("board", game)
            game = game.replace(board, "")
            while "<attribute" in board:
                attribute = self._get_tag("attribute", board)
                if self._get_value_of("name", attribute) == "fen":
                    board_fen = self._get_contents_of(attribute).split(" ")
                board = board.replace(attribute, "")
            self.board.set_board_fen(board_fen[0])
            if board_fen[1] == "w":
                self.board.turn = True
            else:
                self.board.turn = False
        self.moves = self.board.move_stack
        
        # Get the moves
        stack = self._get_tag("stack", game)
        game = game.replace(stack, "")
        while "<move" in stack:
            move = self._get_tag("move", stack)
            moves = self._get_contents_of(move)
            moves = moves.split("...")
            for m in moves:
                if m != "":
                    self.board.push(chess.Move.from_uci(m))
            stack = stack.replace(move, "")
        return self

if __name__ == "__main__":
    board = chess.Board()
    board.push(chess.Move.from_uci("b1c3"))
    board.push(chess.Move.from_uci("d7d5"))
    board.push(chess.Move.from_uci("a2a3"))
    game = Game(board)
    print(str(game))
    print()
    game = Game()
    game.from_file("/home/sam/text.dcn")
    print(str(game))