import numpy as np
import h5py
import matplotlib.pyplot as plt


def parse_episode_scores(move_history):
    """Find a list of scores of each episode.

    This is currently very hacky because move_history contains many rollouts
    in a dimension of the array. A better solution would be to divide rollouts.
    But this makes (slightly) more of a change in converting between
    move_history_lists and a single array (which is good for supplying to
    model).

    Use the fact that the return will always decrease throughout a rollout.
    """
    episode_returns = []
    episode_start_indeces = []

    current_score = np.inf
    for i in range(move_history.shape[0]):
        score = move_history['return'][i]
        if score > current_score:
            episode_returns.append(score)
            episode_start_indeces.append(i)
        current_score = score

    return episode_start_indeces, episode_returns

if __name__ == '__main__':
    filename = 'episodes.hdf5'
    policy_name = 'random_policy'

    f = h5py.File(filename, 'r')
    move_history = np.array(f[policy_name])
    _, episode_returns = parse_episode_scores(move_history)

    print('Episodes parsed: ', len(episode_returns))

    plt.hist(episode_returns)
    plt.title('Episode Scores')
    plt.xlabel('Scores')
    plt.ylabel('Num episodes')

    plt.show()
