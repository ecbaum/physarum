import numpy as np
import scipy.ndimage
from helpers import grid_id
from cell import Cell


class Species:
    def __init__(self, size):
        self.size = size
        self.grid = np.zeros(self.size, dtype=int)
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


class Trail:
    def __init__(self, size):
        self.size = np.array(size)
        self.grid = np.zeros(self.size)

        self.alpha = 0.6
        self.sigma = 1

    def diffuse(self, data_grid):
        self.grid = self.grid + data_grid
        self.grid = self.alpha * scipy.ndimage.filters.gaussian_filter(self.grid, self.sigma)
