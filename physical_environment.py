import numpy as np
from collections import deque
from scipy.ndimage import gaussian_filter
from species import Species


class Environment:
    def __init__(self, size, decay, sigma, simulate_nutrients):
        self.size = np.array(size)
        self.decay = decay
        self.sigma = sigma
        self.simulate_nutrients = simulate_nutrients

        self.data_map = list()
        self.species = list()
        self.occupation_maps = list()
        self.scent_trails = list()

        for i in range(size[0]):
            _row = [deque() for j in range(size[1])]
            self.data_map.append(_row)

    def generate_species(self, species_list):
        if len(species_list) >= 3:
            raise Exception("Color map currently only support up to three species")

        for spc_id in range(len(species_list)):
            spc = species_list[spc_id]
            spc.id = spc_id
            spc.generate_cells()
            self.species.append(spc)
            self.scent_trails.append(np.zeros(self.size))
        self.generate_occupation_map()

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

        for species_id in range(len(self.species)):
            trail = gaussian_filter(self.occupation_maps[species_id], self.sigma) + \
                    self.decay*self.scent_trails[species_id]
            self.scent_trails[species_id] = trail

    def move(self, cell, pos_A, pos_B):
        grid_pos_a = self.grid_pos(pos_A)
        grid_pos_b = self.grid_pos(pos_B)
        if grid_pos_b[0] == pos_B[0] and grid_pos_b[1] == pos_B[1]:
            return
        self.data_map[grid_pos_a[0]][grid_pos_a[1]].remove(cell)
        self.data_map[grid_pos_b[0]][grid_pos_b[1]].append(cell)

    def species_activity(self):
        self.generate_scent_trails()
        for spc in self.species:
            spc.activate()
            if self.simulate_nutrients:
                for i in range(2):
                    spc.diffuse_nutrients()

        #self.generate_scent_trails()

    def valid(self, pos):
        return 0 <= pos[0] < self.size[0] and 0 <= pos[1] < self.size[1]

    def grid_pos(self, pos):
        if self.valid(pos):
            return tuple(pos.astype(int))
        else:
            raise Exception("Position [" + str(pos[0]) + ", " + str(pos[1]) + "] outside of grid.")
