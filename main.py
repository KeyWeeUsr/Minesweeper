# -*- coding: utf-8 -*-
# Minesweeper
# Version: 0.2.0
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
import os


class Minesweeper(object):
    first = True
    mine = u'¤'
    found_mine = '*'
    padding = 2
    count_mines = 10
    board_x = 20
    board_y = 5
    mines = []
    numbers = []
    _board = []
    logo = '''
  _____ _
 |     |_|___ ___ ___ _ _ _ ___ ___ ___ ___ ___
 | | | | |   | -_|_ -| | | | -_| -_| . | -_|  _|
 |_|_|_|_|_|_|___|___|_____|___|___|  _|___|_|
                                   |_|
                                       by KeyWeeUsr
'''

    def __init__(self, **kwargs):
        super(Minesweeper, self).__init__(**kwargs)
        self.clean()
        if self.first:
            self._board.append('-'+'-'*self.board_x*2)
            for i in range(self.board_y):
                self._board.append('|'+'x'*self.board_x)
            self._board.append('-'+'-'*self.board_x*2)
            self.board = self._board[:]
            self.start()
        self.print_board()
        while True:
            self.check()

    def clean(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.logo)

    def reset(self):
        pass

    def print_board(self, x=None, y=None, end=False, found=False):
        if not x and not y:
            for _row in self.board:
                row = []
                for r in _row:
                    if r != '|' and r != '-':
                        row.append(r+'|')
                    else:
                        row.append(r)
                print(' '*self.padding + ''.join(row))
        else:
            if not end:
                self.board[y] = list(self.board[y])
                self.board[y][x] = str(self.numbers[y-1][x-1][2])
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
                        row.append(r+'|')
                    else:
                        row.append(r)
                print(' '*self.padding + ''.join(row))
            if end and not found:
                print('Game Over')
                if raw_input('Play again? y/n') != 'y':
                    exit()
                else:
                    # reset here
                    pass
                return

    def start(self):
        while len(self.mines) < self.count_mines:
            x = randint(1, self.board_x)
            y = randint(1, self.board_y)
            if [x, y] not in self.mines:
                self.mines.append([x, y])
        self.first = False
        self.nums()

    def nums(self):
        for i in range(1, self.board_y+1):
            for j in range(1, self.board_x+1):
                m = 0
                if [j-1, i] in self.mines:
                    m += 1
                if [j-1, i-1] in self.mines:
                    m += 1
                if [j, i-1] in self.mines:
                    m += 1
                if [j+1, i-1] in self.mines:
                    m += 1
                if [j+1, i] in self.mines:
                    m += 1
                if [j+1, i+1] in self.mines:
                    m += 1
                if [j, i+1] in self.mines:
                    m += 1
                if [j-1, i+1] in self.mines:
                    m += 1
                self.numbers.append([j, i, m])
        _numbers = []
        for x in xrange(0, len(self.numbers), self.board_x):
            _numbers.append(self.numbers[x:x+self.board_x])
        self.numbers = _numbers[:]

    def check(self):
        x, y = None, None
        found = False
        while not x and not y:
            x = raw_input('x >>> ')
            y = raw_input('y >>> ')
            try:
                x = int(x)
                y = int(y)
            except ValueError:
                try:
                    if x[-1:] == self.found_mine and y[-1:] == self.found_mine:
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
            print('Only positive numbers!')
            return
        self.clean()
        self.reveal(x, y, found)

    def reveal(self, x, y, found):
        zeros = [[x, y]]

        # where to look
        # corners
        if x == 1 and y == 1:
            zeros.extend([[x, y+1], [x+1, y+1], [x+1, y]])
        elif x == self.board_x and y == self.board_y:
            zeros.extend([[x, y-1], [x-1, y-1], [x-1, y]])

        # edges
        elif x == 1 and y > 1 and y < self.board_y:
            zeros.extend([[x, y+1], [x+1, y+1], [x+1, y],
                          [x+1, y-1], [x, y-1]])

        elif y == 1 and x > 1 and x < self.board_x:
            zeros.extend([[x, y+1], [x+1, y+1], [x+1, y],
                          [x-1, y], [x-1, y+1]])

        # core
        elif x > 1 and x < self.board_x and y > 1 and y < self.board_y:
            zeros.extend([[x, y+1], [x+1, y+1], [x+1, y], [x+1, y-1],
                          [x, y-1], [x-1, y-1], [x-1, y], [x-1, y-1]])

        for z in zeros:
            try:
                if (self.numbers[z[1]-1][z[0]-1][2] == 0 and
                        self.numbers[z[1]-1][z[0]-1] not in self.mines):
                    self.clean()
                    self.print_board(z[0], z[1],
                                     [z[0], z[1]] in self.mines, found)
                else:
                    self.clean()
                    self.print_board(x, y, [x, y] in self.mines, found)
                    return
            except IndexError:
                self.print_board()
                print('Out of bounds!')

if __name__ == "__main__":
    Minesweeper()
# difficulty = # of mines in x*y space
# beginner = 10 in 9x9
# intermediate = 40 in 16x16
# expert = 99 in 30x16
