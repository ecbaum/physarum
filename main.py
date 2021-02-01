from helpers import VideoWriter, DataLogger, DisplayEnvironment
from physical_environment import Environment
from organism import CellSpecies, Nutrient
import numpy as np
from tqdm import tqdm

# Simulation settings
save_video = 0
show_entropy = 0
fps = 60

simulation_length = 1000
simulate_nutrients = 1
env_width = 100
env_aspect_ratio = 4/3

# Species settings
organism_list = [CellSpecies(cell_amount=1000,
                             scent_decay=0.8,
                             scent_sigma=0.3,
                             sensor_distance=3,
                             sensor_angle=np.radians(70),
                             sensor_width=1),

                 Nutrient(cell_amount=2,
                          scent_decay=0.9,
                          scent_sigma=6)]


env = Environment(width=env_width,
                  aspect_ratio=env_aspect_ratio,
                  organism_list=organism_list,
                  sim_nutr=simulate_nutrients)

display = DisplayEnvironment(env)
writer = VideoWriter(save_video, fps)
logger = DataLogger(env, simulation_length, show_entropy)


with writer, logger:
    for i in tqdm(range(simulation_length)):
        env.simulate()
        display.update()
        writer.get_frame()
        logger.log()
        tqdm.write(f"output: {env.organism[1].cells[0].nutrient}, level: {env.organism[1].cells[0].nutrient_level}")

