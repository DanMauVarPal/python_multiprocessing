"""
=================================================================================================
Title           : Daniel_Vargas_R11998328_final_project.py
Description     : Serial Cell Life Simulator.
Author          : var28790 (R#11998328)
Date            : 05/01/2026
Version         : 2.3
Usage           : python3 example.py -i input_file_path -o output_file_path -p processes_number
Python Version  : 3.13
=================================================================================================
"""

import argparse
import copy
import os
import sys
from multiprocessing import Pool

# Constants and Sets
POWERS_OF_TWO = {1, 2, 4, 8, 16, 32, 64}
FIBONACCI_SET = {0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89}
PRIME_NUMBERS = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89}

# 1.3.1 Symbols
# 1.3.2.2 Value assigned based on state
CELL_TO_VALUE = {"O": 3, "o": 1, ".": 0, "x": -1, "X": -3}
VALUE_TO_CELL = {3: "O", 1: "o", 0: ".", -1: "x", -3: "X"}

# Global look-up table
STAGE_UPDATE = {3: {}, 1: {}, 0: {}, -1: {}, -3: {}}


# Create Rules Dictionary
def rule_creation():
    for inner_score in range(-24, 25):  # 8 cells with (-3 to 3) value each = (-24 to 24)
        for cell in STAGE_UPDATE:
            STAGE_UPDATE[cell][inner_score] = {}

        for outer_score in range(-48, 49):  # 16 cells with (-3 to 3) value each = (-48 to 48)
            # 1.3.2.3c influence_score
            influence_score = 2 * inner_score + outer_score

            # 1.3.2.4 cell is 'O'
            if influence_score in POWERS_OF_TWO:
                STAGE_UPDATE[3][inner_score][outer_score] = 0
            elif outer_score < 2:
                STAGE_UPDATE[3][inner_score][outer_score] = 1
            else:
                STAGE_UPDATE[3][inner_score][outer_score] = 3

            # 1.3.2.5 cell is 'o'
            if inner_score in FIBONACCI_SET:
                STAGE_UPDATE[1][inner_score][outer_score] = 3
            elif influence_score <= 0:
                STAGE_UPDATE[1][inner_score][outer_score] = 0
            else:
                STAGE_UPDATE[1][inner_score][outer_score] = 1

            # 1.3.2.6 cell is '.'
            if influence_score in PRIME_NUMBERS:
                STAGE_UPDATE[0][inner_score][outer_score] = 1
            elif influence_score < 0 and -influence_score in PRIME_NUMBERS:
                STAGE_UPDATE[0][inner_score][outer_score] = -1
            else:
                STAGE_UPDATE[0][inner_score][outer_score] = 0

            # 1.3.2.7 cell is 'x'
            if inner_score < 0 and -inner_score in FIBONACCI_SET:
                STAGE_UPDATE[-1][inner_score][outer_score] = -3
            elif influence_score >= 0:
                STAGE_UPDATE[-1][inner_score][outer_score] = 0
            else:
                STAGE_UPDATE[-1][inner_score][outer_score] = -1

            # 1.3.2.8 cell is 'X'
            if influence_score < 0 and -influence_score in POWERS_OF_TWO:
                STAGE_UPDATE[-3][inner_score][outer_score] = 0
            elif outer_score > -2:
                STAGE_UPDATE[-3][inner_score][outer_score] = -1
            else:
                STAGE_UPDATE[-3][inner_score][outer_score] = -3

# 1.3.2 Iterative Rules
rule_creation()


# Command Line Argument Parsing
def argument_parsing():
    # Parser declaration
    parser = argparse.ArgumentParser(description="Serial Cellular Life Simulator")

    # Arguments declaration
    parser.add_argument('-i', type=str, required=True, help="Path to the starting cellular matrix input file")
    parser.add_argument('-o', type=str, required=True, help="Path for store cellular simulation matrix output file")
    parser.add_argument('-p', type=int, default=1, help="Number of processes")

    # Parse arguments from command line
    args = parser.parse_args()

    # Check if the input argument is not a file, inaccessible or not found
    if not os.path.isfile(args.i):
        print(f"Error: input file {args.i} not found or inaccessible")
        sys.exit(1)

    # Check if the directory for the output file exists
    out_dir = os.path.dirname(args.o)  # Get the dir only for output
    if out_dir and not os.path.isdir(out_dir):
        print(f"Error: output directory {out_dir} not found or inaccessible")
        sys.exit(1)

    # Check if the processes argument is greater than or equal to 1
    if args.p < 1:
        print(f"Error: number of processes {args.p} is not 1 or greater")
        sys.exit(1)

    return args


