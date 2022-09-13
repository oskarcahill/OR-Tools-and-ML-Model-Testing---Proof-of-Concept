from ortools.sat.python import cp_model
import numpy
import random


def display_sudoku(sudoku):
    (i, j) = (0, 0)
    for i in range(9):
        for j in range(9):
            print(sudoku[i, j], end=" ")
        print("")


# Allow to put initial constraint of the Sudoku
def initialize_sudoku(model_or_tool, sudoku_init, sudoku_to_do):
    for i in range(9):
        for j in range(9):
            if sudoku_to_do[i][j] != 0:  # If case of sudoku is filled
                sudoku_init[i][j] = model_or_tool.NewIntVar(int(sudoku_to_do[i][j]), int(sudoku_to_do[i][j]),
                                                            'column: %i' % i)
    return sudoku_init


def sudoku_solver(sudoku):
    model = cp_model.CpModel()
    solution = numpy.full((9,9), 0, dtype=float)
    sudoku2 = [[model.NewIntVar(1, 9, 'column: %i' % i) for i in range(9)] for j in range(9)]
    sudoku = initialize_sudoku(model, sudoku2, sudoku)

    # Constraint in line
    for i in range(9):
        line = []
        for j in range(9):
            line.append(sudoku[i][j])
        model.AddAllDifferent(line)

    # Constraint in column
    for i in range(9):
        column = []
        for j in range(9):
            column.append(sudoku[j][i])
        model.AddAllDifferent(column)

    # Constraint in sector
    for index in range(9):
        sector = []
        for i in [(index // 3) * 3, (index // 3) * 3 + 1, (index // 3) * 3 + 2]:
            for j in [(index % 3) * 3, (index % 3) * 3 + 1, (index % 3) * 3 + 2]:
                sector.append(sudoku[i][j])
                model.AddAllDifferent(sector)

    # Initialize the solver
    solver = cp_model.CpSolver()

    # Solving
    status = solver.Solve(model)
    
    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
        for i in range(9):
            for j in range(9):
                solution[i,j]=solver.Value(sudoku[i][j])
        return solution
    return numpy.full((9,9), -1, dtype=float)



