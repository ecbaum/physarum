from helpers import VideoWriter, DataRecorder, DisplayEnvironment
from physical_environment import Environment
from tqdm import tqdm


save_video = 0
show_entropy = 0

env_size = (100, 133)
simulation_length = 500
fps = 60


env = Environment(env_size)
env.generate_species(1000)

display = DisplayEnvironment(env)
writer = VideoWriter(save_video, fps)
recorder = DataRecorder(env, simulation_length, show_entropy)

for i in tqdm(range(simulation_length)):

    env.species_activity()
    display.update()
    writer.get_frame()
    recorder.log()

writer.close()
recorder.plot()
