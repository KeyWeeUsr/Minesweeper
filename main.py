# -*- coding: utf-8 -*-
# Minesweeper
# Version: 0.1.0
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

from random import randint


class Mine(object):
    first = True
    mine = u'¤'
    count_mines = 10
    board_x = 20
    board_y = 5
    mines = []
    numbers = []
    _board = ['---------------------------------------',
              '|xxxxxxxxxxxxxxxxxxx',
              '|xxxxxxxxxxxxxxxxxxx',
              '|xxxxxxxxxxxxxxxxxxx',
              '|xxxxxxxxxxxxxxxxxxx',
              '|xxxxxxxxxxxxxxxxxxx',
              '---------------------------------------']
    board = _board[:]

    def __init__(self, **kwargs):
        super(Mine, self).__init__(**kwargs)
        if self.first:
            self.start()
        self.print_board()
        while True:
            self.check()

    def print_board(self, x=None, y=None, end=False):
        if not x and not y:
            for _row in self.board:
                row = []
                for r in _row:
                    if r != '|' and r != '-':
                        row.append(r+'|')
                    else:
                        row.append(r)
                print ''.join(row)
        else:
            if not end:
                _x = x-1
                _y = y-1
                pos = (_x) * _y + _x
                print 'num length', len(self.numbers)
                print self.numbers[pos]
                print self.numbers[pos][2]
            else:
                self.board[y][x] = self.mine
            for _row in self.board:
                row = []
                for r in _row:
                    if r != '|' and r != '-':
                        row.append(r+'|')
                    else:
                        row.append(r)
                print ''.join(row)
            if end:
                print 'Game Over'
                if raw_input('Play again? y/n') != 'y':
                    exit()
                else:
                    #reset here
                    pass

    def start(self):
        while len(self.mines) < self.count_mines:
            x = randint(1, self.board_x+1)
            y = randint(1, self.board_y+1)
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
        x = input('x >>> ')
        y = input('y >>> ')
        if x < 0 or y < 0:
            print 'Only positive numbers!'
            return
        print self.mines
        print self.numbers
        #print 'Gotcha!' if [x, y] in self.mines else 'Try again!'
        try:
            self.print_board(x, y, [x, y] in self.mines)
        except IndexError:
            print 'Out of bounds!'
        # show area - for loop, check near mine
        #     if 0 reveal
        #     if 0 in near, reveal too

if __name__ == "__main__":
    Mine()
# difficulty = #mines in x*y space
# beginner = 10 in 9x9
# intermediate = 40 in 16x16
# expert = 99 in 30x16
