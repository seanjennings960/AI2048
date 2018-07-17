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

model = Sequential([
    Dense(32, input_shape=state_shape, activation='sigmoid'),
    Dense(4, activation='relu'),
    Dense(1),
    Activation('linear')
    ])

model.compile(optimizer='rmsprop',
              loss='mse')

for num_trial in range(num_trials):
    move_history = episode_generator.play_policy(policy)
    state_vectors = log_state_vector(move_history['after_state'], cutoff_values)
    returns = sum_cumulative_returns(move_history)
    trial_loss = model.train_on_batch(state_vectors, returns)
    print('Trial: {} | Loss: {}'.format(num_trial, trail_loss))

test_episode = episode_generator.play_policy(policy)
state_vectors = log_state_vector(move_history['after_state'], cutoff_values)
returns = sum_cumulative_returns(move_history)
trial_loss = model.test_on_batch(state_vectors, returns)
print('Test Trial Loss: {}'.format(num_trial, trail_loss))
