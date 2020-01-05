import pygame as pg
import time
import sys

# format for comments at top of functions
# brief description of what function does
# @arguments (if any)
# $return value (if any)

pg.init()
pg.display.set_caption("Sudoku Solver")

# board with fixed values, edit this to edit the puzzle. Board will be format checked to make sure
# it is a valid 9x9 Sudoku puzzle. Includes check for contradictions, such as multiple of the same number
# in a single row.
board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 3, 0, 8, 5],
         [0, 0, 1, 0, 2, 0, 0, 0, 0],
         [0, 0, 0, 5, 0, 7, 0, 0, 0],
         [0, 0, 4, 0, 0, 0, 1, 0, 0],
         [0, 9, 0, 0, 0, 0, 0, 0, 0],
         [5, 0, 0, 0, 0, 0, 0, 7, 3],
         [0, 0, 2, 0, 1, 0, 0, 0, 0],
         [0, 0, 0, 0, 4, 0, 0, 0, 9]]

### error checking the board
# check number of rows
if len(board) != 9:
    pg.quit()
    err = f"Could not load Sudoku: contains {len(board)} rows instead of 9"
    sys.exit(err)

for x in range(0, 9):
    # check each row for correct number of elements
    if len(board[x]) != 9:
        pg.quit()
        err = f"Could not load Sudoku: row {x + 1} has {len(board[x])} values instead of 9"
        sys.exit(err)
    # checking for invalid values
    for y in board[x]:
        if isinstance(y, int) is False or y < 0 or y > 9:
            pg.quit()
            err = f"Could not load Sudoku: contains invalid value '{y}' in row {x + 1}"
            sys.exit(err)

# colors
BLOCK_COLOR = (0, 0, 0)
BACK_COLOR = (240, 240, 240)
SQUARE_COLOR = (180, 180, 180)
CORRECT_COLOR = (3, 98, 252)
INCORRECT_COLOR = (222, 27, 27)


### change color scheme

# changes the background to be darker, makes main lines lighter to stand out
def make_dark():
    global BLOCK_COLOR
    global BACK_COLOR
    BLOCK_COLOR = (250, 250, 250)
    BACK_COLOR = (30, 30, 30)


# reverts to original color scheme with off-white background
def make_light():
    global BLOCK_COLOR
    global BACK_COLOR
    BLOCK_COLOR = (0, 0, 0)
    BACK_COLOR = (240, 240, 240)


# window details
MINSIZE = 90
MULTIPLIER = 7
SIZE = MINSIZE * MULTIPLIER

# grid details
SQUARE_SIZE = int(SIZE / 9)
BLOCK_SIZE = int(SIZE / 3)

window = pg.display.set_mode((SIZE + 2, SIZE + SQUARE_SIZE + 1))

# return a solution to the current board using backtracking. This is used to allow the user
# to attempt to solve the Sudoku board.
# @board: the original game board
# $solved: the backtracking solution, if any solution exists.
def solve(board):
    solved = board
    return solved


# function to draw the Sudoku board, including grid lines and current numbers
# @board: the original game board
# @solution: the current solution including numbers not on the starting board
def draw_board(board, solution):
    window.fill(BACK_COLOR)
    for x in range(0, SIZE + SQUARE_SIZE, SQUARE_SIZE):
        pg.draw.line(window, SQUARE_COLOR, (x, 0), (x, SIZE))
    for y in range(0, SIZE + SQUARE_SIZE, SQUARE_SIZE):
        pg.draw.line(window, SQUARE_COLOR, (0, y), (SIZE, y))

    for x in range(0, SIZE + BLOCK_SIZE, BLOCK_SIZE):
        pg.draw.line(window, BLOCK_COLOR, (x, 0), (x, SIZE), 2)
    for y in range(0, SIZE + BLOCK_SIZE, BLOCK_SIZE):
        pg.draw.line(window, BLOCK_COLOR, (0, y), (SIZE, y), 2)


# draws the solution to demonstrate backtracking
# @board the unsolved Sudoku board
def show_solution(board):
    none = False


solved = solve(board)
solution = board

running = True
while running:
    pg.time.delay(100)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()

    if keys[pg.K_SPACE]:
        show_solution(board, window)

    make_dark()
    draw_board(board, solution)
    pg.display.update()

pg.quit()
