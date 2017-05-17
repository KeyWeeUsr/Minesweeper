# -*- coding: utf-8 -*-
# Minesweeper
# Version: 0.4.0
# Copyright (C) 2016, KeyWeeUsr(Peter Badida) <keyweeusr@gmail.com>
# License: GNU GPL v3.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# More info in LICENSE.txt
#
# The above copyright notice, warning and additional info together with
# LICENSE.txt file shall be included in all copies or substantial portions
# of the Software.

from __future__ import print_function
from random import randint
import sys
import os

if sys.version_info[0] > 2:
    raw_input = input
    xrange = range


class Minesweeper(object):
    logo = '''
  _____ _
 |     |_|___ ___ ___ _ _ _ ___ ___ ___ ___ ___
 | | | | |   | -_|_ -| | | | -_| -_| . | -_|  _|
 |_|_|_|_|_|_|___|___|_____|___|___|  _|___|_|
                                   |_|
                                       by KeyWeeUsr\n'''

    def __init__(self, **kwargs):
        super(Minesweeper, self).__init__(**kwargs)

        # set initial values
        self.mines = []
        self.mine = u'¤'
        self.cover = 'x'
        self.empty = ' '
        self.spacing = 1
        self.padding = 2
        self.board_y = 5
        self._board = []
        self.numbers = []
        self.board_x = 20
        self.found_mine = '*'
        self.count_mines = 10

        # X, Y, mines count
        self.difficulty = [
            [9, 9, 10],
            [16, 16, 40],
            [32, 16, 99]
        ]

        # set padding & spacing
        self.pad = self.empty * self.padding
        self.spa = self.empty * self.spacing

        # set menu layout
        self.main_menu = [
            '(1) Play Game',
            '(2) Instructions',
            '(3) Options',
            '(4) About',
            '(5) Exit Game'
        ]

        self.menu_values = [
            ['(1) Beginner',
             '(2) Intermediate',
             '(3) Expert',
             '(4) Custom'],
            [('1) Select a place in the minefield by typing '
              'correct values of X and Y.'),
             ('2) Select a mine by typing asterisk(*) after '
              'both X and Y coordinates\n' + self.pad +
              '-> e.g. 1* 1*'),
             ('3) Exit game either with Ctrl+C or '
              'Ctrl+Pause/Break combination.')],
            ['Options are set for a single game only:',
             '(1) Mine character (default: ' + self.mine + ')',
             '(2) Found mine character (default: ' +
             self.found_mine + ')',
             '(3) Empty place character - zero mines around ' +
             '(default: "' + self.empty + '")',
             '(4) Padding - from left (default: ' +
             str(self.padding) + ')',
             '(5) Spacing - between places in minefield ' +
             '(default: ' + str(self.spacing) + ')'],
            [('This Minesweeper is inspired by the old Win95 '
              'game I used to play long ago.'),
             ('Even now I play some clone on android once in '
              'a while, so...'),
             ('I decided to make a text version controlled '
              'by a keyboard.'),
             (' ' * 50 + 'Have fun!')],
            '']

        self.clean()
        self.menu()
        self.set_board()
        while True:
            self.check()

    def clean(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.logo)

    def menu(self):
        for m in self.main_menu:
            print(self.pad + m)

        try:
            select = int(raw_input('\n' + self.pad + '>>> '))
            self.clean()

            for v in self.menu_values[select - 1]:
                print(self.pad + v)

            if select == 1:
                value = int(raw_input('\n' + self.pad + '>>> '))
                if value != 4:
                    self.board_x = self.difficulty[value - 1][0]
                    self.board_y = self.difficulty[value - 1][1]
                    self.count_mines = self.difficulty[value - 1][2]
                else:
                    x = int(raw_input(self.pad + 'width >>> '))
                    y = int(raw_input(self.pad + 'height >>> '))
                    m = int(raw_input(self.pad + '# of mines >>> '))
                    if x == 1 and y == 1 or m < 1 or x < 1 or y < 1:
                        raise
                    self.board_x = x
                    self.board_y = y
                    self.count_mines = m

            elif select == 2:
                raw_input()
                self.clean()
                self.menu()

            elif select == 3:
                option = int(raw_input('\n' + self.pad + '>>> '))
                value = raw_input('\n' + self.pad + '>>> ')
                if option == 1:
                    self.mine = value
                elif option == 2:
                    self.found_mine = value
                elif option == 3:
                    self.empty = value
                elif option == 4:
                    self.padding = int(value)
                elif option == 5:
                    self.spacing = int(value)
                raw_input()
                self.clean()
                self.menu()

            elif select == 4:
                raw_input()
                self.clean()
                self.menu()

            elif select == 5:
                exit()
            self.clean()

        except Exception:
            self.clean()
            self.menu()

    def set_board(self):
        self._board.append('-' + '-' * self.board_x * 2)

        for i in xrange(self.board_y):
            self._board.append('|' + self.cover * self.board_x)

        self._board.append('-' + '-' * self.board_x * 2)
        self.board = self._board[:]
        self.start()
        self.print_board()

    def start(self):
        while len(self.mines) < self.count_mines:
            x = randint(1, self.board_x)
            y = randint(1, self.board_y)
            if [x, y] not in self.mines:
                self.mines.append([x, y])
        self.nums()

    def nums(self):
        for i in xrange(1, self.board_y + 1):
            for j in xrange(1, self.board_x + 1):
                m = 0
                if [j - 1, i] in self.mines:
                    m += 1
                if [j - 1, i - 1] in self.mines:
                    m += 1
                if [j, i - 1] in self.mines:
                    m += 1
                if [j + 1, i - 1] in self.mines:
                    m += 1
                if [j + 1, i] in self.mines:
                    m += 1
                if [j + 1, i + 1] in self.mines:
                    m += 1
                if [j, i + 1] in self.mines:
                    m += 1
                if [j - 1, i + 1] in self.mines:
                    m += 1
                self.numbers.append([j, i, m])  # oh, hi Jim!

        _numbers = []
        for x in xrange(0, len(self.numbers), self.board_x):
            _numbers.append(self.numbers[x:x + self.board_x])
        self.numbers = _numbers[:]

    def print_board(self, x=None, y=None, end=False, found=False):
        # cache
        pad = self.pad
        spa = self.spa

        print(pad + 'v Y / X ->')
        if not x and not y:
            for _row in self.board:
                row = []
                for r in _row:
                    if r != '|' and r != '-':
                        row.append(r + spa + '|' + spa)
                    else:
                        row.append(r + spa)
                print(pad + ''.join(row))
        else:
            if not end:
                self.board[y] = list(self.board[y])
                self.board[y][x] = str(self.numbers[y - 1][x - 1][2])
                self.board[y] = ''.join(self.board[y])
            else:
                self.board[y] = list(self.board[y])
                if found:
                    self.board[y][x] = self.found_mine
                else:
                    self.board[y][x] = self.mine
                self.board[y] = ''.join(self.board[y])
            for _row in self.board:
                row = []
                for r in _row:
                    if r != '|' and r != '-':
                        row.append(r + spa + '|' + spa)
                    else:
                        row.append(r + spa)

                print(pad + ''.join(row).replace('0', self.empty))
            if end and not found:
                print(self.pad + 'Game Over')
                if raw_input(self.pad + 'Play again? y/n') != 'y':
                    exit()
                else:
                    self.reset()
                return

    def check(self):
        x, y = None, None
        found = False
        while not x and not y:
            try:
                x = raw_input(self.pad + 'x >>> ')
                y = raw_input(self.pad + 'y >>> ')
            except EOFError:
                continue

            try:
                x = int(x)
                y = int(y)
            except ValueError:

                try:
                    if x[-1:] == y[-1:] == self.found_mine:
                        x = int(x[:-1])
                        y = int(y[:-1])
                        found = True
                    else:
                        # if input is e.g. 1a, 2
                        x, y = 0, 0
                except TypeError:
                    x, y = 0, 0

            except TypeError:
                # if input is strange e.g. 2*2
                x, y = 0, 0

        if x <= 0 or y <= 0:
            print(self.pad + 'Only positive numbers!')
            return

        self.clean()
        self.reveal(x, y, found)
        self.check_end()

    def reveal(self, x, y, found):
        zeros = [[x, y]]
        num = self.numbers

        # where to look
        # corners
        if x == 1 and y == 1:
            zeros.extend([[x, y + 1], [x + 1, y + 1], [x + 1, y]])
        elif x == self.board_x and y == self.board_y:
            zeros.extend([[x, y - 1], [x - 1, y - 1], [x - 1, y]])
        elif x == 1 and y == self.board_y:
            zeros.extend([[x + 1, y], [x + 1, y - 1], [x, y - 1]])
        elif y == 1 and x == self.board_x:
            zeros.extend([[x, y + 1], [x - 1, y], [x - 1, y + 1]])

        # edges
        elif x == 1 and y > 1 and y < self.board_y:
            zeros.extend([[x, y + 1], [x + 1, y + 1], [x + 1, y],
                          [x + 1, y - 1], [x, y - 1]])

        elif y == 1 and x > 1 and x < self.board_x:
            zeros.extend([[x, y + 1], [x + 1, y + 1], [x + 1, y],
                          [x - 1, y], [x - 1, y + 1]])

        elif x == self.board_x and y > 1 and y < self.board_y:
            zeros.extend([[x, y + 1], [x, y - 1], [x - 1, y],
                          [x - 1, y - 1], [x - 1, y + 1]])

        elif y == self.board_y and x > 1 and x < self.board_x:
            zeros.extend([[x + 1, y], [x + 1, y - 1], [x, y - 1],
                          [x - 1, y], [x - 1, y - 1]])

        # middle
        elif x > 1 and x < self.board_x and y > 1 and y < self.board_y:
            zeros.extend([[x + 1, y + 1], [x, y + 1], [x + 1, y],
                          [x + 1, y - 1], [x, y - 1], [x - 1, y],
                          [x - 1, y + 1], [x - 1, y - 1]])

        for z in zeros:
            try:
                if (num[z[1] - 1][z[0] - 1][2] == 0 and
                        num[z[1] - 1][z[0] - 1] not in self.mines):
                    self.clean()
                    self.print_board(
                        z[0], z[1],
                        [z[0], z[1]] in self.mines,
                        found
                    )
                else:
                    self.clean()
                    self.print_board(
                        x, y,
                        [x, y] in self.mines,
                        found
                    )
                    return

            except IndexError:
                self.print_board()
                print(self.pad + 'Out of bounds!')

    def check_end(self):
        revealed = 0
        remaining = 0
        for row in self.board:
            remaining += row.count(self.cover)
            revealed += row.count(self.found_mine)

        if len(self.mines) in (revealed, remaining):
            print(self.pad + 'Congrats!')
            raw_input()
            self.reset()

    def reset(self):
        self.__init__()


if __name__ == "__main__":
    Minesweeper()
