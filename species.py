import numpy as np
from cell import Cell, NutrientSource
from scipy.ndimage import gaussian_filter
from helpers import timer


class Species:
    def __init__(self, cell_amount,
                 scent_decay=5,
                 scent_sigma=0.8,
                 sensor_distance=3,
                 sensor_angle=np.pi/3,
                 sensor_width=2):

        self.env = None
        self.scent_decay = scent_decay
        self.scent_sigma = scent_sigma
        self.amount = cell_amount
        self.cells = np.empty(cell_amount, dtype=Cell)
        self.cell_settings = [sensor_distance, sensor_angle, sensor_width]
        self.id = -1

    def generate(self):
        r = self.env.size[0] / 2 * 0.8
        c = self.env.size / 2
        i = 0
        for k in range(self.amount):
            for tries in range(30):
                pos = self.env.size * np.random.rand(2)
                if np.linalg.norm(c-pos) < r:
                    cell = Cell(pos, self.id, self.cell_settings)
                    self.cells[i] = cell
                    cell_grid_pos = self.env.grid_pos(pos)
                    self.env.data_map[cell_grid_pos[0]][cell_grid_pos[1]].append(cell)
                    i += 1
                    break

    def scent_trail(self, previous_scent_trail):
        occupation_map = np.zeros(self.env.size)
        for cell in self.cells:
            occupation_map[self.env.grid_pos(cell.pos)] = 1
        self.env.occupation_maps[self.id] = occupation_map

        scent_addition = gaussian_filter(occupation_map, self.scent_sigma)
        previous_scent = gaussian_filter(previous_scent_trail, self.env.sigma)

        return scent_addition + self.scent_decay * previous_scent

    def activate(self):
        known_scent = self.env.scent_trails[self.id]
        unknown_scent = np.zeros(self.env.size)

        for spc_id, spc in enumerate(self.env.species):  # This can be made more efficient by introducing a trailsum in env
            if type(spc) == Nutrient:
                known_scent += self.env.scent_trails[spc_id]
            elif spc_id is not self.id:
                unknown_scent += self.env.scent_trails[spc_id]

        for cell in self.cells:
            cell.observe(known_scent - unknown_scent)  # Sense trail of species
            cell.move(self.env)

    def diffuse_nutrients(self):
        dr = 1  # diffusion radius

        for i in range(self.env.size[0]):
            for j in range(self.env.size[1]):
                neighbouring_cell = list()

                for ii in range(-dr+1, dr+1):
                    for jj in range(-dr+1, dr+1):
                        x_pos = ii + i
                        y_pos = jj + j

                        if self.env.valid([x_pos, y_pos]):
                            for cell in self.env.data_map[x_pos][y_pos]:
                                if cell.id == self.id or type(cell) == NutrientSource:
                                    neighbouring_cell.append(cell)

                n = len(neighbouring_cell)

                nutrient_sum = 0
                for k in range(n):
                    if type(neighbouring_cell[k]) == NutrientSource:
                        nutrient_sum += neighbouring_cell[k].extract_nutrient()
                    else:
                        nutrient_sum += neighbouring_cell[k].nutrient

                for k in range(n):
                    if type(neighbouring_cell[k]) != Nutrient:
                        neighbouring_cell[k].nutrient = nutrient_sum/n


class Nutrient:
    def __init__(self, cell_amount, scent_decay, scent_sigma):
        self.env = None
        self.amount = cell_amount
        self.pos = None
        self.scent_decay = scent_decay
        self.scent_sigma = scent_sigma
        self.cells = np.empty(cell_amount, dtype=NutrientSource)
        self.display_factor = 5
        self.id = -1

    def generate(self):
        for k in range(self.amount):
            self.pos = self.env.size * np.random.rand(2)
            source = NutrientSource(self.pos)
            self.cells[k] = source

            source_grid_pos = self.env.grid_pos(self.pos)
            self.env.data_map[source_grid_pos[0]][source_grid_pos[1]].append(source)

    def scent_trail(self, previous_scent_trail):
        occupation_map = np.zeros(self.env.size)
        for cell in self.cells:
            occupation_map[self.env.grid_pos(cell.pos)] = cell.nutrient/self.display_factor
        self.env.occupation_maps[self.id] = occupation_map

        scent_addition = gaussian_filter(occupation_map, self.scent_sigma)
        previous_scent = gaussian_filter(previous_scent_trail, self.env.sigma)

        return scent_addition + self.scent_decay * previous_scent

