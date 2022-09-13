import unittest
import operator
import numpy as np
import modules.app.sudoku_ortools as sor


sudokus = np.load("data/sudokus.npy")
solutions = np.load("data/sudoku_solutions.npy")

class TestSudoku(unittest.TestCase):
    def test_easy(self):
        r = range(0,5)
        for i in r:
            sudoku = sudokus[i].copy()
            sudoku_solved=sor.sudoku_solver(sudoku)
            np.testing.assert_array_equal(solutions[i], sudoku_solved)
            
    def test_medium(self):
        r = range(5,10)
        for i in r:
            sudoku = sudokus[i].copy()
            sudoku_solved=sor.sudoku_solver(sudoku)
            np.testing.assert_array_equal(solutions[i], sudoku_solved)
    def test_invalid(self):
        r=range(10,15)
        for i in r:
            sudoku = sudokus[i].copy()
            sudoku_solved=sor.sudoku_solver(sudoku)
            np.testing.assert_array_equal(solutions[i], sudoku_solved)

    def test_complex(self):
        r=range(15,20)
        for i in r:
            sudoku = sudokus[i].copy()
            sudoku_solved=sor.sudoku_solver(sudoku)
            np.testing.assert_array_equal(solutions[i], sudoku_solved)


if __name__ == '__main__':
    unittest.main()
