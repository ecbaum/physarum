import numpy as np


class Cell:
    def __init__(self, pos):
        # positional data
        self.pos = pos
        self.angle = np.random.rand(1)*2*np.pi

        # sensor placement data
        self.sensor_distance = 8
        self.sensor_angle = np.pi/8
        self.sensor_width = 2

        self.sensor_data_spc = np.zeros(3)
        self.sensor_data_aln = np.zeros(3)

    def sensor_pos(self):
        angles = np.array([[self.angle],                            # Front
                           [self.angle + self.sensor_angle],        # Left
                           [self.angle - self.sensor_angle]])       # Right

        x = self.pos[0] + self.sensor_distance*np.cos(angles)
        y = self.pos[1] + self.sensor_distance*np.sin(angles)

        return np.hstack((x, y))

    def observe(self, tm, within_spc):
        sensor_data = np.zeros(3)  # [front, left, right] measurement
        sensor_positions = self.sensor_pos()
        for i in range(3):

            c = tuple(sensor_positions[i, :].astype(int))
            w = self.sensor_width

            x_range = np.arange(int(c[0] - w / 2), (int(c[0] - w / 2) + w))
            y_range = np.arange(int(c[1] - w / 2), (int(c[1] - w / 2) + w))

            edge, measurement_sum = 0, 0
            for x in x_range:
                for y in y_range:
                    pos = tuple([x, y])
                    if tm.valid(pos):
                        measurement_sum += tm.grid[pos]
                    else:
                        edge = 1

            sensor_data[i] = measurement_sum/(w**2) if edge == 0 else 0

        if within_spc:
            self.sensor_data_spc = sensor_data
        else:
            self.sensor_data_aln = sensor_data

    def decide(self):

        front, left, right = self.sensor_data_spc - self.sensor_data_aln
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

    def move(self, dm, spc):

        self.angle += np.random.rand(1) * self.decide() * np.pi
        self.angle = np.mod(self.angle, 2 * np.pi)

        next_pos = self.pos + 1.1*np.hstack((np.cos(self.angle), np.sin(self.angle)))

        if dm.valid(next_pos):

            dm.grid[tuple(self.pos.astype(int))] = 0
            dm.grid[tuple(next_pos.astype(int))] = 1

            spc.grid[tuple(self.pos.astype(int))] = 0
            spc.grid[tuple(next_pos.astype(int))] = 1

            self.pos = next_pos
