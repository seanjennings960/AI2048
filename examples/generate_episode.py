import numpy as np
import h5py
import time

from episode_generator import EpisodeGenerator, NewEpisodeGenerator
from Policy import RandomPolicy
from policy import NewRandomPolicy

episode_generator = EpisodeGenerator()
policy = RandomPolicy()

num_episodes = 1000

# start_time = time.time()
# move_history = episode_generator.play_policy_multi(policy, num_episodes)
# print('Old episode generator runtime: ', time.time() - start_time)

new_episode_generator = NewEpisodeGenerator(low_level='minimal')
new_policy = NewRandomPolicy()

start_time = time.time()
new_move_history = new_episode_generator.play_policy_multi(new_policy, num_episodes, verbose=True)
print('New episode generator runtime: ', time.time() - start_time)


write_to_file = False

# print('Board Score: ', board.score)
# print('Reward sum: ', np.sum(move_history['reward']))
# print('Number of moves: ', move_history.shape[0])
# print('Final board position:\n', move_history[-1]['after_state'])
# print('Returns of initial position: ', returns_array[0])
# print('Returns after final position: ', returns_array[-1])
# print('Returns calculated in move_history: ', move_history['return'][0],
#       move_history['return'][-1])

print(move_history.shape[0])
if write_to_file:
    f = h5py.File('episodes.hdf5', 'w')
    f.create_dataset('random_policy', data=move_history)
    f.close()
