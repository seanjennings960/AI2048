import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
from episode_generator import EpisodeGenerator
from Policy import RandomPolicy
from state_vector import log_state_vector
from returns import sum_cumulative_returns

episode_generator = EpisodeGenerator()
policy = RandomPolicy()
num_trials = 100
cutoff_values = np.array([1, 8, 32, 128, 2048])
state_shape = (4, 4, len(cutoff_values) - 1)
new_state_shape = (np.prod(state_shape),)

model = Sequential([
    Dense(32, input_shape=new_state_shape, activation='sigmoid'),
    Dense(1),
    Activation('linear')
    ])

model.compile(optimizer='rmsprop',
              loss='mse')

print('Generating Episodes...')
move_history = episode_generator.play_policy_multi(policy, num_trials)
state_vector = log_state_vector(move_history['after_state'], cutoff_values)
returns = sum_cumulative_returns(move_history)
print('Number of moves: ', move_history.shape[0])

print('Fitting model')

history = model.fit(state_vector, returns, epochs=5)
