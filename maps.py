import numpy as np
import scipy.ndimage
from cell import Cell


class DataMap:
    def __init__(self, size):
        self.size = np.array(size)
        self.grid = np.zeros(self.size, dtype=int)
        self.cells = []

    def generate_cells(self, amount):

        self.cells = np.empty(amount, dtype=Cell)

        i = 0
        for k in range(amount):
            for tries in range(30):
                pos = self.size*np.random.rand(2)
                if self.grid[tuple(pos.astype(int))] == 0:
                    self.grid[tuple(pos.astype(int))] = 1
                    self.cells[i] = Cell(pos)
                    i += 1
                    break

        self.cells = self.cells[0:i]
        print("Generated " + str(i) + "/" + str(amount) + " cells")
        return

    def cell_operation(self, tm):
        for cell in self.cells:
            cell.observe(tm)  # Sensory stage
            cell.move(self)   # Motor stage
        return


class TrailMap:
    def __init__(self, size):
        self.size = np.array(size)
        self.grid = np.zeros(self.size)

        self.alpha = 0.93
        self.sigma = 1.1

    def diffuse(self, dm):
        self.grid = self.grid + dm.grid
        self.grid = self.alpha * scipy.ndimage.filters.gaussian_filter(self.grid, self.sigma)

