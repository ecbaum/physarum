import numpy as np
from collections import deque
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
from species import Species


class Environment:
    def __init__(self, size):
        self.size = np.array(size)
        self.data_map = list()
        self.species = list()
        self.occupation_maps = list()
        self.scent_trails = list()

        for i in range(size[0]):
            _row = [deque() for j in range(size[1])]
            self.data_map.append(_row)

        self.color_bias = [0, 0.45, 0.6]
        self.color_maps = {0: 'Greens', 1: 'Reds', 2: 'Blues'}
        self.color_intensity = [5, 5, 5]

    def valid(self, pos):
        return 0 <= pos[0] < self.size[0] and 0 < pos[1] < self.size[1]

    def img(self):
        img = np.zeros(np.hstack((self.size, 4)))
        n = len(self.species)
        for i in range(n):
            c_map = plt.get_cmap(self.color_maps[i])
            img = img + c_map(self.color_intensity[i] * self.scent_trails[i]) - self.color_bias[n-1]
        img[np.where(img > 1)] = 1
        img[np.where(img < 0)] = 0
        return img

    def generate_species(self, cell_amount):
        if len(self.species) >= 3:
            raise Exception("Color map currently only support up to three species")

        spc_id = len(self.species) + 1
        spc = Species(self.size, spc_id)
        spc.generate_cells(cell_amount)
        self.species.append(spc)

    def generate_occupation_map(self):
        self.occupation_maps = list()
        for species_id in range(len(self.species)):
            occupation_map = np.zeros(self.size)
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    for cell in self.data_map[i][j]:
                        if cell.id == species_id:
                            occupation_map[i, j] = 1
                            break
            self.occupation_maps.append(occupation_map)

    def generate_scent_trails(self):
        self.generate_occupation_map()
        self.scent_trails = list()
        for species_id in range(len(self.species)):
            trail = 0.7 * gaussian_filter(self.occupation_maps[species_id], 1)
            self.scent_trails.append(trail)

    def move(self, cell, pos_A, pos_B):
        self.data_map[pos_A[0]][pos_A[1]].remove(cell)
        self.data_map[pos_B[0]][pos_B[1]].append(cell)
