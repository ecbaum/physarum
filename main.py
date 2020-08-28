from helpers import VideoWriterIo, EntropyRecorder, DisplayEnvironment
from data import DataMap
from tqdm import tqdm


save_video = 0
show_entropy = 0

sz = (100, 130)
simulation_length = 30
fps = 60

dm = DataMap(sz)
dm.generate_species(200)
dm.deposit_species_trail()

de = DisplayEnvironment(dm.img())
wr = VideoWriterIo(save_video, fps)
er = EntropyRecorder(simulation_length, show_entropy)

for i in tqdm(range(simulation_length)):

    dm.species_activity()
    dm.deposit_species_trail()

    de.update(dm.img())
    wr.get_frame()

    er.record(i, dm.grid)

wr.close()
er.plot()
