import numpy as np
import os
import matplotlib.pyplot as plt
from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_problem
from pymoo.optimize import minimize


def solve_problem(problem):
    algorithm = NSGA2(pop_size=100)

    res = minimize(problem, algorithm, ('n_gen', 200), seed=1, verbose=False)
    print("Running time of NSGA2 :", res.exec_time, "s")
    np.savetxt("./coords/nsga2_in.txt", res.X)
    np.savetxt("./coords/nsga2_fit.txt", res.F)

    plt.title('NSGA2_Front')
    plt.xlabel('fitness_y1')
    plt.ylabel('fitness_y2')
    plt.scatter(res.F[:, 0], res.F[:, 1], s=30, c='red', marker=".", alpha=1.0)

    plt.savefig('./imgs/NSGA2_Front.png')
    plt.close()


def driver(funct):
    if funct == 1:
        problem = get_problem("zdt1")
    elif funct == 2:
        problem = get_problem("tnk")
    elif funct == 3:
        problem = get_problem("osy")
    else:
        problem = get_problem("bnh")
    solve_problem(problem)
