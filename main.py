from maps import DataMap, TrailMap
import matplotlib.pyplot as plt

sz = (100, 133)
cells = 400

dm = DataMap(sz)
tm = TrailMap(sz)

dm.generate_cells(cells)
tm.diffuse(dm)

fig, (ax1, ax2) = plt.subplots(1, 2)
im1 = ax1.imshow(dm.grid)
im2 = ax2.imshow(tm.grid)

for i in range(1000):
    dm.cell_operation(tm)
    tm.diffuse(dm)
    im1.set_array(dm.grid)
    im2.set_array(tm.grid)
    plt.pause(0.01)

plt.show()
