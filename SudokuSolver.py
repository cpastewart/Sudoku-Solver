import pygame as pg
import time
import sys

# format for comments at top of functions
# brief description of what function does
# @arguments (if any)
# $return value (if any)


# checks to see if a position x, y on the sudoku board is the same number as any
# other numbers in the same row, column, or 3x3 section of the board.
# @board: A Sudoku board, can have missing values
# @x: the row number of the position to be checked
# @y: the column number of the position to be checked
# $valid: True if board[x][y] contains a valid number, False otherwise
def check_valid(board, x, y):
    if x > 8 or x < 0:
        err = f"x value {x} is out of range"
        sys.exit(err)
    if y > 8 or y < 0:
        err = f"y value {y} is out of range"
        sys.exit(err)

    # empty spaces are always considered valid
    if board[x][y] == 0:
        return True

    # check by column of current number
    for num in range(0, 9):
        if board[x][num] == board[x][y] and num != y:
            return False

        if board[num][y] == board[x][y] and num != x:
            return False


    # check the 3x3 section of current number
    # subtract the remainder from 3 to find the lower bound of the
    # 3x3 section that the current number is in.
    x_lower = x - x % 3
    y_lower = y - y % 3

    # check by 3x3 square
    for i in range(x_lower, x_lower + 3):
        for j in range(y_lower, y_lower + 3):
            # skip loop iteration if it is a comparison between the current square and itself
            if i == x and j == y:
                continue

            if board[i][j] == board[x][y]:
                return False

    # if there are none of the same number in the same column, row, or 3x3 area, then
    # the current space contains a valid number, so return True
    return True


# return a solution to the current board using backtracking. This is used to allow the user
# to attempt to solve the Sudoku board.
# @board: the original game board
# @x: row number to solve for
# @y: column number to solve for
# @display: if True, shows the solving process on the display window
# $solved: the backtracking solution, if any solution exists.
def solve(board, x, y, display=False):
    # if there's already a number here, then it is from the starting board and this function
    # shouldn't change it
    if board[x][y] != 0:
        y = y + 1
        # if y goes out of bounds, go to the next row
        if y > 8:
            y = 0
            x = x + 1
            # if x goes out of bounds, then there are no rows left
            # if we find a valid value and have no rows left, we have found a solution
            if x > 8:
                return board
        # recursively solve the next square on the board
        return solve(board, x, y, display=display)

    for value in range(1, 10):
        board[x][y] = value
        if check_valid(board, x, y) is True:
            #if display is True:
            #    draw_number(value, x, y, correct=True)
            new_y = y + 1
            # if y goes out of bounds, go to the next row
            if new_y > 8:
                new_y = 0
                new_x = x + 1
                # if x goes out of bounds, then there are no rows left
                # if we find a valid value and have no rows left, we have found a solution
                if new_x > 8:
                    return board
            else:
                new_x = x

            solution = solve(board, new_x, new_y, display=display)
            # if there are 0's on the board, we have not found a solution, so continue to next number
            if 0 in (values for rows in board for values in rows):
                continue
            return solution
        #else:
            #if display is True:
            #    draw_number(value, x, y, correct=False)
    # if no numbers have returned a solution, then backtrack by resetting the space to 0
    # and returning the original board
    board[x][y] = 0
    #if display is True:
    #    draw_number(0, x, y, correct=False)
    return board




# function to draw the Sudoku board, including grid lines and current numbers
# @board: the original game board
# @solution: the current solution including numbers not on the starting board
def draw_board(board, solved):
    window.fill(BACK_COLOR)
    for x in range(0, SIZE + SQUARE_SIZE, SQUARE_SIZE):
        pg.draw.line(window, SQUARE_COLOR, (x, 0), (x, SIZE))
    for y in range(0, SIZE + SQUARE_SIZE, SQUARE_SIZE):
        pg.draw.line(window, SQUARE_COLOR, (0, y), (SIZE, y))

    for x in range(0, SIZE + BLOCK_SIZE, BLOCK_SIZE):
        pg.draw.line(window, BLOCK_COLOR, (x, 0), (x, SIZE), 2)
    for y in range(0, SIZE + BLOCK_SIZE, BLOCK_SIZE):
        pg.draw.line(window, BLOCK_COLOR, (0, y), (SIZE, y), 2)

    # TODO: Display numbers in each box
    # TODO: Draw squares for valid/invalid numbers

