import numpy as np
from maps import DataMap, TrailMap
from cell import Cell
import matplotlib.pyplot as plt
import time





sz = (50, 50)

dm = DataMap(sz)
tm = TrailMap(sz)

dm.generate_cells(200)
tm.diffuse(dm)

fig, (ax1, ax2) = plt.subplots(1, 2)

for i in range(100):
    dm.cell_operation(tm)
    tm.diffuse(dm)
    ax1.imshow(dm.grid)
    ax2.imshow(tm.grid)
    plt.pause(0.05)
plt.show()
#dm.cell_operation(tm)

#c = Cell(np.array([5, 5]))
#c.observe(tm)
#print(c.sensor_data)
#print(c.decide())
#c.view()
#print(np.degrees(c.angle))