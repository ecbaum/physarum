import numpy as np


class Cell:
    def __init__(self, pos):
        # positional data
        self.pos = pos
        self.angle = np.random.rand(1)*2*np.pi

        # sensor placement data
        self.sensor_distance = 8
        self.sensor_angle = np.pi/8

        self.sensor_data = np.zeros(3)

    def sensor_pos(self):
        angles = np.array([[self.angle],                            # Front
                           [self.angle + self.sensor_angle],        # Left
                           [self.angle - self.sensor_angle]])       # Right

        x = self.pos[0] + self.sensor_distance*np.cos(angles)
        y = self.pos[1] + self.sensor_distance*np.sin(angles)

        return np.hstack((x, y))

    def observe(self, tm):
        sensor_data = np.zeros(3)  # [front, left, right] measurement
        sensor_positions = self.sensor_pos()
        for i in range(3):
            pos = tuple(sensor_positions[i, :].astype(int))
            if tm.valid(pos):
                sensor_data[i] = tm.grid[pos]

        self.sensor_data = sensor_data

    def decide(self):

        front, left, right = self.sensor_data
        rotation = 2

        if front > left and front > right:
            rotation = 0
        elif front < left and front < right:
            rotation = 2
        elif left < right:
            rotation = -1
        elif right < left:
            rotation = 1

        return rotation

    def move(self, dm):

        self.angle += np.random.rand(1) * self.decide() * np.pi
        self.angle = np.mod(self.angle, 2 * np.pi)

        next_pos = self.pos + 1.1*np.hstack((np.cos(self.angle), np.sin(self.angle)))

        if dm.valid(next_pos):
            dm.grid[tuple(self.pos.astype(int))] = 0
            dm.grid[tuple(next_pos.astype(int))] = 1
            self.pos = next_pos
