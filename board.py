# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import random

class Board:
    def __init__(self, width, height, num_mines):
        self.width = width
        self.height = height
        self.num_mines = num_mines

        self.num_revealed = 0
        self.num_to_win = width * height - num_mines
        self.won = False
        self.finished = False

        self.grid = [[' ' for x in range(width)] for y in range(height)]
        self.revealed = [[False for x in range(width)] for y in range(height)]

        self._populate_mines()

    def _populate_mines(self):
        num_spaces = self.width * self.height
        for pos in random.sample(range(num_spaces), self.num_mines):
            self.grid[pos // self.height][pos % self.width] = '*'

    def __str__(self):
        board_display = []
        letter_code = ord('A')
        board_display.append('     ')
        for x in range(self.width):
            board_display.append(chr(letter_code))
            letter_code += 1
        board_display.append('\n')

        for y in range(self.height):
            board_display.append("{:>3} ".format(y + 1))
            for x in range(self.width):
                if self.finished and self.grid[y][x] == '*':
                    if self.revealed[y][x] is True:
                        board_display.append('X')
                    else:
                        board_display.append(self.grid[y][x])
                else:
                    if self.revealed[y][x] is True:
                        num_adjacent_mines = self._get_num_adjacent_mines(x, y)
                        if num_adjacent_mines == 0:
                            board_display.append(' ')
                        else:
                            board_display.append(str(num_adjacent_mines))
                    elif self.revealed[y][x] == '!':
                        board_display.append('!')
                    else:
                        board_display.append('?')
            board_display.append('\n')

        return " ".join(board_display)

    def _has_adjacent_revealed(self, x, y):
        squares_to_check = self._collect_adjacents(self.revealed, x, y)

        for (square, x, y) in squares_to_check:
            if square is True:
                return True

        return False

    def _get_num_adjacent_mines(self, x, y):
        squares_to_check = self._collect_adjacents(self.grid, x, y)
        num_adjacent_mines = 0

        for (square, x, y) in squares_to_check:
            if square == '*':
                num_adjacent_mines += 1

        return num_adjacent_mines

    def _collect_adjacents(self, grid, x, y):
        squares_to_check = []
        if x > 0:
            if y > 0:
                squares_to_check.append((grid[y - 1][x - 1], x - 1, y -1))
            squares_to_check.append((grid[y][x - 1], x - 1, y))
            if y < self.height - 1:
                squares_to_check.append((grid[y + 1][x - 1], x - 1, y + 1))
        if y > 0:
            squares_to_check.append((grid[y - 1][x], x, y - 1))
        if y < self.height - 1:
            squares_to_check.append((grid[y + 1][x], x, y + 1))
        if x < self.width - 1:
            if y > 0:
                squares_to_check.append((grid[y - 1][x + 1], x + 1, y - 1))
            squares_to_check.append((grid[y][x + 1], x + 1, y))
            if y < self.height - 1:
                squares_to_check.append((grid[y + 1][x + 1], x + 1, y + 1))
        return squares_to_check

    def flag_square(self, x, y):
        if self.revealed[y][x] is True:
            return

        if self.revealed[y][x] == '!':
            self.revealed[y][x] = False
        else:
            self.revealed[y][x] = '!'

    def uncover_square(self, x, y):
        if self.revealed[y][x] is True:
            return False

        if self.grid[y][x] == '*':
            # boom!
            self.revealed[y][x] = True
            self.finished = True
            return True
        else:
            self.revealed[y][x] = True
            self.num_revealed += 1

            # flood uncover
            num_adjacent_mines = self._get_num_adjacent_mines(x, y)
            if num_adjacent_mines == 0:
                adjacents = self._collect_adjacents(self.revealed, x, y)
                for (square, adj_x, adj_y) in adjacents:
                    self.uncover_square(adj_x, adj_y)

            if self.check_is_won():
                self.won = True
                self.finished = True
                return True
            return False

    def check_is_won(self):
        return self.num_revealed >= self.num_to_win
