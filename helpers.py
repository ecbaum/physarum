import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
import cv2
import os


class VideoWriter:
    def __init__(self, write_vid):
        self.writeVid = write_vid

        self.folder_path = Path(Path.cwd(), 'video_out')
        self.vid_path = Path(self.folder_path, 'sim_' + datetime.now().strftime("%d%m%Y%H%M%S") + '.mp4v')
        self.fig_path = Path(self.folder_path, 'temp.png')

        self.video = []

        if write_vid:
            Path(self.folder_path).mkdir(exist_ok=True)
            plt.savefig(self.fig_path)

            frame = cv2.imread(str(self.fig_path))
            height, width, layers = frame.shape
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.video = cv2.VideoWriter(str(self.vid_path), fourcc, 90, (width, height))

    def get_frame(self):
        if self.writeVid:
            plt.savefig(self.fig_path)
            self.video.write(cv2.imread(str(self.fig_path)))

    def close(self):
        if self.writeVid:
            cv2.destroyAllWindows()
            self.video.release()
            os.remove(self.fig_path)


def valid(pos, grid):
    return 0 <= pos[0] < grid.shape[0] and 0 < pos[1] < grid.shape[1]