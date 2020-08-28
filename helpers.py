import cv2
import os
import imageio
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from pathlib import Path
import skimage.measure

class VideoWriterIo:
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


class VideoWriter:
    def __init__(self, write_vid, fps):
        self.write_vid = write_vid

        self.folder_path = Path(Path.cwd(), 'video_out')
        self.vid_path = Path(self.folder_path, 'sim_' + datetime.now().strftime("%d%m%Y%H%M%S") + '.mp4v')
        self.fig_path = Path(self.folder_path, 'temp.png')

        self.fps = fps
        self.video = []

        if write_vid:
            Path(self.folder_path).mkdir(exist_ok=True)
            plt.savefig(self.fig_path)

            frame = cv2.imread(str(self.fig_path))
            height, width, layers = frame.shape
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.video = cv2.VideoWriter(str(self.vid_path), fourcc, self.fps, (width, height))

    def get_frame(self):
        if self.write_vid:
            plt.savefig(self.fig_path)
            self.video.write(cv2.imread(str(self.fig_path)))

    def close(self):
        if self.write_vid:
            cv2.destroyAllWindows()
            self.video.release()
            os.remove(self.fig_path)


class EntropyRecorder:
    def __init__(self, simulation_length, run):
        self.entropy = np.zeros(simulation_length)
        self.run = run

    def record(self, i, grid):
        if self.run:
            self.entropy[i] = skimage.measure.shannon_entropy(grid)

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
