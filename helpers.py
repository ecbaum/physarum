from pathlib import Path
import cv2
import matplotlib.pyplot as plt


class VideoWriter:
    def __init__(self, write_vid):
        self.writeVid = write_vid
        self.path = Path(Path.cwd(), 'temp.png')
        self.video = []

        if write_vid:
            plt.savefig(self.path)
            video_name = 'video.avi'
            frame = cv2.imread(str(self.path))
            height, width, layers = frame.shape
            self.video = cv2.VideoWriter(video_name, 0, 30, (width, height))

    def get_frame(self):
        if self.writeVid:
            plt.savefig(self.path)
            self.video.write(cv2.imread(str(self.path)))

    def close(self):
        if self.writeVid:
            cv2.destroyAllWindows()
            self.video.release()


def valid(pos, grid):
    return 0 <= pos[0] < grid.shape[0] and 0 < pos[1] < grid.shape[1]