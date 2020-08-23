from maps import DataMap
import matplotlib.pyplot as plt
import numpy as np
import skimage.measure
from tqdm import tqdm
from helpers import VideoWriter, VideoWriterIo


save_video = 0
show_entropy = 0

sz = (200, 260)
dm = DataMap(sz)

dm.generate_cell_species(400)
#dm.generate_cell_species(400)
#dm.generate_cell_species(400)

simulation_length = 150
fps = 60


dm.deposit_species_trail()
entropy = np.zeros(simulation_length)

plt.figure()

fig = plt.imshow(dm.img())

plt.gca().set_axis_off()
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
plt.margins(0, 0)


wr = VideoWriterIo(save_video, fps)


for i in tqdm(range(simulation_length)):

    dm.species_activity()
    dm.deposit_species_trail()

    fig.set_array(dm.img())
    entropy[i] = skimage.measure.shannon_entropy(dm.grid)
    plt.pause(0.01)
    wr.get_frame()

wr.close()

if show_entropy:
    plt.show()
    plt.figure()
    plt.plot(entropy)
    plt.title("Entropy of system over time")
    plt.ylabel("Shannon entropy")
    plt.xlabel("Iteration")
