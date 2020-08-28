import matplotlib.pyplot as plt
from helpers import VideoWriterIo, EntropyRecorder
from data import DataMap
from tqdm import tqdm


save_video = 0
show_entropy = 0

sz = (100, 130)
dm = DataMap(sz)
simulation_length = 30
fps = 60

dm.generate_species(200)


dm.deposit_species_trail()

plt.figure()
fig = plt.imshow(dm.img())
plt.gca().set_axis_off()
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
plt.margins(0, 0)

wr = VideoWriterIo(save_video, fps)
er = EntropyRecorder(simulation_length, show_entropy)

for i in tqdm(range(simulation_length)):

    dm.species_activity()
    dm.deposit_species_trail()

    fig.set_array(dm.img())
    plt.pause(0.01)
    wr.get_frame()
    er.record(i, dm.grid)

wr.close()
er.plot()
