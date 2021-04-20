import numpy as np

# Need to improve complexity of this function


def rad_sort(Matrix):
    """
    Performs a lexicographical sort on the fitness value columns
    :variable Matrix_temp: Holds reverse matrix
    :variable Matrix_row: Holds transpose matrix
    :variable rank: Corresponding indices after lexsort
    :variable Sorted_Matrix: Sorted matrix
    """
    Matrix_temp = Matrix[:, ::-1]  # Swap columns
    Matrix_row = Matrix_temp.T  # Transpose
    rank = np.lexsort(Matrix_row)  # Radix sort
    # rank holds the indices
    Sorted_Matrix = Matrix[rank, :]  # Sorted matrix
    return Sorted_Matrix, rank


def nondomsort_(violations_, fitness_, pop_size):
    """
    Peforms non-dominated sorting of fitness values
    Removes values which violate the given constraints
    Returns pareto levels of each particle
    :param violations_: Array of number of violations of each particle
    :param fitness_: Fitness values of particles
    :param pop_size: Population size
    :variable NDfront: Non-dominated front
    :variable pareto_level: 1 - best pareto level
    """
    # particles, num_of_objective functions
    N, M = fitness_.shape
    # non dominated front
    NDfront = np.inf * np.ones((1, N))
    pareto_level = 0
    # radix sort fitness values
    fitness_, rank = rad_sort(fitness_)
    # Check constraint violation
    violations = violations_[rank]
    # update non dominated front
    temp = np.sum(NDfront != np.inf)
    while(temp < pop_size):
        pareto_level += 1
        # for all fitness function value pairs
        for i in range(N):
            # print('i loop NDfront:', NDfront)
            if NDfront[0, i] == np.inf:
                dom_flag = False
                for j in range(i - 1, -1, -1):
                    # print('j loop NDfront:', NDfront)
                    if NDfront[0, j] == pareto_level:
                        if violations[i, 0] == True and violations[j, 0] == True:
                            m = 2
                            while (m <= M) and (fitness_[i, m-1] >= fitness_[j, m-1]):
                                m += 1
                            if m > M:
                                dom_flag = True
                            if dom_flag or (M == 2):
                                break
                        elif violations[i, 0] == False and violations[i, 1] > (M+1)//2:
                            NDfront[0, i] = -1
                            break
                        elif violations[j, 0] == False and violations[j, 1] > (M+1)//2:
                            NDfront[0, j] = -1
                            continue
                        elif violations[i, 0] == False and violations[j, 0] == False:
                            if violations[i, 1] > violations[j, 1]:
                                NDfront[0, i] = -1
                                break
                            else:
                                NDfront[0, j] = -1
                                continue
                        elif violations[i, 0] == True and violations[j, 0] == False:
                            NDfront[0, j] = -1
                            continue
                        elif violations[j, 0] == True and violations[i, 0] == False:
                            NDfront[0, i] = -1
                            break
                if not dom_flag:
                    NDfront[0, i] = pareto_level
        temp = np.sum(NDfront != np.inf)
    front_temp = np.zeros((1, N))
    front_temp[0, rank] = NDfront
    return front_temp, pareto_level
