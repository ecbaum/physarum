from maps import DataMap, TrailMap
import matplotlib.pyplot as plt
import numpy as np
import skimage.measure

sz = (100, 133)
cells = 400
simulation_length = 2000

dm = DataMap(sz)
tm = TrailMap(sz)

dm.generate_cells(cells)
tm.diffuse(dm)

fig, (ax1, ax2) = plt.subplots(1, 2)
im1 = ax1.imshow(dm.grid)
im2 = ax2.imshow(tm.grid)

entropy = np.zeros(simulation_length)

for i in range(simulation_length):
    dm.cell_operation(tm)
    tm.diffuse(dm)
    im1.set_array(dm.grid)
    im2.set_array(tm.grid)

    entropy[i] = skimage.measure.shannon_entropy(dm.grid)

    plt.pause(0.01)

plt.show()

plt.figure()
plt.plot(entropy)
plt.title("Entropy of system over time")
plt.ylabel("Shannon entropy")
plt.xlabel("Iteration")
