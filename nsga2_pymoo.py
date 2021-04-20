import numpy as np
from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_problem
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter


def solve_problem(problem):
    algorithm = NSGA2(pop_size=100)

    res = minimize(problem, algorithm, ('n_gen', 200), seed=1, verbose=False)
    print("Running time of NSGA2 :", res.exec_time, "s")
    np.savetxt("./coords/nsga2_in.txt", res.X)
    np.savetxt("./coords/nsga2_fit.txt", res.F)

    # plot = Scatter()
    # plot.add(problem.pareto_front(), plot_type="line",
    #          color="black", alpha=0.7)
    # plot.add(res.F, color="red")

    # f = open("./nsga2_in.txt", 'w')
    # for line in res.X:
    #     mystr = (str(line)).strip("[]")+"\n"
    #     f.write(mystr)
    # f.close()
    # plot.show()


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
