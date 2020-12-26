from helpers import VideoWriter, DataRecorder, DisplayEnvironment
from physical_environment import Environment
from tqdm import tqdm


save_video = 0
show_entropy = 0
simulate_nutrients = 1
display_nutrients = 1

env_size = (220, 360)
simulation_length = 500
fps = 60


env = Environment(env_size)
env.generate_species(1000)

env.simulate_nutrients = simulate_nutrients

env.species[0].cells[0].nutrient = 100
env.species[0].cells[1].nutrient = 100


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