def draw_timer(draw_time, font):
    minutes = str(int(draw_time / 60000)).zfill(2)
    seconds = str(int((draw_time % 60000) / 1000)).zfill(2)

    global BLOCK_COLOR
    global SIZE
    global SQUARE_SIZE
    global window
    text = font.render(f"{minutes}:{seconds}", 1, BLOCK_COLOR)
    window.blit(text, (SQUARE_SIZE * 7.5, SIZE + (SQUARE_SIZE * 0.2)))


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


pg.init()
pg.display.set_caption("Sudoku Solver")

# board with fixed values, edit this to edit the puzzle. Board will be format checked to make sure
# it is a valid 9x9 Sudoku puzzle. Includes check for contradictions, such as multiple of the same number
# in a single row.
#starting_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
#                  [0, 0, 0, 0, 0, 3, 0, 8, 5],
#                  [0, 0, 1, 0, 2, 0, 0, 0, 0],
#                  [0, 0, 0, 5, 0, 7, 0, 0, 0],
#                  [0, 0, 4, 0, 0, 0, 1, 0, 0],
#                  [0, 9, 0, 0, 0, 0, 0, 0, 0],
#                  [5, 0, 0, 0, 0, 0, 0, 7, 3],
#                  [0, 0, 2, 0, 1, 0, 0, 0, 0],
#                  [0, 0, 0, 0, 4, 0, 0, 0, 9]]

starting_board = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
                  [6, 0, 0, 1, 9, 5, 0, 0, 0],
                  [0, 9, 8, 0, 0, 0, 0, 6, 0],
                  [8, 0, 0, 0, 6, 0, 0, 0, 3],
                  [4, 0, 0, 8, 0, 3, 0, 0, 1],
                  [7, 0, 0, 0, 2, 0, 0, 0, 6],
                  [0, 6, 0, 0, 0, 0, 2, 8, 0],
                  [0, 0, 0, 4, 1, 9, 0, 0, 5],
                  [0, 0, 0, 0, 8, 0, 0, 7, 9]]

# error checking the board
# check number of rows
if len(starting_board) != 9:
    pg.quit()
    err = f"Could not load Sudoku: contains {len(starting_board)} rows instead of 9"
    sys.exit(err)

for x_pos in range(0, 9):
    # check each row for correct number of elements
    if len(starting_board[x_pos]) != 9:
        pg.quit()
        err = f"Could not load Sudoku: row {x_pos + 1} has {len(starting_board[x_pos])} values instead of 9"
        sys.exit(err)
    # checking for invalid values
    for y_pos in range(0, 9):
        val = starting_board[x_pos][y_pos]
        if isinstance(val, int) is False or val < 0 or val > 9:
            pg.quit()
            err = f"Could not load Sudoku: contains invalid value '{val}' in row {x_pos + 1}"
            sys.exit(err)

        if check_valid(starting_board, x_pos, y_pos) is False:
            pg.quit()
            err = f"Loaded Sudoko is invalid, row {y_pos + 1}, column {x_pos + 1} contains invalid number."
            sys.exit(err)


# colors
BLOCK_COLOR = (0, 0, 0)
BACK_COLOR = (240, 240, 240)
SQUARE_COLOR = (180, 180, 180)
CORRECT_COLOR = (3, 98, 252)
INCORRECT_COLOR = (222, 27, 27)


# window details
MINSIZE = 90
MULTIPLIER = 7
SIZE = MINSIZE * MULTIPLIER

# grid details
SQUARE_SIZE = int(SIZE / 9)
BLOCK_SIZE = int(SIZE / 3)

# font
numfont = pg.font.SysFont("arial", int(SQUARE_SIZE * 0.6))

window = pg.display.set_mode((SIZE + 2, SIZE + SQUARE_SIZE + 1))

solved = solve(starting_board, 0, 0)
for row in solved:
    print(row)
solution = starting_board

start_time = pg.time.get_ticks()

draw_board(starting_board, solution)
running = True
while running:
    pg.time.delay(100)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()

    if keys[pg.K_SPACE]:
        solve(starting_board, 0, 0, display=True)

    # TODO: Make 3 strikes system
    # TODO: Make Light/Dark mode button

    current_time = pg.time.get_ticks() - start_time

    draw_board(starting_board, solution)
    draw_timer(current_time, numfont)
    pg.display.update()

pg.quit()
