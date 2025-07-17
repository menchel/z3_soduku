import z3
from boards import ALL_BOARDS,EMPTY
SIZE = 9
BOX = 3
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
CYAN = "\033[96m"

def print_board(model, cells, board):
    """
    Prints the Sudoku board
    """
    LINE = f"{CYAN}+-------+-------+-------+{RESET}"
    for i in range(SIZE):
        if i % 3 == 0:
            print(LINE)
        row = []
        for j in range(SIZE):
            val = model.evaluate(cells[i][j])
            cell = str(val)
            if j % 3 == 0:
                row.append(f"{CYAN}|{RESET}")
            row.append(cell)
        row.append(f"{CYAN}|{RESET}")
        print(" ".join(row))
    print(LINE)

def create_solver(BOARD):
    """
    Creating a solver object to represent the board
    """
    solver = z3.Solver()
    cells = [[z3.Int(f"cell_{i}_{j}") for j in range(SIZE)] for i in range(SIZE)]
    
    # constraint 1: values from 1 to 9
    for i in range(SIZE):
        for j in range(SIZE):
            solver.add(z3.And(cells[i][j] >= 1, cells[i][j] <= SIZE))

    # constraint 2: distinct rows
    for i in range(SIZE):
        solver.add(z3.Distinct(cells[i]))

    # constraint 3: distinct cols
    for j in range(SIZE):
        solver.add(z3.Distinct([cells[i][j] for i in range(SIZE)]))

    # constraint 4: distinct boxes
    for box_i in range(BOX):
        for box_j in range(BOX):
            box = [
                cells[i][j]
                for i in range(box_i * BOX, (box_i+1) * BOX)
                for j in range(box_j * BOX, (box_j+1) * BOX)
            ]
            solver.add(z3.Distinct(box))

    # constraint 4: fits the given board
    for i in range(SIZE):
        for j in range(SIZE):
            if BOARD[i][j] is not None:
                solver.add(cells[i][j] == BOARD[i][j])
    return solver,cells

def result(BOARD):
    """
    Prints the result for the solving of the board
    """
    solver,cells = create_solver(BOARD)
    if solver.check() == z3.sat:
        model = solver.model()
        print(f"{GREEN}solution found{RESET}")
        print_board(model, cells,BOARD)
    else:
        print(f"{RED}No solution found{RESET}")

def main():
    for i, board in enumerate(ALL_BOARDS):
        print(f"{BLUE}Solving board {i + 1}{RESET}")
        result(board)
        if i < len(ALL_BOARDS)-1:
            print("\n")

if __name__ == "__main__":
    main()