# Read Matrix From File
def read_matrix(path):
    matrix = []
    with open(path) as file:
        # Get first line in file
        file_line = file.readline().strip()

        # Adding dead cells to the row start
        row = [0] * 2

        # Getting all cells in row from file
        for cell in file_line:
            if cell in CELL_TO_VALUE:
                row.append(CELL_TO_VALUE[cell])
            elif cell != "\n":
                print(f"Invalid cell type: '{cell}'")
                sys.exit(1)

        # Adding dead cells to the row end
        row.extend([0, 0])

        # Get constant length for all rows
        cols = len(row)

        # Adding the first row of the matrix
        matrix.append(row)

        # Get next lines in file
        for file_line in file:
            line = file_line.strip()

            # Check if rows are all equal length
            if len(line) != (cols - 4):
                print(f"Invalid row length: '{len(line)}'")

            row = [0] * 2

            for cell in file_line:
                if cell in CELL_TO_VALUE:
                    row.append(CELL_TO_VALUE[cell])
                elif cell != "\n":
                    print(f"Invalid cell type: '{cell}'")
                    sys.exit(1)

            row.extend([0, 0])

            # Adding rows with cells to matrix
            matrix.append(row)

        # Adding dead cells to the matrix
        matrix = [[0] * cols, [0] * cols] + matrix + [[0] * cols, [0] * cols]

        # Get constant height for matrix
        rows = len(matrix)

    return [matrix, cols, rows]


# Write Matrix At File
def write_matrix(matrix, rows, cols, path):
    with open(path, 'w') as file:
        for y in range(2, rows - 2):
            row = matrix[y]
            for x in range(2, cols - 2):
                # Changing number values to character representations
                file.write(VALUE_TO_CELL[row[x]])

            file.write('\n')


# Slice Matrix
def matrix_slicing(procs, rows):
    # Constant row allocation for all processes
    base_chunk = rows // procs
    # Remaining rows in case of imperfect division
    rem = rows % procs

    # Storing for matrix slices start and end indexes
    chunk_indexes = []
    start = 2

    for i in range(procs):
        size = base_chunk + (1 if i < rem else 0)
        end = start + size
        chunk_indexes.append((start, end))
        start = end

    return chunk_indexes


# Life Simulation
def chunk_simulation(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    # Matrix copy to work on
    sim_matrix = copy.deepcopy(matrix)

    # Matrix iteration
    for y in range(2, rows - 2):
        # 5 rows for the 5x5 score calculation
        lower_row = matrix[y - 2]
        low_row = matrix[y - 1]
        self_row = matrix[y]
        high_row = matrix[y + 1]
        higher_row = matrix[y + 2]

        # Row iteration
        for x in range(2, cols - 2):
            # x positions for rings
            x_left2 = x - 2
            x_left1 = x - 1
            x_right1 = x + 1
            x_right2 = x + 2

            # 1.3.2.1a Inner ring consisting of 8 adjacent cells
            inner_score = (
                # low_row
                    low_row[x_left1] + low_row[x] + low_row[x_right1] +
                    # self_row
                    self_row[x_left1] + self_row[x_right1] +
                    # high_row
                    high_row[x_left1] + high_row[x] + high_row[x_right1]
            )

            # 1.3.2.1b Outer ring consisting of remaining 16 cells within 5x5 region
            outer_score = (
                # lower_row
                    lower_row[x_left2] + lower_row[x_left1] + lower_row[x] + lower_row[x_right1] + lower_row[
                x_right2] +
                    # low_row
                    low_row[x_left2] + low_row[x_right2] +
                    # self_row
                    self_row[x_left2] + self_row[x_right2] +
                    # high_row
                    high_row[x_left2] + high_row[x_right2] +
                    # higher_row
                    higher_row[x_left2] + higher_row[x_left1] + higher_row[x] + higher_row[x_right1] + higher_row[
                        x_right2]
            )

            # Updating the cell based on the simulation rules
            sim_matrix[y][x] = STAGE_UPDATE[self_row[x]][inner_score][outer_score]

    return sim_matrix[2: rows - 2]


# Main driver function
def main():
    print("Project :: R11998328")

    # 1.1 Data Retrieval
    args = argument_parsing()

    # 1.2.1 Read Matrix
    matrix, cols, rows = read_matrix(args.i)
    # matrix, cols, rows = read_matrix("test_inputs/100x100_time_step_0.dat")

    # 2.1 Concurrency Using Multiprocessing
    # Slicing calculation
    proc = args.p
    # proc = 27

    chunk_indexes = matrix_slicing(proc, rows - 4)

    # 1.3 Matrix Processing
    with Pool(processes=proc) as pool:
        for _ in range(100):
            # Scatter the matrix
            chunks = []
            for start, end in chunk_indexes:
                chunks.append(matrix[start - 2: end + 2])

            # Start parallel processes
            res = pool.map(chunk_simulation, chunks)

            # Gather the updated rows
            matrix.clear()
            for chunk in res:
                matrix.extend(chunk)

            # Adding dead cells to the matrix
            matrix = [[0] * cols, [0] * cols] + matrix + [[0] * cols, [0] * cols]

    # 1.2.2 Write Matrix
    write_matrix(matrix, rows, cols, args.o)
    # write_matrix(matrix, rows, cols, "test_output.txt")


if __name__ == "__main__":
    main()
