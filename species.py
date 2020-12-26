import numpy as np
import scipy.ndimage
from helpers import grid_id, valid
from cell import Cell


class Species:
    def __init__(self, size, env):
        self.size = size
        self.cells = []
        self.amount = []
        self.id = -1
        self.env = env

    def generate_cells(self, amount):

        self.cells = np.empty(amount, dtype=Cell)  # Cells in species
        r = self.size[0] / 2 * 0.8
        c = self.size / 2
        i = 0
        for k in range(amount):
            for tries in range(30):
                pos = self.size * np.random.rand(2)
                if np.linalg.norm(c-pos) < r:
                    cell = Cell(pos, self.id)
                    self.cells[i] = cell
                    self.env.data_map[pos[0]][pos[1]].append(cell)
                    i += 1
                    break

    def activate(self, data_map):
        trail_env = 2 * self.trail.grid - data_map.trail_sum
        for cell in self.cells:
            cell.observe(trail_env)  # Sense trail of species
            cell.move(data_map, self)

    def diffuse_nutrients(self, population_map):
        dr = 1  # diffusion radius
        for i in range(self.size[0]):
            for j in range(self.size[1]):

                cell_amount = population_map[i, j]
                neighbour_cell = list()
                nutrient_lvl = 0

                if cell_amount >= 1:
                    for ii in range(-dr+1, dr+1):
                        for jj in range(-dr+1, dr+1):
                            x_pos = ii + i
                            y_pos = jj + j
                            if valid([x_pos, y_pos], self.env.grid) and population_map[x_pos, y_pos] >= 1:
                                neighbour_cell.append([x_pos, y_pos])
                                nutrient_lvl += self.grid[x_pos, y_pos]
                else:
                    continue

                n = len(neighbour_cell)
                for k in range(n):
                    x_pos = neighbour_cell[k][0]
                    y_pos = neighbour_cell[k][1]
                    self.grid[x_pos, y_pos] = nutrient_lvl/n


