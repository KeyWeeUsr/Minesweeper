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
    mines = []
    numbers = []

    def __init__(self, **kwargs):
        super(Mine, self).__init__(**kwargs)
        if self.first:
            self.start()
        self.print_it()
        while True:
            self.check()

    def print_it(self):
        print '---------------------------------------'
        print '|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|'
        print '|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|'
        print '|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|'
        print '|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|'
        print '|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|'
        print '---------------------------------------'

    def start(self):
        for i in range(10):
            x = randint(1, 21)
            y = randint(1, 6)
            if [x, y] not in self.mines:
                self.mines.append([x, y])
        self.first = False
        self.nums()

    def nums(self):
        for i in range(1, 6):
            for j in range(1, 21):
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

    def check(self):
        x = input('x >>> ')
        y = input('y >>> ')
        print self.mines
        print self.numbers
        print 'Gotcha!' if [x, y] in self.mines else 'Try again!'
        # show area - for loop, check near mine
        #     if 0 reveal
        #     if 0 in near, reveal too

if __name__ == "__main__":
    Mine()
# difficulty = #mines in x*y space
# beginner = 10 in 9x9
# intermediate = 40 in 16x16
# expert = 99 in 30x16
