import numpy as np
import app.sudoku_ortools as sor
import appwithout.sud as swor


# Load sudokus
sudokus = np.load("data/sudokus.npy")
#print("Shape of one sudoku array:", sudokus[0].shape, ". Type of array values:", sudokus.dtype)

# Load solutions
solutions = np.load("data/sudoku_solutions.npy")

r=range(0,20)
for i in r:
	sudoku = sudokus[i].copy()
	print("This is sudoku number", i)
	print(sudoku)
	print("This is solution for s number", i)
	print(solutions[i])
	your_solution=swor.sudoku_solver(sudoku)
	print("This is your solution for sudoku number", i)
	print(your_solution)
	print("Is your solution correct?")
	print(np.array_equal(your_solution, solutions[i]))

for i in r:
	sudoku = sudokus[i].copy()
	print("This is sudoku number", i)
	print(sudoku)
	print("This is solution for s number", i)
	print(solutions[i])
	your_solution=sor.solveSudoku(sudoku)
	print("This is your solution for sudoku number", i)
	print(your_solution)
	print("Is your solution correct?")
	print(np.array_equal(your_solution, solutions[i]))
