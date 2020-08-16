from maps import DataMap
import matplotlib.pyplot as plt
import numpy as np
import skimage.measure


sz = (250, 250)
dm = DataMap(sz)

dm.generate_cell_species(1000)
dm.generate_cell_species(1000)


simulation_length = 2000


dm.deposit_species_trail()
fig = plt.imshow(dm.img())
entropy = np.zeros(simulation_length)

for i in range(simulation_length):
    dm.species_activity()
    dm.deposit_species_trail()
    fig.set_array(dm.img())
    entropy[i] = skimage.measure.shannon_entropy(dm.grid)
    plt.pause(0.05)

plt.show()
plt.figure()
plt.plot(entropy)
plt.title("Entropy of system over time")
plt.ylabel("Shannon entropy")
plt.xlabel("Iteration")