from maps import DataMap
import matplotlib.pyplot as plt
import numpy as np
import skimage.measure
from tqdm import tqdm
from helpers import VideoWriter, VideoWriterIo


save_video = 1

sz = (200, 260)
dm = DataMap(sz)

dm.generate_cell_species(800)
dm.generate_cell_species(800)

simulation_length = 6


dm.deposit_species_trail()
entropy = np.zeros(simulation_length)

plt.figure()

fig = plt.imshow(dm.img())

plt.gca().set_axis_off()
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
plt.margins(0, 0)


wr = VideoWriterIo(save_video)


for i in tqdm(range(simulation_length)):

    dm.species_activity()
    dm.deposit_species_trail()

    fig.set_array(dm.img())
    entropy[i] = skimage.measure.shannon_entropy(dm.grid)
    plt.pause(0.01)
    wr.get_frame()

wr.close()

plt.show()
plt.figure()
plt.plot(entropy)
plt.title("Entropy of system over time")
plt.ylabel("Shannon entropy")
plt.xlabel("Iteration")
