import numpy as np
import init
import update
import plot
import time
import objectives
import mutate
from tqdm import tqdm


class Mopso:
    def __init__(self, particles, w, wdamp, c1, c2, max_, min_, thresh, funct, num_obj, mu, mesh_div=10):
        """
        Mopso object
        :param particles: Number of particles in swarm
        :param w: Inertia factor
        :param wdamp: Interia dampening factor
        :param c1: Local velocity factor
        :param c2: Global velocity factor
        :param max_: Upper bounds for the particles
        :param min_: Lower bounds for the particles
        :param thresh: External archive threshold
        :param funct: Test function number
        :param num_obj: Number of objective functions
        :param mu: Mutation rate
        :param mesh_div: Number of grid divisions
        :param cycle_: Iterations
        :param max_v: Upper velocity limit
        :param min_v: Lower velocity limit
        """
        self.w, self.wdamp, self.c1, self.c2 = w, wdamp, c1, c2
        self.funct = funct
        self.mesh_div = mesh_div
        self.mu = mu
        self.num_obj = num_obj
        self.particles = particles
        self.thresh = thresh
        self.max_ = max_
        self.min_ = min_
        self.trig = 0
        self.max_v = (max_-min_)*0.05
        self.min_v = (max_-min_)*(-0.05)
        self.plot_ = plot.Plot_pareto()

    def evaluation_fitness(self):
        """
        Evaluates fitness function for the input swarm
        """
        self.fitness_ = objectives.get_objective(
            "value", self.funct, self.num_obj, self.in_)

    def initialize(self):
        """
        Initializes Mopso object
        """
        # Init coords
        self.in_ = init.init_pos(self.particles, self.min_, self.max_)
        # Init particle velocity
        self.v_ = init.init_v(self.particles, self.min_v, self.max_v)
        # Calcuate fitness
        self.evaluation_fitness()
        # Init individual optimal
        self.in_p, self.fitness_p = self.in_, self.fitness_
        # Init external archive
        self.archive_in, self.archive_fitness = init.init_archive(
            self.in_, self.fitness_)
        # Init global optimal
        self.in_g, self.fitness_g = update.update_gbest(
            self.archive_in, self.archive_fitness, self.mesh_div, self.min_, self.max_, self.particles)

    def update_(self, i, cycle_):
        """
        Updates Mopso object after every iteration
        """
        # Mutation every 300 iterations with dampening
        if i % 300 == 0 and i > 0:
            self.in_, self.mu = mutate.mutate_(
                i, cycle_, self.mu, self.in_, self.min_, self.max_)
        # Update velocity
        self.v_ = update.update_v(self.v_, self.min_v, self.max_v,
                                  self.in_, self.in_p, self.in_g, self.w, self.c1, self.c2)
        # Update position
        self.in_ = update.update_in(self.in_, self.v_, self.min_, self.max_)
        # Evaluate fitness
        self.evaluation_fitness()
        # Update pBest
        self.in_p, self.fitness_p = update.update_pbest(
            self.in_, self.fitness_, self.in_p, self.fitness_p)
        # Update archive
        self.archive_in, self.archive_fitness = update.update_archive(
            i, self.in_, self.fitness_, self.archive_in, self.archive_fitness, self.thresh,
            self.mesh_div, self.min_, self.max_, self.funct)
        # Update gBest
        self.in_g, self.fitness_g = update.update_gbest(
            self.archive_in, self.archive_fitness, self.mesh_div, self.min_, self.max_, self.particles)

    def done(self, cycle_):
        """
        Returns the archive and fitness after completion of algo
        """
        self.initialize()
        st = time.time()
        for i in tqdm(range(cycle_), desc="MOPSO+ progress"):
            self.update_(i, cycle_)
            if i == (cycle_ - 1):
                print('\nRunning time of MOPSO+ :', np.round(
                    time.time() - st, 2), "s")
                self.plot_.show(self.fitness_, self.archive_fitness, i)
            # Dampening factor
            # self.w = self.w * self.wdamp
        return self.archive_in, self.archive_fitness
