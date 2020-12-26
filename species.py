import numpy as np
from cell import Cell


class Species:
    def __init__(self, env, spc_id):
        self.cells = []
        self.amount = []
        self.id = spc_id
        self.env = env

    def generate_cells(self, amount):

        self.cells = np.empty(amount, dtype=Cell)  # Cells in species
        r = self.env.size[0] / 2 * 0.8
        c = self.env.size / 2
        i = 0
        for k in range(amount):
            for tries in range(30):
                pos = self.env.size * np.random.rand(2)
                if np.linalg.norm(c-pos) < r:
                    cell = Cell(pos, self.id)
                    self.cells[i] = cell

                    cell_grid_pos = self.env.grid_pos(pos)
                    self.env.data_map[cell_grid_pos[0]][cell_grid_pos[1]].append(cell)
                    i += 1
                    break

    def activate(self):
        known_scent = self.env.scent_trails[self.id]
        unknown_scent = np.zeros(self.env.size)

        for spc_id in range(len(self.env.species)):
            if spc_id is not self.id:
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
                                if cell.id == self.id:
                                    neighbouring_cell.append(cell)

                n = len(neighbouring_cell)

                nutrient_sum = 0
                for k in range(n):
                    nutrient_sum += neighbouring_cell[k].nutrient

                for k in range(n):
                    neighbouring_cell[k].nutrient = nutrient_sum/n
