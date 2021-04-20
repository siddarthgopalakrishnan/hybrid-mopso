import numpy as np
from jmetal.util.solution import get_non_dominated_solutions
from jmetal.lab.visualization.plotting import Plot
from jmetal.algorithm.multiobjective.smpso import SMPSO
from jmetal.operator import PolynomialMutation
from jmetal.util.archive import CrowdingDistanceArchive
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.problem import ZDT1, Tanaka
from jmetal.problem.multiobjective.constrained import Osyczka2, Binh2


def solve_problem(problem):

    mutation_probability = 1.0 / problem.number_of_variables
    max_evaluations = 15000
    swarm_size = 100

    algorithm = SMPSO(
        problem=problem,
        swarm_size=swarm_size,
        mutation=PolynomialMutation(
            mutation_probability, distribution_index=20),
        leaders=CrowdingDistanceArchive(100),
        termination_criterion=StoppingByEvaluations(max_evaluations)
    )

    algorithm.run()
    solutions = algorithm.get_result()
    front = get_non_dominated_solutions(solutions)
    # plot_front = Plot(title='Pareto front approximation',
    #                   axis_labels=['x', 'y'])
    # plot_front.plot(front, label='SMPSO')

    print("Running time of SMPSO :", algorithm.total_computing_time, "s")
    getres = np.array(solutions)
    archive_pts = []
    archive_fitness = []
    for i in range(getres.shape[0]):
        archive_fitness.append(getattr(solutions[i], 'objectives'))
        archive_pts.append(getattr(solutions[i], 'variables'))

    archive_fitness = np.array(archive_fitness)
    archive_pts = np.array(archive_pts)

    np.savetxt("./coords/smpso_in.txt", archive_pts)
    np.savetxt("./coords/smpso_fit.txt", archive_fitness)

    # f = open("./smpso_in.txt", 'w')
    # for i in range(getres.shape[0]):
    #     mystr = (str(np.array(getattr(solutions[i], 'variables')))).strip(
    #         "[]")+"\n"
    #     f.write(mystr)
    # f.close()


def driver(funct):
    if funct == 1:
        problem = ZDT1()
    elif funct == 2:
        problem = Tanaka()
    elif funct == 3:
        problem = Osyczka2()
    else:
        problem = Binh2()
    solve_problem(problem)
