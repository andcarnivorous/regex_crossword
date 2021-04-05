"""
This module is from this geeksforgeeks article https://www.geeksforgeeks.org/building-and-visualizing-sudoku-game-using-pygame/
"""

import pygame
from drawer import Drawer
from key_map import KeyMapper
from regex_generator import PuzzleGenerator

# initialise the pygame font
pygame.font.init()

# Total window
screen = pygame.display.set_mode((1200, 900))

# Title and Icon
pygame.display.set_caption("RegEx Crosswords :D")

x = 0
y = 0
dif = 500 / 9
val = 0
# Default Sudoku Board.
size = 10
puzzle = PuzzleGenerator(size)
result_grid = puzzle.letters_matrix
grid = puzzle.empty_matrix

# Load test fonts for future use
font1 = pygame.font.SysFont("comicsans", 40)
font2 = pygame.font.SysFont("comicsans", 20)

drawer = Drawer(screen, font1, font2, x, y)


def get_cord(pos):
    global x
    x = pos[0]//dif
    global y
    y = pos[1]//dif
    drawer.update_xy(x, y)


run = True
flag1 = 0
flag2 = 0
rs = 0
error = 0
# The loop thats keep the window running
while run:

    # White color background
    screen.fill((255, 255, 255))
    # Loop through the events stored in event.get()
    for event in pygame.event.get():
        # Quit the game window
        if event.type == pygame.QUIT:
            run = False
        # Get the mouse postion to insert number
        if event.type == pygame.MOUSEBUTTONDOWN:
            flag1 = 1
            pos = pygame.mouse.get_pos()
            get_cord(pos)
        # Get the number to be inserted if key pressed
        if event.type == pygame.KEYDOWN:

            key = KeyMapper(event, size, x, y)
            x, y = key.x, key.y
            drawer.update_xy(key.x, key.y)
            val = key.uni if key.valid else ""
            # If R pressed clear the sudoku board
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
#                grid = puzzle.empty_matrix            # If D is pressed reset the board to default

    if list(grid.flatten()) == puzzle.solution:
        flag2 = 1
    if flag2 == 1:
        rs = 1
        flag2 = 0
    if val:
        drawer.draw_val(val)

        grid[int(drawer.x)-10][int(drawer.y)] = val.upper()
        val = 0

    if rs == 1:
        drawer.draw_result()
    drawer.draw(puzzle.letters_matrix.shape[0], grid)
    if flag1 == 1:
        drawer.draw_box()
    drawer.draw_expressions(puzzle.rows_expressions, puzzle.cols_expressions)
    drawer.draw_instruction()

    # Update window
    pygame.display.update()

# Quit pygame window
pygame.quit()
