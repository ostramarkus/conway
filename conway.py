import random
import numpy as np

def setup_grid(grid_size):
    """Create grid - a 2d nparray"""
    grid = np.zeros((grid_size, grid_size))
    return grid

def count_neighbours(grid, x, y):
    """Count neighbours of position"""
    offsets = [(-1,-1), (0,-1), (1,-1),
               (1,0), (1,1), (0,1),
               (-1,1), (-1,0)]
    return sum(get_cell_val(grid, x+dx, y+dy) for dx, dy in offsets)


def update_grid(grid):
    """Update grid according to the rules - return a new grid"""
    new_grid = grid.copy()

    for index, value in np.ndenumerate(grid):
        x = index[0]
        y = index[1]

        new_value = value

        neighbours = count_neighbours(grid, x, y)

        if value == 1:
            if neighbours < 2 or neighbours > 3: new_value = 0
            else: new_value = 1
        else:
            if neighbours == 3: new_value = 1
            else: new_value = 0

        new_grid[x, y] = new_value

    return new_grid


def get_cell_val(grid, x, y):
    """Get value of position - return 0 if out of grid"""
    try:
        return grid[x, y];
    except IndexError:
        return 0

    
def randomize_grid(grid, density = 40):
    """Randomize values in the grid"""
    grid_size = grid.shape[0]
    cells = density * grid_size
    for i in range(0, cells):
        rand_x = int(random.random() * (grid_size - 1))
        rand_y = int(random.random() * (grid_size - 1))
        grid[rand_x][rand_y] = 1
    return grid