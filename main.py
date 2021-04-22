import numpy as np
import objectives
from mopso import *
import smpso
import nsga2_pymoo
import compare_pfs


def main():
    """
    Driver code
    :param w: Inertia factor
    :param wdamp: Interia dampening factor
    :param c1: Local velocity factor
    :param c2: Global velocity factor
    :param particles: Number of particles in swarm
    :param cycle_: Iterations
    :param mesh_div: Number of grid divisions
    :param thresh: External archive threshold
    :param funct: Test function number
    :param num_obj: Number of objective functions
    :param min_: Lower bounds for the particles
    :param max_: Upper bounds for the particles
    :param mu: Mutation rate
    :param pareto_in: Pareto coordinates
    :param pareto_fitness: Pareto fitness values
    """
    w = 0.4
    wdamp = 0.99
    c1 = 2
    c2 = 2
    particles = 200
    cycle_ = 15000
    mesh_div = 10
    thresh = 100

    funct = int(input("1-ZDT2 | 2-Tanaka | 3-Osyczka | 4-Binh: "))
    if funct == 1:
        cycle_ = 8000
    num_obj = 2
    bounds = objectives.get_objective(
        flag="init", funct=funct, num_obj=num_obj, Input=particles)
    min_ = bounds[0]
    max_ = bounds[1]

    mu = 0.6

    # MOPSO instantiation
    mopso_ = Mopso(particles, w, wdamp, c1, c2, max_, min_,
                   thresh, funct, num_obj, mu, mesh_div)
    pareto_in, pareto_fitness = mopso_.done(
        cycle_)

    # Saving coordinates of pareto boundary
    np.savetxt("./coords/mopso_in.txt", pareto_in)
    # Saving fitness value of pareto boundary
    np.savetxt("./coords/mopso_fit.txt", pareto_fitness)

    # Call SMPSO and NSGA2 function
    smpso.driver(funct)
    nsga2_pymoo.driver(funct)

    # Call comapre_pfs function
    compare_pfs._compare_funcs(funct, min_, max_)


if __name__ == "__main__":
    main()
