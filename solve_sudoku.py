### Ari Chadda
### 10/25/20 CS76 F20
### PA5

from display import display_sudoku_solution
import random, sys
from SAT import SAT

if __name__ == "__main__":
    random.seed(1)  # can specify a seed for pseudorandom number generator or not

    # To run, uncomment a puzzle, and an algorithm

    # puzzle choices
    # puzzle = "one_cell.cnf"
    # puzzle = "all_cells.cnf"
    # puzzle = "rows.cnf"
    # puzzle = "rows_and_cols.cnf"
    # puzzle = "puzzle1.sud"
    puzzle = "puzzle2.sud"

    sat = SAT(puzzle) # instantiating puzzle object

    # algorithm choices
    result = sat.walksat()
    # result = sat.gsat()

    # to generate solution file
    puzzle_name = str(puzzle[:-4])
    sol_filename = puzzle_name + ".sol"

    if result:
        sat.write_solution(sol_filename)
        display_sudoku_solution(sol_filename)