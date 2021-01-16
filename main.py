from helpers import VideoWriter, DataRecorder, DisplayEnvironment
from physical_environment import Environment
from species import Species
import numpy as np
from tqdm import tqdm

# Simulation settings
save_video = 0
show_entropy = 0

simulation_length = 100
fps = 60

# Enviroment settings
simulate_nutrients = 0
env_width = 30
env_size = (env_width, int(4/3*env_width))

env = Environment(env_size, simulate_nutrients)

# Species settings
species_list = [Species(env, cell_amount=15,
                        scent_decay=0.5,
                        scent_sigma=0.8,
                        sensor_distance=3,
                        sensor_angle=np.radians(60),
                        sensor_width=2)]


env.generate_species(species_list)
display = DisplayEnvironment(env)
writer = VideoWriter(save_video, fps)
recorder = DataRecorder(env, simulation_length, show_entropy)

for i in tqdm(range(simulation_length)):
    if i == 1:
        env.species[0].cells[0].nutrient = 1.3
    env.species_activity()
    display.update()
    writer.get_frame()
    recorder.log()

writer.close()
recorder.plot()
