# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import argparse
import sys

CELL_TYPES = {'O', 'X', 'o', 'x', '.'}

def parse_args():
    parser = argparse.ArgumentParser(description="Serial Cellular Life Simulator")

    parser.add_argument('-i', type=str, required=True, help="Path to the starting cellular matrix input file.")
    parser.add_argument('-o', type=str, required=True, help="Path for the final output file.")
    parser.add_argument('-p', type=int, default=1, help="Number of processes to spawn (default: 1).")

    args = parser.parse_args()

    return args

def read_matrix(path):
    matrix = []
    with open(path) as file:
        row = file.readline().strip()

        for cell in row:
            if cell not in CELL_TYPES:
                print(f"Invalid cell type: '{cell}'")
                sys.exit(1)

        matrix.append(list(row))

        side = len(row)

        for line in file:
            row = line.strip()

            if len(row) != side:
                print(f"Invalid row length: '{len(row)}'")

            for cell in row:
                if cell not in CELL_TYPES:
                    print(f"Invalid cell type: '{cell}'")
                    sys.exit(1)

            matrix.append(list(row))


    return matrix

def write_matrix(matrix, path):
    with open(path, 'w') as file:
        for row in matrix:
            file.write("".join(row) + "\n")

def main():
    # args = parse_args()

    # matrix = read_matrix(arg.i)
    matrix = read_matrix("ten_by_ten/time_step_0.dat")

    # write_matrix(matrix, arg.o)
    write_matrix(matrix, "test_output.txt")

if __name__ == '__main__':
    main()
