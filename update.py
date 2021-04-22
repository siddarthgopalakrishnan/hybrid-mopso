import numpy as np
import random
import init
import nondomsort
import delete_entry
import constraints
import augment
import objectives


def update_v(v_, v_min, v_max, in_, in_pbest, in_gbest, w, c1, c2):
    """
    Update speed value
    """
    r1 = random.uniform(0, 1)
    r2 = random.uniform(0, 1)
    v_temp = w*v_ + r1*c1*(in_pbest-in_) + r2*c2*(in_gbest-in_)
    for i in range(v_temp.shape[0]):
        for j in range(v_temp.shape[1]):
            if v_temp[i, j] < v_min[j]:
                v_temp[i, j] = v_min[j]
            if v_temp[i, j] > v_max[j]:
                v_temp[i, j] = v_max[j]
    return v_temp


def update_in(in_, v_, in_min, in_max):
    """
    Update location parameters
    """
    in_temp = in_ + v_
    for i in range(in_temp.shape[0]):
        for j in range(in_temp.shape[1]):
            if in_temp[i, j] < in_min[j]:
                in_temp[i, j] = in_min[j]
            if in_temp[i, j] > in_max[j]:
                in_temp[i, j] = in_max[j]
    return in_temp


def update_pbest(in_, fitness_, in_pbest, out_pbest):
    """
    Update personal best of a particle
    """
    # Current, pBest
    temp = out_pbest - fitness_
    Dominate = np.int64(np.any(temp < 0, axis=1)) - \
        np.int64(np.any(temp > 0, axis=1))
    # Replace wherever fitness_ dominates
    remained_1 = Dominate == -1
    out_pbest[remained_1] = fitness_[remained_1]
    in_pbest[remained_1] = in_[remained_1]
    # Replace based on prob
    remained_2 = Dominate == 0
    remained_temp_rand = np.random.rand(len(Dominate),) < 0.5
    remained_final = remained_2 & remained_temp_rand
    out_pbest[remained_final] = fitness_[remained_final]
    in_pbest[remained_final] = in_[remained_final]
    return in_pbest, out_pbest


def update_archive(it, in_, fitness_, archive_in, archive_fitness, thresh, mesh_div, min_, max_, funct):
    """
    Calculate pareto boundary of current swarm and add boundary particles to archive
    Periodic Hybridization of the swarm to improve search capabilities
    Removing excess particles from the swarm based on crowding distance
    """
    combined_pop = np.vstack((archive_in, in_))
    total_Func = np.vstack((archive_fitness, fitness_))
    # Hybridization
    if it > 0 and it % 300 == 0:
        # Augment population
        archive_in = augment.hybridize_(archive_in, min_, max_)
        # Get new fitness values
        archive_fitness = objectives.get_objective(
            "value", funct, archive_fitness.shape[1], archive_in)
        combined_pop = np.vstack((combined_pop, archive_in))
        total_Func = np.vstack((total_Func, archive_fitness))

    # Removing outliers and bad solutions
    violations_ = constraints.constraints_(combined_pop, funct, min_, max_)
    first_tier_indices = nondomsort.nondomsort_(
        violations_, total_Func, combined_pop.shape[0])[0] == 1
    first_tier_indices = np.reshape(first_tier_indices, (-1,))
    archive_in = combined_pop[first_tier_indices]
    archive_fitness = total_Func[first_tier_indices]

    # Deleting elements
    if archive_in.shape[0] > thresh:
        removing = archive_in.shape[0] - thresh
        archive_in, archive_fitness = delete_entry.delete_entry_(
            archive_in, archive_fitness, removing, mesh_div)
    return archive_in, archive_fitness


def RouletteWheelSelection(N, Fitness):
    """
    Roulette wheel for grid selection
    Generate N random points
    See which grid number those N points lie in
    Return array of those grid numbers for each random point
    index is the above array
    """
    Fitness = np.reshape(Fitness, (-1,))  # reshape rows unkown
    # remove negative values
    Fitness = Fitness + np.minimum(np.min(Fitness), 0)
    Fitness = np.cumsum(1/Fitness)
    Fitness = Fitness/np.max(Fitness)
    index = np.sum(np.int64(~(np.random.rand(N, 1) < Fitness)), axis=1)
    return index


def update_gbest(archiving_in, archiving_fit, mesh_div, min_, max_, particles):
    """
    Update global best of the particles based on hypercube method
    """
    apop_size, _ = archiving_fit.shape
    # Calculate the grid location of each solution
    fmax = np.max(archiving_fit, axis=0)
    fmin = np.min(archiving_fit, axis=0)
    d = (fmax-fmin)/mesh_div
    fmin = np.tile(fmin, (apop_size, 1))
    d = np.tile(d, (apop_size, 1))
    grid_norm = np.floor((archiving_fit - fmin) / d)
    grid_norm[grid_norm >= mesh_div] = mesh_div-1
    grid_norm[np.isnan(grid_norm)] = 0
    # Detect the grid of each solution belongs to
    _, _, grid_site = np.unique(grid_norm, return_index=True,
                                return_inverse=True, axis=0)
    # which grid number will the objective space point (pair <f1,f2>) lie in
    # Calculate the crowd degree of each grid
    crowding = np.histogram(grid_site, np.max(grid_site)+1)[0]
    # Roulette-wheel 1/Fitnessselection
    TheGrid = RouletteWheelSelection(particles, crowding)
    # Grid numbers of N random points on the grid

    ReP = np.zeros(particles,)
    for i in range(particles):
        # where the randomly generated element from TheGrid, lies in our grid_site
        InGrid = np.where(grid_site == TheGrid[i])[0]
        Temp = np.random.randint(0, len(InGrid))
        ReP[i] = InGrid[Temp]
    ReP = np.int64(ReP)
    return archiving_in[ReP], archiving_fit[ReP]
