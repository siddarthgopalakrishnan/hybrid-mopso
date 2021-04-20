import random
import numpy as np
import nondomsort


def init_pos(particles, in_min, in_max):
    """
    Initializes positions of particles randomly
    :param particles: Number of particles
    :param in_min: Lower bounds for the particles
    :param in_max: Upper bounds for the particles
    :variable in_dim: Dimension of input parameters
    Returns randomly generated population
    """
    in_dim = len(in_max)
    print('\nDecision space dimension:', in_dim)
    in_temp = np.random.uniform(
        0, 1, (particles, in_dim))*(in_max - in_min) + in_min
    return in_temp


def init_v(particles, v_max, v_min):
    """
    Initializes velocities of particles to zero
    :param particles: Number of particles
    :param v_max: Upper bounds of particle velocity
    :param v_min: Lower bounds of particle velocity
    :variable v_dim: Dimension of input parameters
    Returns zero velocities
    """
    v_dim = len(v_max)
    v_ = np.zeros((particles, v_dim))
    return v_


def init_archive(in_, fitness_):
    """
    Initializes archive
    :param in_: Input particles
    :param fitness_: Particle fitness
    Returns an archive of the best particles
    """
    first_tier_indices = nondomsort.nondomsort_(
        in_, fitness_, in_.shape[0])[0] == 1
    first_tier_indices = np.reshape(first_tier_indices, (-1,))
    curr_archiving_in = in_[first_tier_indices]
    curr_archiving_fit = fitness_[first_tier_indices]
    return curr_archiving_in, curr_archiving_fit
