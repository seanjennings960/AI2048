import numpy as np
import h5py

from episode_generator import EpisodeGenerator
from Policy import RandomPolicy
from returns import sum_cumulative_returns

episode_generator = EpisodeGenerator()
policy = RandomPolicy()


num_episodes = 1000
move_history = episode_generator.play_policy_multi(policy, num_episodes)
write_to_file = True

print(move_history.shape[0])
if write_to_file:
    f = h5py.File('episodes.hdf5', 'w')
    f.create_dataset('random_policy', data=move_history)
    f.close()
