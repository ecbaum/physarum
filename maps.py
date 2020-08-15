import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt

class DataMap:
    def __init__(self, size):
        self.size = np.array(size)
        self.grid = np.zeros(self.size, dtype=int)
        self.cells = []

    def generate_cells(self, amount):
        # Allocate for amount
        i = 0
        for k in range(amount):
            for tries in range(30):
                pos = self.size*np.random.rand(2)
                if self.grid[tuple(pos.astype(int))] == 0:
                    self.grid[tuple(pos.astype(int))] = 1
                    i += 1
                    # Generate cell at pos at index i
                    break
        # Truncate to i
        print("Generated " + str(i) + "/" + str(amount) + " cells")
        return

    def observe(self, tm):
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


sz = (50, 50)

dm = DataMap(sz)
dm.generate_cells(200)
tm = TrailMap(sz)

tm.diffuse(dm)

plt.imshow(tm.grid)
plt.show()
