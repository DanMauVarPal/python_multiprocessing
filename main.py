import argparse
import sys

POWERS_OF_TWO = {1, 2, 4, 8, 16, 32, 64}
FIBONACCI_SET = {0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89}
PRIME_NUMBERS = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89}

# 1.3.1 Symbols
# 1.3.2.2 Value assigned based on state
CELL_VALUE = {"O": 3, "o": 1, ".": 0, "x": -1, "X": -3}

STAGE_UPDATE = {
    'O': {"value": 3},
    'o': {"value": 1},
    ".": {"value": 0},
    "x": {"value": -1},
    "X": {"value": -3}
}


def main():
    print("Project :: R11998328")

    # 1.1 Data Retrieval
    # parser = argparse.ArgumentParser(description="Serial Cellular Life Simulator")
    # parser.add_argument('-i', type=str, required=True, help="Path to the starting cellular matrix")
    # parser.add_argument('-o', type=str, required=True, help="Path for the final output file")
    # parser.add_argument('-p', type=int, default=1, help="Number of processes to spawn (Ignored in Phase 1)")
    #
    # args = parser.parse_args()

    # 1.2.1 Read Matrix
    matrix = []
    # with open(args.i) as file:
    with open("ten_by_ten/time_step_0.dat") as file:
        # Get first line in file
        file_line = file.readline().strip()

        # Adding padding to the row start
        row = ["."] * 2

        # Getting all cells in row from file
        for cell in file_line:
            if cell in STAGE_UPDATE:
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
                if cell in STAGE_UPDATE:
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

    # 1.3.2 Iterative Rules
    for inner_score in range(-24, 25):  # 8 cells with (-3 to 3) value each = (-24 to 24)
        for cell in STAGE_UPDATE:
            STAGE_UPDATE[cell][inner_score] = {}

        for outer_score in range(-48, 49):  # 16 cells with (-3 to 3) value each = (-48 to 48)
            # 1.3.2.3c influence_score
            influence_score = 2 * inner_score + outer_score

            # 1.3.2.4 cell is 'O'
            if influence_score in POWERS_OF_TWO:
                STAGE_UPDATE["O"][inner_score][outer_score] = "."
            elif outer_score < 2:
                STAGE_UPDATE["O"][inner_score][outer_score] = "o"
            else:
                STAGE_UPDATE["O"][inner_score][outer_score] = "O"

            # 1.3.2.5 cell is 'o'
            if inner_score in FIBONACCI_SET:
                STAGE_UPDATE["o"][inner_score][outer_score] = "O"
            elif influence_score <= 0:
                STAGE_UPDATE["o"][inner_score][outer_score] = "."
            else:
                STAGE_UPDATE["o"][inner_score][outer_score] = "o"

            # 1.3.2.6 cell is '.'
            if influence_score in PRIME_NUMBERS:
                STAGE_UPDATE["."][inner_score][outer_score] = "o"
            elif influence_score < 0 and -influence_score in PRIME_NUMBERS:
                STAGE_UPDATE["."][inner_score][outer_score] = "x"
            else:
                STAGE_UPDATE["."][inner_score][outer_score] = "."

            # 1.3.2.7 cell is 'x'
            if inner_score < 0 and -inner_score in FIBONACCI_SET:
                STAGE_UPDATE["x"][inner_score][outer_score] = "X"
            elif influence_score >= 0:
                STAGE_UPDATE["x"][inner_score][outer_score] = "."
            else:
                STAGE_UPDATE["x"][inner_score][outer_score] = "x"

            # 1.3.2.8 cell is 'X'
            if influence_score < 0 and -influence_score in POWERS_OF_TWO:
                STAGE_UPDATE["X"][inner_score][outer_score] = "."
            elif outer_score > -2:
                STAGE_UPDATE["X"][inner_score][outer_score] = "x"
            else:
                STAGE_UPDATE["X"][inner_score][outer_score] = "X"

    # 1.3 Matrix Processing
    for _ in range(100):
        sim_matrix = [["."] * cols for _ in range(rows)]
        # matrix iteration
        for y in range(2, rows - 2):
            lower_row = matrix[y - 2]
            low_row = matrix[y - 1]
            self_row = matrix[y]
            high_row = matrix[y + 1]
            higher_row = matrix[y + 2]

            for x in range(2, cols - 2):
                # 1.3.2.1a Inner ring consisting of 8 adjacent cells
                inner_score = (
                    # low_row
                        STAGE_UPDATE[low_row[x - 1]]["value"] + STAGE_UPDATE[low_row[x]]["value"] +
                        STAGE_UPDATE[low_row[x + 1]]["value"] +
                        # self_row
                        STAGE_UPDATE[self_row[x - 1]]["value"] + STAGE_UPDATE[self_row[x + 1]]["value"] +
                        # high_row
                        STAGE_UPDATE[high_row[x - 1]]["value"] + STAGE_UPDATE[high_row[x]]["value"] +
                        STAGE_UPDATE[high_row[x + 1]]["value"]
                )

                # 1.3.2.1b Outer ring consisting of remaining 16 cells within 5x5 region
                outer_score = (
                    # lower_row
                        STAGE_UPDATE[lower_row[x - 2]]["value"] + STAGE_UPDATE[lower_row[x - 1]]["value"] +
                        STAGE_UPDATE[lower_row[x]]["value"] +
                        STAGE_UPDATE[lower_row[x + 1]]["value"] + STAGE_UPDATE[lower_row[x + 2]]["value"] +
                        # low_row
                        STAGE_UPDATE[low_row[x - 2]]["value"] + STAGE_UPDATE[low_row[x + 2]]["value"] +
                        # self_row
                        STAGE_UPDATE[self_row[x - 2]]["value"] + STAGE_UPDATE[self_row[x + 2]]["value"] +
                        # high_row
                        STAGE_UPDATE[high_row[x - 2]]["value"] + STAGE_UPDATE[high_row[x + 2]]["value"] +
                        # higher_row
                        STAGE_UPDATE[higher_row[x - 2]]["value"] + STAGE_UPDATE[higher_row[x - 1]]["value"] +
                        STAGE_UPDATE[higher_row[x]]["value"] +
                        STAGE_UPDATE[higher_row[x + 1]]["value"] + STAGE_UPDATE[higher_row[x + 2]]["value"]
                )

                sim_matrix[y][x] = STAGE_UPDATE[self_row[x]][inner_score][outer_score]

        matrix = sim_matrix

    # 1.2.2 Write Matrix
    with open("test_output.txt", 'w') as file:
        for y in range(2, rows - 2):
            for x in range(2, cols - 2):
                file.write(matrix[y][x])

            file.write('\n')


if __name__ == "__main__":
    main()
