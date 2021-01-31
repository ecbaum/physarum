import numpy as np
from collections import deque
from species import Nutrient
from helpers import timer


class Environment:
    def __init__(self, width, aspect_ratio, species_list, sim_nutr):
        self.size = np.array((width, int(aspect_ratio*width)))
        self.sim_nutr = sim_nutr
        self.species = list()
        self.occupation_maps = list()
        self.scent_trails = list()
        self.sigma = 0.1

        # Creates a size[0] x size[1] list of empty deque()
        self.data_map = [list() + [deque() for _ in range(self.size[1])] for _ in range(self.size[0])]

        self.generate_species(species_list)

    def generate_species(self, species_list):
        if len(species_list) >= 3:
            raise Exception("Color map currently only support up to three species")

        for spc_id, spc in enumerate(species_list):
            spc.id = spc_id
            spc.env = self
            spc.generate()
            self.species.append(spc)
            self.scent_trails.append(np.zeros(self.size))
            self.occupation_maps.append(np.zeros(self.size))

    def generate_scent_trails(self):
        for spc_id in range(len(self.species)):
            self.scent_trails[spc_id] = self.species[spc_id].scent_trail(self.scent_trails[spc_id])

    def move(self, cell, pos_A, pos_B):
        grid_pos_a = self.grid_pos(pos_A)
        grid_pos_b = self.grid_pos(pos_B)
        if grid_pos_b[0] == pos_B[0] and grid_pos_b[1] == pos_B[1]:
            return
        self.data_map[grid_pos_a[0]][grid_pos_a[1]].remove(cell)
        self.data_map[grid_pos_b[0]][grid_pos_b[1]].append(cell)

    def simulate(self):
        self.generate_scent_trails()
        for spc in self.species:
            if type(spc) != Nutrient:
                spc.activate()
                if self.sim_nutr:
                    for i in range(2):
                        spc.diffuse_nutrients()

    def valid(self, pos):
        return 0 <= pos[0] < self.size[0] and 0 <= pos[1] < self.size[1]

    def grid_pos(self, pos):
        if self.valid(pos):
            return tuple(pos.astype(int))
        else:
            raise Exception(f"Position {pos} outside of grid of size {self.size}")
