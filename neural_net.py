import numpy as np
import h5py
from keras.models import Sequential
from keras.layers import Dense, Activation
from episode_generator import EpisodeGenerator
from Policy import RandomPolicy
from state_vector import log_state_vector

load_from_hdf5 = True

if not load_from_hdf5:
    episode_generator = EpisodeGenerator()
    policy = RandomPolicy()
    num_trials = 100
    print('Generating Episodes...')
    move_history = episode_generator.play_policy_multi(policy, num_trials)
else:
    f = h5py.File('episodes.hdf5')
    move_history = f['random_policy']


cutoff_values = np.array([1, 8, 32, 128, 2048])
state_shape = (16 * (len(cutoff_values) - 1),)

model = Sequential([
    Dense(32, input_shape=state_shape),
    Dense(32, activation='sigmoid'),
    Dense(1)
    ])

model.compile(optimizer='rmsprop',
              loss='mse')

state_vector = log_state_vector(move_history['after_state'], cutoff_values)
returns = move_history['return']
print('Number of moves: ', move_history.shape[0])

print('Fitting model')

history = model.fit(state_vector, returns, validation_split=0.7, epochs=5)
import pdb; pdb.set_trace()
