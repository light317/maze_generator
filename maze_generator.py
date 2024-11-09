import time
import pygame
import argparse
import sys
import random

pygame.init()

grid_width = 300
grid_height = 100
cell_size = 5


pygame.display.set_caption('Life')
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)


stack = []


class Cell:
    def __init__(self, x, y, color, east_wall=True, south_wall=True, north_wall=False, west_wall=False):
        self.x = x
        self.y = y
        self.color = color
        self.east_wall = east_wall
        self.south_wall = south_wall
        self.north_wall = north_wall
        self.west_wall = west_wall
        self.visited = False
        self.is_head = False


def genrate_grid(width, height):
    # return [[random.randint(0, 1) for _ in range(width)] for _ in range(height)]
    grid = [[Cell(x, y, white) for x in range(width)]
            for y in range(height)]

    for i in range(0, len(grid)):
        grid[i][0].west_wall = True

    for i in range(0, len(grid[0])):
        grid[0][i].north_wall = True

    return grid


def draw_grid_from_array(screen, array):
    for y, row in enumerate(array):
        for x, cell in enumerate(row):
            # color = white if cell == 0 else black
            east_wall = 2 if cell.east_wall else 0
            south_wall = 2 if cell.south_wall else 0
            north_wall = 2 if cell.north_wall else 0
            west_wall = 2 if cell.west_wall else 0
            color2 = black if cell.visited else white
            color = green if cell.is_head else color2
            pygame.draw.rect(screen, color, (x * cell_size + west_wall,
                             y * cell_size + north_wall, cell_size - east_wall - west_wall, cell_size - south_wall - north_wall))
            # pygame.draw.rect(screen, black, (x * cell_size, y *
            #                  cell_size, cell_size, cell_size), 1)  # grid lines


def get_all_valid_neighbors(grid, cell):
    valid_cells = []

    if cell.x - 1 >= 0:
        if not grid[cell.y][cell.x-1].visited:
            valid_cells.append((grid[cell.y][cell.x-1], "LEFT"))

    if cell.x + 1 <= len(grid[0])-1:
        if not grid[cell.y][cell.x+1].visited:
            valid_cells.append((grid[cell.y][cell.x+1], "RIGHT"))

    if cell.y - 1 >= 0:
        if not grid[cell.y-1][cell.x].visited:
            valid_cells.append((grid[cell.y-1][cell.x], "UP"))

    if cell.y + 1 <= len(grid)-1:
        if not grid[cell.y+1][cell.x].visited:
            valid_cells.append((grid[cell.y+1][cell.x], "DOWN"))

    return valid_cells


def get_random_neighbor(cells):

    return random.choice(cells)

# def iterrate_life(old_grid):
#     new_grid = generate_grid(len(old_grid), len(old_grid[0]))
#
#     return new_grid


# We can later pass in the type of neighbors we are counting via enum, so it is
# reusable
# def count_neighbors(cell, grid):
#     count: int = 0
#
#     if grid[(cell[0]-1) % grid_width][(cell[1] - 1) % grid_height] == 1:
#         count = count + 1
#
#     if grid[(cell[0]-1) % grid_width][(cell[1]) % grid_height] == 1:
#         count = count + 1
#
#     if grid[(cell[0]-1) % grid_width][(cell[1]+1) % grid_height] == 1:
#         count = count + 1
#
#     if grid[(cell[0]+1) % grid_width][(cell[1]-1) % grid_height] == 1:
#         count = count + 1
#
#     if grid[(cell[0]+1) % grid_width][(cell[1]) % grid_height] == 1:
#         count = count + 1
#
#     if grid[(cell[0]+1) % grid_width][(cell[1]+1) % grid_height] == 1:
#         count = count + 1
#
#     if grid[cell[0]][(cell[1]-1) % grid_height] == 1:
#         count = count + 1
#
#     if grid[cell[0]][(cell[1]+1) % grid_height] == 1:
#         count = count + 1
#
#     return count


def full_maze_solve(screen, grid):
    print("In run life")

    while len(stack) != 0:
        solve_maze(grid)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw(screen, grid)


def live_maze_solve(screen, grid):
    print("In run life")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        solve_maze(grid)
        draw(screen, grid)


def draw(screen, grid):
    screen.fill(blue)  # You can use a different background color
    draw_grid_from_array(screen, grid)
    pygame.display.flip()
    # time.sleep(0.05)


def solve_maze(grid):

    # logic to generate maze
    if not len(stack) == 0:
        current_cell = stack[-1]

        neighbors = get_all_valid_neighbors(grid, current_cell)

        while len(neighbors) == 0 and len(stack) != 0:
            grid[current_cell.y][current_cell.x].is_head = False
            stack.pop()

            if len(stack) == 0:
                break

            current_cell = stack[-1]

            neighbors = get_all_valid_neighbors(grid, current_cell)

        if len(neighbors) == 0:
            return

        chosen_neighbor = get_random_neighbor(neighbors)

        if chosen_neighbor[1] == "RIGHT":
            grid[current_cell.y][current_cell.x].east_wall = False

        elif chosen_neighbor[1] == "DOWN":
            grid[current_cell.y][current_cell.x].south_wall = False

        stack.append(grid[chosen_neighbor[0].y][chosen_neighbor[0].x])

        grid[current_cell.y][current_cell.x].is_head = False

        stack[-1].visited = True
        stack[-1].is_head = True
        current_cell = stack[-1]

        if chosen_neighbor[1] == "LEFT":
            grid[current_cell.y][current_cell.x].east_wall = False

        elif chosen_neighbor[1] == "UP":
            grid[current_cell.y][current_cell.x].south_wall = False


def main():
    print("in main")
    parser = argparse.ArgumentParser()
    parser.add_argument('--grid_width', type=int, default=30)
    parser.add_argument('--grid_height', type=int, default=20)
    parser.add_argument('--gen_style', type=str, default="live")
    args = parser.parse_args()

    global grid_width
    grid_width = args.grid_width

    global grid_height
    grid_height = args.grid_height

    gen_style = args.gen_style

    screen = pygame.display.set_mode(
        (grid_width * cell_size, grid_height * cell_size))
    # grid = genrate_random_grid(args.grid_width, args.grid_height)
    # new_grid = iterrate_life(grid)

    # live_neighbors = count_neighbors((0, 0), grid)
    # print(live_neighbors)

    grid = genrate_grid(grid_width, grid_height)

    starting_point = grid[random.randint(
        0, grid_height-1)][random.randint(0, grid_width-1)]

    starting_point.visited = True
    starting_point.is_head = True
    stack.append(starting_point)

    if gen_style == "full":
        full_maze_solve(screen, grid)
    else:
        live_maze_solve(screen, grid)
    # full_maze_solve(screen, grid)


if __name__ == '__main__':
    main()
