from helpers import VideoWriter, DataRecorder, DisplayEnvironment
from environment import DataMap
from tqdm import tqdm


save_video = 0
show_entropy = 0

sz = (40, 60)
simulation_length = 500
fps = 60


env = DataMap(sz)
env.generate_species(60)

display = DisplayEnvironment(env.img())
writer = VideoWriter(save_video, fps)
recorder = DataRecorder(simulation_length, show_entropy)

for i in tqdm(range(simulation_length)):

    env.species_activity()

    display.update(env.img())
    writer.get_frame()
    recorder.log(i, env.grid)

writer.close()
recorder.plot()
