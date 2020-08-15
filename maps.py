import numpy as np
import scipy.ndimage
from cell import Cell
from collections import deque
import time


class TrailMap:
    def __init__(self, size):
        self.size = np.array(size)
        self.grid = np.zeros(self.size)

        self.alpha = 0.6
        self.sigma = 1

    def valid(self, pos):
        return 0 <= pos[0] < self.size[0] and 0 < pos[1] < self.size[1]

    def diffuse(self, data_grid):
        self.grid = self.grid + data_grid
        self.grid = self.alpha * scipy.ndimage.filters.gaussian_filter(self.grid, self.sigma)


class DataMap:
    def __init__(self, size):
        self.size = np.array(size)
        self.grid = np.zeros(self.size, dtype=int)

        self.species = []

    def valid(self, pos):
        return 0 <= pos[0] < self.size[0] and 0 < pos[1] < self.size[1]

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
        print("Generated " + str(i) + "/" + str(amount) + " cells of species " + chr(len(self.species)+64))

        return

    def deposit_species_trail(self):
        for spc in self.species:
            spc.deposit()

    def species_activity(self):

        for spc in self.species:

            for cell in spc.cells:
                cell.observe(spc.trail.grid, True)  # Sense trail of species

            trail_data = np.zeros(self.size)        # Sum trail of all other species
            for cmp_spc in self.species:
                if cmp_spc is not spc:
                    trail_data = trail_data + cmp_spc.trail.grid

            for cell in spc.cells:
                cell.observe(trail_data, False)  # Sense trail of alien species

            for cell in spc.cells:
                cell.move(self, spc)

        return


class Species:
    def __init__(self, cells, grid, trail):
        self.cells = cells
        self.amount = len(cells)
        self.grid = grid
        self.trail = trail

    def deposit(self):
        self.trail.diffuse(self.grid)