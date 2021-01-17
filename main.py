from helpers import VideoWriter, DataRecorder, DisplayEnvironment
from physical_environment import Environment
from species import Species, Nutrient
import numpy as np
from tqdm import tqdm

# Simulation settings
save_video = 0
show_entropy = 0

simulation_length = 300
fps = 60

# Enviroment settings
simulate_nutrients = 1
env_width = 100
env_size = (env_width, int(4/3*env_width))

env = Environment(env_size, simulate_nutrients)

# Species settings
species_list = [Species(env, 400,
                        scent_decay=0.8,
                        scent_sigma=0.4,
                        sensor_distance=3,
                        sensor_angle=np.radians(70),
                        sensor_width=1),
                Nutrient(env, 10, 0.95, 2)]


env.generate_species(species_list)
#nutr = Nutrient(env,10,0.5,0.5)
#env.generate_nutrients(nutr)
display = DisplayEnvironment(env)
writer = VideoWriter(save_video, fps)
recorder = DataRecorder(env, simulation_length, show_entropy)

for i in tqdm(range(simulation_length)):
    #if i == 1:
    #    env.species[0].cells[0].nutrient = 1.3
    env.species_activity()
    display.update()
    writer.get_frame()
    recorder.log()

writer.close()
recorder.plot()
