import numpy as np
import objectives

# Take delta input from user
delta = 0.6


def hybridize_(archive_in, min_, max_):
    """
    Augment our archive to explore locally and improve search capabilities.
    For each dimension we perform x_i = x_i +/- delta_x_i
    For large input dimensions, we can choose dimensions to hybridize on probability
    :param archive_in: Current archive set
    :param min_: Lower bounds for the particles
    :param max_: Upper bounds for the particles
    Returns augmented population
    """
    temparch = archive_in
    combined_pop = archive_in
    rand_hyb = (archive_in.shape[1] >= 6)
    for i in range(archive_in.shape[1]):
        if rand_hyb and np.random.rand() > 0.5:
            continue
        temparch[:, i] = temparch[:, i] - delta
        temparch[(temparch[:, i] < min_[i]), i] = min_[i]
        combined_pop = np.vstack((combined_pop, temparch))
        temparch[:, i] = temparch[:, i] + 2*delta
        temparch[(temparch[:, i] > max_[i]), i] = max_[i]
        combined_pop = np.vstack((combined_pop, temparch))
    return combined_pop
