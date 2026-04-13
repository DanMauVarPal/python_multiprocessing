import argparse
import sys

CELL_TYPES = {'O', 'X', 'o', 'x', '.', '\n'}
POWERS_OF_TWO = {1, 2, 4, 8, 16, 32, 64, 128}
FIBONACCI_SET = {0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144}
PRIME_NUMBERS = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97}


def main():
    print("Project :: R11998328")

    # 1. Data Retrieval
    # parser = argparse.ArgumentParser(description="Serial Cellular Life Simulator")
    # parser.add_argument('-i', type=str, required=True, help="Path to the starting cellular matrix")
    # parser.add_argument('-o', type=str, required=True, help="Path for the final output file")
    # parser.add_argument('-p', type=int, default=1, help="Number of processes to spawn (Ignored in Phase 1)")
    #
    # args = parser.parse_args()

    # 2. Read Matrix
    matrix = []
    # with open(args.i) as file:
    with open("ten_by_ten/time_step_0.dat") as file:
        # Get first line in file
        file_line = file.readline().strip()
        row = []
        for cell in file_line:
            if cell not in CELL_TYPES:
                print(f"Invalid cell type: '{cell}'")
                sys.exit(1)
            elif cell == 'O':
                row.append(3)
            elif cell == 'o':
                row.append(1)
            elif cell == '.':
                row.append(0)
            elif cell == 'x':
                row.append(-1)
            elif cell == 'X':
                row.append(-3)

        matrix.append(row)

        # Get constant length for all rows
        cols = len(row)

        # Get next lines in file
        for file_line in file:
            line = file_line.strip()
            if not line:
                break

            row = []

            if len(line) != cols:
                print(f"Invalid row length: '{len(line)}'")

            for cell in file_line:
                if cell not in CELL_TYPES:
                    print(f"Invalid cell type: '{cell}'")
                    sys.exit(1)
                elif cell == 'O':
                    row.append(3)
                elif cell == 'o':
                    row.append(1)
                elif cell == '.':
                    row.append(0)
                elif cell == 'x':
                    row.append(-1)
                elif cell == 'X':
                    row.append(-3)

            matrix.append(row)

        rows = len(matrix)

    # 3. Matrix Processing
    # time_steps
    for _ in range(30):
        sim_matrix = []
        # matrix iteration
        for y in range(rows):
            row = []
            for x in range(cols):
                # ring scores
                inner_score, outer_score = 0, 0

                # 5x5 matrix around current cell
                for y_score in range(-2, 3):
                    for x_score in range(-2, 3):
                        # skip current cell
                        if y_score == 0 and x_score == 0:
                            continue

                        y_actual, x_actual = y + y_score, x + x_score

                        # check inside-bound cells
                        if (0 <= y_actual < rows) and (0 <= x_actual < cols):
                            # inner circle values
                            if y_score in {-1, 0, 1} and x_score in {-1, 0, 1}:
                                inner_score += matrix[y_actual][x_actual]
                            # outer circle values
                            else:
                                outer_score += matrix[y_actual][x_actual]

                influence_score = 2 * inner_score + outer_score
                cell = matrix[y][x]

                # cell update rules
                # cell is 'O'
                if cell == 3:
                    if influence_score in POWERS_OF_TWO:
                        row.append(0)
                    elif outer_score < 2:
                        row.append(1)
                    else:
                        row.append(3)

                # cell is 'o'
                elif cell == 1:
                    if inner_score in FIBONACCI_SET:
                        row.append(3)
                    elif influence_score <= 0:
                        row.append(0)
                    else:
                        row.append(1)

                # cell is '.'
                elif cell == 0:
                    if influence_score in PRIME_NUMBERS:
                        row.append(1)
                    elif influence_score < 0 and -1 * influence_score in PRIME_NUMBERS:
                        row.append(-1)
                    else:
                        row.append(0)

                # cell is 'x'
                elif cell == -1:
                    if inner_score < 0 and -1 * inner_score in FIBONACCI_SET:
                        row.append(-3)
                    elif influence_score >= 0:
                        row.append(0)
                    else:
                        row.append(-1)

                # cell is 'X'
                elif cell == -3:
                    if influence_score < 0 and -1 * influence_score in POWERS_OF_TWO:
                        row.append(0)
                    elif outer_score > -2:
                        row.append(-1)
                    else:
                        row.append(-3)

            sim_matrix.append(row)

        matrix = sim_matrix

    # 4. Write Matrix
    with open("test_output.txt", 'w') as file:
        for row in matrix:
            for cell in row:
                if cell == 3:
                    file.write("O")
                elif cell == 1:
                    file.write("o")
                elif cell == 0:
                    file.write(".")
                elif cell == -1:
                    file.write("x")
                elif cell == -3:
                    file.write("X")

            file.write('\n')


if __name__ == "__main__":
    main()
