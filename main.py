import argparse
import sys

POWERS_OF_TWO = {1, 2, 4, 8, 16, 32, 64}
FIBONACCI_SET = {0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89}
PRIME_NUMBERS = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97}

CELLS = {
    'O': {"value": 3},
    'o': {"value": 1},
    ".": {"value": 0},
    "x": {"value": -1},
    "X": {"value": -3}
}


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
        row = ["."] * 2

        # Getting all cells in row from file
        for cell in file_line:
            if cell in CELLS:
                row.append(cell)
            elif cell != "\n":
                print(f"Invalid cell type: '{cell}'")
                sys.exit(1)

        # Adding padding to the row end
        row.append(".")
        row.append(".")

        # Get constant length for all rows
        cols = len(row)

        # Adding upper padding to the matrix
        matrix.append(["."] * cols)
        matrix.append(["."] * cols)

        # Adding the first row of the matrix
        matrix.append(row)

        # Get next lines in file
        for file_line in file:
            line = file_line.strip()
            if not line:
                break

            row = ["."] * 2

            if len(line) != (cols - 4):
                print(f"Invalid row length: '{len(line)}'")

            for cell in file_line:
                if cell in CELLS:
                    row.append(cell)
                elif cell != "\n":
                    print(f"Invalid cell type: '{cell}'")
                    sys.exit(1)

            matrix.append(row + ["."] * 2)

        # Adding lower padding to the matrix
        matrix.append(["."] * cols)
        matrix.append(["."] * cols)

        # Get constant height for matrix
        rows = len(matrix)
        print(matrix)

    # 3. Map life simulation rules
    for inner in range(-24, 25):  # 8 cells with (-3 to 3) value each = (-24 to 24)
        for cell in CELLS:
            CELLS[cell][inner] = {}

        for outer in range(-48, 49):  # 16 cells with (-3 to 3) value each = (-48 to 48)
            influence = 2 * inner + outer

            # cell is 'O'
            if influence in POWERS_OF_TWO:
                CELLS["O"][inner][outer] = "."
            elif outer < 2:
                CELLS["O"][inner][outer] = "o"
            else:
                CELLS["O"][inner][outer] = "O"

            # cell is 'o'
            if inner in FIBONACCI_SET:
                CELLS["o"][inner][outer] = "O"
            elif influence <= 0:
                CELLS["o"][inner][outer] = "."
            else:
                CELLS["o"][inner][outer] = "o"

            # cell is '.'
            if influence in PRIME_NUMBERS:
                CELLS["."][inner][outer] = "o"
            elif influence < 0 and -influence in PRIME_NUMBERS:
                CELLS["."][inner][outer] = "x"
            else:
                CELLS["."][inner][outer] = "."

            # cell is 'x'
            if inner < 0 and -inner in FIBONACCI_SET:
                CELLS["x"][inner][outer] = "X"
            elif influence >= 0:
                CELLS["x"][inner][outer] = "."
            else:
                CELLS["x"][inner][outer] = "x"

            # cell is 'X'
            if influence < 0 and -influence in POWERS_OF_TWO:
                CELLS["X"][inner][outer] = "."
            elif outer > -2:
                CELLS["X"][inner][outer] = "x"
            else:
                CELLS["X"][inner][outer] = "X"

    # 3. Matrix Processing
    for _ in range(1):
        sim_matrix = [["."] * cols for _ in range(rows)]
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
                inner_score = (CELLS[low_row[x - 1]]["value"] + CELLS[low_row[x]]["value"] + CELLS[low_row[x + 1]][
                    "value"] + CELLS[self_row[x - 1]]["value"] + CELLS[self_row[x + 1]]["value"] +
                               CELLS[high_row[x - 1]]["value"] + CELLS[high_row[x]]["value"] + CELLS[high_row[x + 1]][
                                   "value"])

                outer_score = (
                            CELLS[lower_row[x - 2]]["value"] + CELLS[lower_row[x - 1]]["value"] + CELLS[lower_row[x]][
                        "value"] + CELLS[lower_row[x + 1]]["value"] + CELLS[lower_row[x + 2]]["value"] +
                            CELLS[low_row[x - 2]]["value"] + CELLS[low_row[x + 2]]["value"] + CELLS[self_row[x - 2]][
                                "value"] + CELLS[self_row[x + 2]]["value"] + CELLS[high_row[x - 2]]["value"] + CELLS[high_row[x + 2]]["value"] +
                            CELLS[higher_row[x - 2]]["value"] + CELLS[high_row[x - 1]]["value"] + CELLS[higher_row[x]][
                                "value"] + CELLS[higher_row[x + 1]]["value"] + CELLS[higher_row[x + 2]]["value"])

                influence_score = 2 * inner_score + outer_score
                cell = self_row[x]
                print(f"cell: {cell}")
                print(f"inner_score: {inner_score}")
                print(f"outer_score: {outer_score}")
                print(f"influence_score: {influence_score}")

                # cell update rules
                sim_matrix[y][x] = CELLS[cell][inner_score][outer_score]
                # sim_matrix cell default values are always 0, so conditionals are optimized to not re-assign 0
                # cell is 'O'
                # if cell == 3:
                #     if influence_score not in POWERS_OF_TWO:
                #         sim_matrix[y][x] = 1 if outer_score < 2 else 3
                #
                # # cell is 'o'
                # elif cell == 1:
                #     if inner_score in FIBONACCI_SET:
                #         sim_matrix[y][x] = 3
                #     elif influence_score > 0:
                #         sim_matrix[y][x] = 1
                #
                # # cell is '.'
                # elif cell == 0:
                #     if influence_score in PRIME_NUMBERS:
                #         sim_matrix[y][x] = 1
                #     elif influence_score < 0 and -influence_score in PRIME_NUMBERS:
                #         sim_matrix[y][x] = -1
                #
                # # cell is 'x'
                # elif cell == -1:
                #     if inner_score < 0 and -inner_score in FIBONACCI_SET:
                #         sim_matrix[y][x] = -3
                #     elif influence_score < 0:
                #         sim_matrix[y][x] = -1
                #
                # # cell is 'X'
                # elif cell == -3:
                #     if influence_score < 0 and -1 * influence_score in POWERS_OF_TWO:
                #         sim_matrix[y][x] = 0
                #     elif outer_score > -2:
                #         sim_matrix[y][x] = -1
                #     else:
                #         sim_matrix[y][x] = -3

                print(f"cell update: {sim_matrix[y][x]}")
                print(f"new matrix: {sim_matrix}\n")

        print(sim_matrix)
        matrix = sim_matrix

    # 4. Write Matrix
    print(matrix)
    with open("test_output.txt", 'w') as file:
        for y in range(2, rows - 2):
            for x in range(2, cols - 2):
                file.write(matrix[y][x])

            file.write('\n')


if __name__ == "__main__":
    main()
