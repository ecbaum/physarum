import numpy as np
import scipy.ndimage
from helpers import grid_id, valid
from cell import Cell


class Species:
    def __init__(self, size):
        self.size = size
        self.grid = np.zeros(self.size, dtype=int)
        self.population_map = np.zeros(self.size, dtype=int)
        self.trail = Trail(size)
        self.cells = []
        self.amount = []

    def generate_cells(self, amount):

        self.cells = np.empty(amount, dtype=Cell)  # Cells in species
        r = self.size[0] / 2 * 0.8
        c = self.size / 2
        i = 0
        for k in range(amount):
            for tries in range(30):
                pos = self.size * np.random.rand(2)
                if np.linalg.norm(c-pos) < r:
                    self.grid[grid_id(pos)] = 1  # Add cell pos to global grid
                    self.grid[grid_id(pos)] = 1  # Add cell pos to species grid

                    self.cells[i] = Cell(pos)
                    i += 1
                    break

    def deposit(self):
        self.trail.diffuse(self.grid)

    def activate(self, data_map):
        trail_env = 2 * self.trail.grid - data_map.trail_sum
        for cell in self.cells:
            cell.observe(trail_env)  # Sense trail of species
            cell.move(data_map, self)

    def update_population_map(self):
        self.population_map = np.zeros(self.size, dtype=int)
        for cell in self.cells:
            self.population_map[cell.pos] += 1


class Trail:
    def __init__(self, size):
        self.size = np.array(size)
        self.grid = np.zeros(self.size)

        self.alpha = 0.7
        self.sigma = 1

    def diffuse(self, data_grid):
        self.grid = self.grid + data_grid
        self.grid = self.alpha * scipy.ndimage.filters.gaussian_filter(self.grid, self.sigma)


class Nutrient:
    def __init__(self, size):
        self.size = np.array(size)
        self.grid = np.zeros(self.size)
        self.dr = 1  # diffusion radius

    def diffuse(self, population_map):
        for i in range(self.size[0]):
            for j in range(self.size[1]):

                cell_amount = population_map[i, j]
                neighbour_cell = list()
                nutrient_lvl = 0

                if cell_amount >= 1:
                    for ii in range(-self.dr+1, self.dr+1):
                        for jj in range(-self.dr+1, self.dr+1):
                            x_pos = ii + i
                            y_pos = jj + j
                            if valid([x_pos, y_pos], self.grid) and population_map[x_pos, y_pos] >= 1:
                                neighbour_cell.append([x_pos, y_pos])
                                nutrient_lvl += self.grid[x_pos, y_pos]
                else:
                    continue

                n = len(neighbour_cell)
                for k in range(n):
                    x_pos = neighbour_cell[k][0]
                    y_pos = neighbour_cell[k][1]
                    self.grid[x_pos, y_pos] = nutrient_lvl/n


