from Sudoku import Sudoku
import sys

if __name__ == "__main__":
    test_sudoku = Sudoku()
    puzzle = "puzzle1.sud"

    test_sudoku.load(puzzle)
    print(test_sudoku)

    puzzle_name = puzzle[:-4]
    cnf_filename = puzzle_name + ".cnf"

    test_sudoku.generate_cnf(cnf_filename)
    print("Output file: " + cnf_filename)

