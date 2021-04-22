import numpy as np

# Need to improve complexity of this function
# Current complexity O(M*N^2)


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
    :variable pareto_level: pareto ranking of particle
    """
    # M always = 2 for 2 objective functions
    N, M = fitness_.shape
    # non dominated front
    NDfront = np.inf * np.ones((1, N))
    pareto_level = 1
    # radix sort fitness values
    fitness_, rank = rad_sort(fitness_)
    # Check constraint violation
    violations = violations_[rank]
    # O(M*N^2) loop
    for i in range(N):
        dom_flag = False
        # Skipping the particle if it violates constraints
        if violations[i, 0] == False:
            continue
        for j in range(i-1, -1, -1):
            if NDfront[0, j] == pareto_level:
                if violations[i, 0] and violations[j, 0]:
                    if fitness_[i, 1] >= fitness_[j, 1]:
                        # point i is more than point j
                        dom_flag = True
                    break
                # elif violations[i, 0] == False and violations[j, 0] == False:
                #     if violations[i, 1] > violations[j, 1]:
                #         NDfront[0, i] = -1
                #         break
                #     else:
                #         NDfront[0, j] = -1
                #         continue
                elif violations[i, 0]:
                    NDfront[0, j] = -1
                    continue
        if dom_flag == False:
            # First elements always has pareto_level 1
            NDfront[0, i] = pareto_level
    front_temp = np.zeros((1, N))
    front_temp[0, rank] = NDfront
    return front_temp, pareto_level
