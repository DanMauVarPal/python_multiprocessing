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

        # Adding padding to the row start
        row = [0] * 2
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

        # Adding padding to the row end
        row.append(0)
        row.append(0)

        # Get constant length for all rows
        cols = len(row)

        # Adding upper padding to the matrix
        matrix.append([0] * cols)
        matrix.append([0] * cols)

        matrix.append(row)

        # Get next lines in file
        for file_line in file:
            line = file_line.strip()
            if not line:
                break

            row = [0] * 2

            if len(line) != (cols - 4):
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

            matrix.append(row + [0] * 2)

        # Adding lower padding to the matrix
        matrix.append([0] * cols)
        matrix.append([0] * cols)

        # Get constant height for matrix
        rows = len(matrix)

    # 3. Matrix Processing
    # time_steps
    for _ in range(1):
        sim_matrix = [[0] * cols for _ in range(rows)]
        # matrix iteration
        for y in range(2, rows - 2):
            lower_row = matrix[y - 2]
            low_row = matrix[y - 1]
            self_row = matrix[y]
            high_row = matrix[y + 1]
            higher_row = matrix[y + 2]

            for x in range(2, cols - 2):
                print(f"x: {x - 1} y: {y - 1}")
                print(f"matrix: {matrix}")
                # ring scores
                inner_score = (low_row[x - 1] + low_row[x] + low_row[x + 1] +
                               self_row[x - 1] + self_row[x + 1] +
                               high_row[x - 1] + high_row[x] + high_row[x + 1])

                outer_score = (
                        lower_row[x - 2] + lower_row[x - 1] + lower_row[x] + lower_row[x + 1] + lower_row[x + 2] +
                        low_row[x - 2] + low_row[x + 2] +
                        self_row[x - 2] + self_row[x + 2] +
                        high_row[x - 2] + high_row[x + 2] +
                        higher_row[x - 2] + higher_row[x - 1] + higher_row[x] + higher_row[x + 1] + higher_row[
                            x + 2])

                influence_score = 2 * inner_score + outer_score
                cell = self_row[x]
                print(f"cell: {cell}")
                print(f"inner_score: {inner_score}")
                print(f"outer_score: {outer_score}")
                print(f"influence_score: {influence_score}")

                # cell update rules
                # sim_matrix cell default values are always 0, so conditionals are optimized to not re-assign 0
                # cell is 'O'
                if cell == 3:
                    if influence_score not in POWERS_OF_TWO:
                        sim_matrix[y][x] = 1 if outer_score < 2 else 3

                # cell is 'o'
                elif cell == 1:
                    if inner_score in FIBONACCI_SET:
                        sim_matrix[y][x] = 3
                    elif influence_score > 0:
                        sim_matrix[y][x] = 1

                # cell is '.'
                elif cell == 0:
                    if influence_score in PRIME_NUMBERS:
                        sim_matrix[y][x] = 1
                    elif influence_score < 0 and -influence_score in PRIME_NUMBERS:
                        sim_matrix[y][x] = -1

                # cell is 'x'
                elif cell == -1:
                    if inner_score < 0 and -inner_score in FIBONACCI_SET:
                        sim_matrix[y][x] = -3
                    elif influence_score < 0:
                        sim_matrix[y][x] = -1

                # cell is 'X'
                elif cell == -3:
                    if influence_score < 0 and -1 * influence_score in POWERS_OF_TWO:
                        sim_matrix[y][x] = 0
                    elif outer_score > -2:
                        sim_matrix[y][x] = -1
                    else:
                        sim_matrix[y][x] = -3

                print(f"cell update: {sim_matrix[y][x]}")
                print(f"new matrix: {sim_matrix}\n")

        print(sim_matrix)
        matrix = sim_matrix

    # 4. Write Matrix
    print(matrix)
    with open("test_output.txt", 'w') as file:
        for y in range(2, rows - 2):
            for x in range(2, cols - 2):
                cell = matrix[y][x]
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
