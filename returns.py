import numpy as np

def sum_cumulative_returns(move_history):
	returns_array = np.zeros(move_history.shape)
	cumulative_returns = 0
	for i in range(returns_array.shape[0] - 1, -1, -1):
		cumulative_returns += move_history[i]['reward']
		returns_array[i] = cumulative_returns

	return returns_array
