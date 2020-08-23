import numpy as np
import scipy.ndimage
from cell import Cell
import matplotlib.pyplot as plt


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

        self.color_maps = {0: 'viridis', 1: 'plasma', 2: 'cubehelix'}
        self.color_intensity = [9, 7, 5]
        if len(self.species) > 3:
            raise Exception("Color map currently only support up to three species")

    def img(self):
        img = np.zeros(np.hstack((self.size, 4)))
        bias = 0 if len(self.species) == 1 else 0.2
        for i in range(len(self.species)):
            img = img + plt.get_cmap(self.color_maps[i])(self.color_intensity[i]*self.species[i].trail.grid) - bias
        img[np.where(img > 1)] = 1
        img[np.where(img < 0)] = 0
        return img

    def generate_cell_species(self, amount):

        cells = np.empty(amount, dtype=Cell)          # Cells in species
        spc_grid = np.zeros(self.size, dtype=int)     # Species grid

        i = 0
        for k in range(amount):
            for tries in range(30):
                pos = self.size*np.random.rand(2)
                if self.grid[tuple(pos.astype(int))] == 0:

                    self.grid[tuple(pos.astype(int))] = 1   # Add cell pos to global grid
                    spc_grid[tuple(pos.astype(int))] = 1    # Add cell pos to species grid

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
