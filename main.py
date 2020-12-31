from helpers import VideoWriter, DataRecorder, DisplayEnvironment
from physical_environment import Environment
import numpy as np
from tqdm import tqdm


save_video = 0
show_entropy = 0
simulate_nutrients = 1
display_nutrients = 0

env_size = (100, 130)
simulation_length = 500
fps = 60

decay = 0.5
sigma = 0.8

sensor_distance = 3
sensor_angle = np.pi / 3
sensor_width = 2

env = Environment(env_size)
env.settings([decay, sigma], [sensor_distance, sensor_angle, sensor_width])

env.generate_species([1000])

env.simulate_nutrients = simulate_nutrients

env.species[0].cells[0].nutrient = 1


display = DisplayEnvironment(env)
display.overlay_nutrients = display_nutrients
writer = VideoWriter(save_video, fps)
recorder = DataRecorder(env, simulation_length, show_entropy)

for i in tqdm(range(simulation_length)):

    env.species_activity()
    display.update()
    writer.get_frame()
    recorder.log()

writer.close()
recorder.plot()
