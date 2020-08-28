import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt
from cell import Cell
from helpers import grid_id




class TrailMap:
    def __init__(self, size):
        self.size = np.array(size)
        self.grid = np.zeros(self.size)

        self.alpha = 0.6
        self.sigma = 1

    def diffuse(self, data_grid):
        self.grid = self.grid + data_grid
        self.grid = self.alpha * scipy.ndimage.filters.gaussian_filter(self.grid, self.sigma)


class DataMap:
    def __init__(self, size):
        self.size = np.array(size)
        self.grid = np.zeros(self.size, dtype=int)

        self.species = []
        self.trail_sum = np.zeros(self.size)

        self.color_bias = [0, 0.45, 0.6]
        self.color_maps = {0: 'Greens', 1: 'Reds', 2: 'Blues'}
        self.color_intensity = [5, 5, 5]

    def img(self):
        img = np.zeros(np.hstack((self.size, 4)))
        n = len(self.species)
        for i in range(n):
            c_map = plt.get_cmap(self.color_maps[i])
            img = img + c_map(self.color_intensity[i] * self.species[i].trail.grid) - self.color_bias[n-1]
        img[np.where(img > 1)] = 1
        img[np.where(img < 0)] = 0
        return img

    def generate_cell_species(self, amount):
        if len(self.species) >= 3:
            raise Exception("Color map currently only support up to three species")
        cells = np.empty(amount, dtype=Cell)          # Cells in species
        spc_grid = np.zeros(self.size, dtype=int)     # Species grid

        i = 0
        for k in range(amount):
            for tries in range(30):
                pos = self.size*np.random.rand(2)
                if self.grid[grid_id(pos)] == 0:

                    self.grid[grid_id(pos)] = 1   # Add cell pos to global grid
                    spc_grid[grid_id(pos)] = 1    # Add cell pos to species grid

                    cells[i] = Cell(pos)
                    i += 1
                    break

        species = Species(cells[0:i], spc_grid, TrailMap(self.size))
        self.species.append(species)

    def deposit_species_trail(self):
        #  Clear Trail sum
        self.trail_sum = np.zeros(self.size)

        for spc in self.species:
            spc.deposit()
            self.trail_sum += spc.trail.grid  # sum all trails

    def species_activity(self):

        for spc in self.species:

            # Species specific trail environment (E) = within species trail (W) - alien species trails (A)
            # trail_sum (S) = within species trail (W) + alien species trails (A)

            # S = W + A  =>   A = S - W;    E = W - A =  W - (S - W)  =  2*W - S

            trail_env = 2*spc.trail.grid - self.trail_sum

            for cell in spc.cells:
                cell.observe(trail_env)  # Sense trail of species

            for cell in spc.cells:
                cell.move(self, spc)


class Species:
    def __init__(self, cells, grid, trail):
        self.cells = cells
        self.amount = len(cells)
        self.grid = grid
        self.trail = trail

    def deposit(self):
        self.trail.diffuse(self.grid)
