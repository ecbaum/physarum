import numpy as np
import matplotlib.pyplot as plt
from species import Species


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

    def generate_species(self, cell_amount):
        if len(self.species) >= 3:
            raise Exception("Color map currently only support up to three species")

        spc = Species(self.size)
        spc.generate_cells(cell_amount)
        self.species.append(spc)
        self.deposit_species_trail()

    def deposit_species_trail(self):
        #  Clear Trail sum
        self.trail_sum = np.zeros(self.size)

        for spc in self.species:
            spc.deposit()
            self.trail_sum += spc.trail.grid  # sum all trails

    def species_activity(self):
        for spc in self.species:
            spc.activate(self)
        self.deposit_species_trail()
