import random
import numpy as np

def setup_grid(grid_size):
    grid = np.zeros((grid_size, grid_size))
    return grid


def update_grid(grid):
    new_grid = grid.copy()

    for index, value in np.ndenumerate(grid):
        x = index[0]
        y = index[1]

        new_value = value

        neighbours = 0

        neighbours += get_cell_val(grid, x - 1, y - 1)
        neighbours += get_cell_val(grid, x, y - 1)
        neighbours += get_cell_val(grid, x + 1, y - 1)

        neighbours += get_cell_val(grid, x + 1, y)

        neighbours += get_cell_val(grid,x + 1, y + 1)
        neighbours += get_cell_val(grid,x, y + 1)
        neighbours += get_cell_val(grid,x - 1, y + 1)

        neighbours += get_cell_val(grid,x - 1, y)

        if value == 1:
            if neighbours < 2: new_value = 0
            if neighbours == 2 or neighbours == 3: new_value = 1
            if neighbours > 3: new_value = 0
        else:
            if neighbours == 3: new_value = 1

        new_grid[x, y] = new_value

    return new_grid.copy()


def get_cell_val(grid, x, y):
    try:
        return grid[x, y];
    except IndexError:
        return 0

    
def randomize_grid(grid, nr_of_active_cells = 40):
    grid_size = grid.shape[0]
    cells = nr_of_active_cells * grid_size
    for i in range(0, cells):
        rand_x = int(random.random() * (grid_size - 1))
        rand_y = int(random.random() * (grid_size - 1))
        grid[rand_x][rand_y] = 1
    return grid