from maps import DataMap
import matplotlib.pyplot as plt
import numpy as np
import skimage.measure
from tqdm import tqdm
from helpers import VideoWriter

# Settings #
save_video = 0

sz = (80, 80)
dm = DataMap(sz)

dm.generate_cell_species(100)
dm.generate_cell_species(100)

simulation_length = 200
# # # # # #

dm.deposit_species_trail()
fig = plt.imshow(dm.img())
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())

entropy = np.zeros(simulation_length)

wr = VideoWriter(save_video)

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
