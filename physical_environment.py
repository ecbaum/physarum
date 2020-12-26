import numpy as np
from collections import deque
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
from species import Species


class Environment:
    def __init__(self, size):
        self.size = np.array(size)
        self.data_map = list()
        self.scent_trails = list()
        self.species = list()

        for i in range(size[0]):
            _row = [deque() for j in range(size[1])]
            self.data_map.append(_row)

    def generate_occupation_map(self, species_id):
        occupation_map = np.zeros(self.size)
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                for cell in self.data_map[i][j]:
                    if cell.id == species_id:
                        occupation_map[i, j] = 1
                        break
        return occupation_map

    def generate_scent_trails(self):
        self.scent_trails = []
        for species_id in range(len(self.species)):
            occupation_map = self.generate_occupation_map(species_id)
            trail = 0.7 * gaussian_filter(occupation_map, 1)
            self.scent_trails.append(trail)

    def move(self, cell, pos_A, pos_B):
        self.data_map[pos_A[0]][pos_A[1]].remove(cell)
        self.data_map[pos_B[0]][pos_B[1]].append(cell)
