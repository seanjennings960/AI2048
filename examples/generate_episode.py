import numpy as np

from episode_generator import EpisodeGenerator
from Policy import RandomPolicy
from returns import sum_cumulative_returns

episode_generator = EpisodeGenerator()
policy = RandomPolicy()

move_history = episode_generator.play_policy(policy)
returns_array = sum_cumulative_returns(move_history)

# print('Board Score: ', board.score)
print('Reward sum: ', np.sum(move_history['reward']))
print('Number of moves: ', move_history.shape[0])
print('Final board position:\n', move_history[-1]['after_state'])
print('Returns of initial position: ', returns_array[0])
print('Returns after final position: ', returns_array[-1])
