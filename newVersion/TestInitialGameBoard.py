import unittest
from newVersion.GameBoard import GameBoard


gameBoard = GameBoard(10,10)

class InitialGameBoardTest(unittest.TestCase):

    def setUp(self) -> None:
        self.board = GameBoard(10,8) #10 rows, 8 columns
        self.board_2 = GameBoard(8,4,12,10)

    # test default constructor values
    def test_default_constructor(self):
        self.assertEqual(10, self.board.board_length)
        self.assertEqual(8,self.board.board_height)
        self.assertEqual(0, self.board.min_col)
        self.assertEqual(0, self.board.min_row)
        self.assertEqual(9, self.board.board_max_x_boundary) # column boundary
        self.assertEqual(7, self.board.board_max_y_boundary) # row boundary

    # test valid values, non-default
    def test_valid_constructor_values(self):
        self.assertEqual(8, self.board_2.board_length)
        self.assertEqual(4, self.board_2.board_height)
        self.assertEqual(12, self.board_2.min_col)
        self.assertEqual(10, self.board_2.min_row)
        self.assertEqual(19, self.board_2.board_max_x_boundary)  # column boundary
        self.assertEqual(13, self.board_2.board_max_y_boundary)  # row boundary

    def test_initial_board_vals_equal_zero(self):
        all_zeroes_default = True
        hit = False
        board = self.board.board_array

        for eachRow in board:
            if hit == True:
                break
            for eachCol in eachRow:
                if eachCol > 0 or eachCol < 0:
                    all_zeroes_default = False
                    hit = True
                    break

        all_zeroes_non_default = True
        hit_2 = False
        board_2 = self.board_2.board_array

        for eachRow in board_2:
            if hit_2 == True:
                break
            for eachCol in eachRow:
                if eachCol > 0 or eachCol < 0:
                    all_zeroes_non_default = False
                    hit_2 = True
                    break

        self.assertEqual(True, all_zeroes_default)
        self.assertEqual(True,all_zeroes_non_default)

    def testRaiseValueError(self):
        '''
        Testing if invalid inputs passed into constructor
        :return: void
        '''
        error_counter = 0

        try:
            GameBoard(0,1) # edge case: board length = 0
        except ValueError:
            error_counter += 1

        try:
            GameBoard(1,0) # edge case: board height = 0
        except ValueError:
            error_counter += 1

        try:
            GameBoard(-1,2) # board length < 0
        except ValueError:
            error_counter += 1

        try:
            GameBoard(2,-1) # board height < 0
        except ValueError:
            error_counter += 1

        self.assertEqual(4, error_counter)

def main():
    unittest.main(verbosity=3)

if __name__ == '__main__':
    main()