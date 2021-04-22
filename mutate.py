import numpy as np
import update


def mutate_(i, cycle_, mu, in_, min_, max_):
    """
    Performs mutation operation to improve exploration of search space
    :param i: Current iteration
    :param cycle_: Total iterations
    :param mu: Mutation rate
    :param in_: Input swarm
    :param min_: Lower bounds for the particles
    :param max_: Upper bounds for the particles
    Returns mutated population and modified mutation rate
    """
    nVar = in_.shape[1]
    pmu = ((cycle_ - i) / (cycle_ - 1))**(5 / mu)
    for it in range(in_.shape[0]):
        if np.random.rand() > pmu:
            j = int(np.random.uniform(0, nVar-1))
            # difference of pm*VarBound
            dx = pmu*(max_[j] - min_[j])
            # lower bound = x - difference
            lb = in_[it, j]-dx
            if lb < min_[j]:
                lb = min_[j]
            # upper bound = x + difference
            ub = in_[it, j]+dx
            if ub > max_[j]:
                ub = max_[j]
            in_[it, j] = np.random.uniform(lb, ub)
    # Dampening factor
    mu = 0.99*mu
    return in_, mu
