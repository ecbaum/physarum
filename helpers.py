import cv2
import os
import imageio
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from pathlib import Path
import skimage.measure


class DisplayEnvironment:
    def __init__(self, env):
        plt.figure()
        self.env = env
        self.color_bias = [0, 0.45, 0.6]
        self.color_maps = {0: 'Greens', 1: 'Reds', 2: 'Blues'}
        self.color_intensity = [5, 5, 5]
        self.fig = plt.imshow(self.img())

        plt.gca().set_axis_off()
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0, 0)

    def img(self):
        img = np.zeros(np.hstack((self.env.size, 4)))
        n = len(self.env.species)
        for i in range(n):
            c_map = plt.get_cmap(self.color_maps[i])
            img = img + c_map(self.color_intensity[i] * self.env.scent_trails[i]) - self.color_bias[n-1]
        img[np.where(img > 1)] = 1
        img[np.where(img < 0)] = 0
        return img

    def update(self):
        self.fig.set_array(self.img())
        plt.pause(0.01)


class VideoWriter:
    def __init__(self, write_vid, fps):
        self.write_vid = write_vid
        self.fps = fps

        self.folder_path = Path(Path.cwd(), 'video_out')
        self.vid_path = Path(self.folder_path, 'sim_' + datetime.now().strftime("%d%m%Y%H%M%S") + '.mp4')
        self.fig_path = Path(self.folder_path, 'temp.png')

        self.writer = []

        if write_vid:
            Path(self.folder_path).mkdir(exist_ok=True)
            plt.savefig(self.fig_path)

            self.writer = imageio.get_writer(self.vid_path, fps=self.fps)

    def get_frame(self):
        if self.write_vid:
            plt.savefig(self.fig_path)
            im = imageio.imread(str(self.fig_path))
            self.writer.append_data(im)

    def close(self):
        if self.write_vid:
            cv2.destroyAllWindows()
            self.writer.close()
            os.remove(self.fig_path)


class DataRecorder:
    def __init__(self, env, simulation_length, run):
        self.env = env
        self.entropy = np.zeros(simulation_length)
        self.run = run
        self.i = 0

    def log(self):
        grid = np.zeros(self.env.size)
        for j in range(len(self.env.occupation_maps)):
            grid += self.env.occupation_maps[j]
        grid[np.where(grid > 1)] = 1

        if self.run:
            self.entropy[self.i] = skimage.measure.shannon_entropy(grid)
            self.i += 1

    def plot(self):
        if self.run:
            plt.show()
            plt.figure()
            plt.plot(self.entropy)
            plt.title("Entropy of system over time")
            plt.ylabel("Shannon entropy")
            plt.xlabel("Iteration")


def valid(pos, grid):
    return 0 <= pos[0] < grid.shape[0] and 0 < pos[1] < grid.shape[1]


def grid_id(pos):
    return tuple(pos.astype(int))
