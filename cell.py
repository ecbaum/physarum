import numpy as np
from helpers import valid, grid_id


class Cell:
    def __init__(self, pos, spc_id):
        # positional data
        self.pos = pos
        self.id = spc_id
        self.angle = np.random.rand(1)*2*np.pi
        self.nutrient = 0

        # sensor placement data
        self.sensor_distance = 8
        self.sensor_angle = np.pi/8
        self.sensor_width = 2
        self.sensor_data = np.zeros(3)

    def sensor_pos(self):
        angles = np.array([[self.angle],                            # Front
                           [self.angle + self.sensor_angle],        # Left
                           [self.angle - self.sensor_angle]])       # Right

        x = self.pos[0] + self.sensor_distance*np.cos(angles)
        y = self.pos[1] + self.sensor_distance*np.sin(angles)

        return np.hstack((x, y))

    def observe(self, grid):
        sensor_data = np.zeros(3)  # [front, left, right] measurement
        sensor_positions = self.sensor_pos()

        for i in range(3):
            if valid(sensor_positions[i, :], grid):
                sensor_data[i] += grid[grid_id(sensor_positions[i, :])]

        self.sensor_data = sensor_data

    def decide(self):

        front, left, right = self.sensor_data

        if front > left and front > right:
            rotation = 0
        elif front < left and front < right:
            rotation = 2
        elif left < right:
            rotation = -1
        elif right < left:
            rotation = 1
        else:
            rotation = 2

        return rotation * np.pi

    def move(self, env):
        self.angle += np.random.rand(1) * self.decide()
        self.angle = np.mod(self.angle, 2 * np.pi)

        next_pos = self.pos + np.hstack((np.cos(self.angle), np.sin(self.angle)))

        if env.valid(next_pos):
            env.move(self, self.pos, next_pos)
            self.pos = next_pos
