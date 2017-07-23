from __future__ import print_function

import sys

if sys.version_info[0] <= 2:
    range = xrange
    input = raw_input

from board import Board

class Minesweeper:
    def __init__(self):
        MAX_WIDTH = 26
        MAX_HEIGHT = 99

        inputs = [
            {
                'key': 'width',
                'prompt': 'Enter board width (1 to ' + str(MAX_WIDTH) + '): ',
                'min_val': 1,
                'max_val': MAX_WIDTH
            },
            {
                'key': 'height',
                'prompt': 'Enter board height: (1 to ' + str(MAX_HEIGHT) + '): ',
                'min_val': 1,
                'max_val': MAX_HEIGHT
            },
            {
                'key': 'num_mines',
                'prompt': 'Enter number of mines: ',
                'max_val': 'area'
            }
        ]

        self.get_inputs(inputs)

        self.board = Board(self.width, self.height, self.num_mines)

    def get_inputs(self, inputs):
        for val_data in inputs:
            key = val_data['key']

            while True:
                try:
                    val = int(input(val_data['prompt']))
                    if 'max_val' in val_data:
                        if val_data['max_val'] == 'area':
                            area = self.width * self.height
                            if val > area:
                                raise ValueError('Over max')
                        elif val > val_data['max_val']:
                            raise ValueError('Over max')

                    if 'min_val' in val_data and val < val_data['min_val']:
                        raise ValueError('Under min')

                    setattr(self, key, val)
                    break
                except ValueError:
                    print("Not a valid value.  Try again.")

    def game_loop(self):
        while not self.board.finished:
            try:
                self.do_turn()
            except KeyboardInterrupt:
                print('\nCtrl-C detected, quitting.')
                return

        if self.board.won:
            print('You win!\n')
        else:
            print('Boom!  Game over.\n')

        print('Final board:\n')
        print(str(self.board))

    def do_turn(self):
        print(str(self.board))
        move_type = False
        valid_move_types = ['F', 'U']

        while move_type not in valid_move_types:
            move_type = str(input("(F)lag or (U)ncover a square? ")).upper()

        while True:
            try:
                x = str(input('Enter a column: ')).upper()
                if len(x) > 1:
                    raise ValueError('Invalid col')
                else:
                    x_int = ord(x) - ord('A')
                    if x_int < 0 or x_int >= self.width:
                        raise ValueError('Invalid col')
                    x = x_int
                    break
            except ValueError:
                print('Invalid column.  Try again.')

        while True:
            try:
                y = int(str(input('Enter a row: ')))
                if(y < 1 or y > self.height):
                    raise ValueError('Invalid row')
                y = y - 1
                break
            except ValueError:
                print('Invalid row.  Try again.')

        movers = {
            'F': self.board.flag_square,
            'U': self.board.uncover_square
        }

        movers[move_type](x, y)

if __name__ == '__main__':
    minesweeper = Minesweeper()
    minesweeper.game_loop()
