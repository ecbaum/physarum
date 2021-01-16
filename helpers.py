import cv2
import os
import imageio
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from pathlib import Path
import skimage.measure
from scipy.ndimage import gaussian_filter


class DisplayEnvironment:
    def __init__(self, env):
        self.env = env
        self.color_bias = [0, 0.45, 0.6]
        self.color_maps = {0: 'Greens', 1: 'Reds', 2: 'Blues'}
        self.color_intensity = [5, 5, 5]
        self.overlay_nutrients = 0

        self.fig = plt.imshow(self.env.scent_trails[0])

        plt.gca().set_axis_off()
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0, 0)

    def pos_img(self):
        img = np.zeros(np.hstack((self.env.size, 4)))
        n = len(self.env.species)
        for i in range(n):
            c_map = plt.get_cmap(self.color_maps[i])
            img = img + c_map(self.color_intensity[i] * self.env.scent_trails[i]) - self.color_bias[n-1]
        img[np.where(img > 1)] = 1
        img[np.where(img < 0)] = 0
        return img

    def nutr_img(self):
        img = np.zeros(self.env.size)
        for i in range(self.env.size[0]):
            for j in range(self.env.size[1]):
                for cell in self.env.data_map[i][j]:
                    img[i, j] += cell.nutrient
        c_map = plt.get_cmap('gist_stern')
        return c_map(img)

    #def img(self):
        #if self.overlay_nutrients:
            #img = 0.5*self.pos_img() + 0.5*gaussian_filter(self.nutr_img(), 0.5)
        #else:
            #img = self.env.scent_trails[0].copy()
            #for i in range(self.env.size[0]):
                #for j in range(self.env.size[1]):
                    #if self.env.occupation_maps[0][i, j] == 1:
                        #img[i, j] = 1

        #return self.env.scent_trails[0]

    def update(self):
        c_map1 = plt.get_cmap('viridis')
        c_map2 = plt.get_cmap('Reds')

        img1 = gaussian_filter(self.env.scent_trails[0],1)
        img2 = np.zeros(self.env.size)

        for i in range(self.env.size[0]):
            for j in range(self.env.size[1]):
                for cell in self.env.data_map[i][j]:
                    img2[i, j] += 100*cell.nutrient
        cmap_img2 = c_map2(img2)
        img = c_map1(img1)

        for i in range(self.env.size[0]):
            for j in range(self.env.size[1]):
                if img2[i, j] > 0.02:
                    for k in range(4):
                        img[i, j, k] = cmap_img2[i, j, k]

        self.fig.set_array(img)
        plt.pause(0.01)
        return


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
