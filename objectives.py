import numpy as np


def get_objective(flag, funct, num_obj, Input):
    """
    Evaluates fitness values of the swarm
    :param flag: Flag for returning bounds or computing fitness
    :param funct: Function number
    :param num_obj: Number of objective functions
    :param Input: Input swarm
    Returns bounds of particles when flag is "init"
    Returns computed fitness values when flag is "value"
    """
    if flag == "init":
        if funct == 1:
            dim = 30
            MaxValue = np.ones((1, dim))
            MinValue = np.zeros((1, dim))
        elif funct == 2:
            MaxValue = np.array([np.pi, np.pi])
            MinValue = np.array([0, 0])
        elif funct == 3:
            MaxValue = np.array([10, 10, 5, 6, 5, 10])
            MinValue = np.array([0, 0, 1, 0, 1, 0])
        elif funct == 4:
            MaxValue = np.array([5, 3])
            MinValue = np.array([0, 0])
        else:
            MaxValue = np.ones((1, dim)) * 10
            MinValue = np.ones((1, dim)) * (-10)
        bounds = np.vstack((MinValue, MaxValue))
        return bounds
    elif flag == "value":
        Population = Input
        FunctionValue = np.zeros((Population.shape[0], num_obj))
        if funct == 1:
            # ZDT2
            FunctionValue[:, 0] = Population[:, 0]
            c = np.sum(FunctionValue[:, 1:], axis=1)
            g = 1.0 + 9.0 * c / 29
            FunctionValue[:, 1] = g * \
                (1 - np.power((FunctionValue[:, 0] * 1.0 / g), 2))
        elif funct == 2:
            # Tanaka
            FunctionValue[:, 0] = Population[:, 0]
            FunctionValue[:, 1] = Population[:, 1]
        elif funct == 3:
            # Osyczka
            FunctionValue[:, 0] = -25 * \
                ((Population[:, 0]-2)**2) - \
                ((Population[:, 1]-2)**2) - \
                ((Population[:, 2]-1)**2) - \
                ((Population[:, 3]-4)**2) - \
                ((Population[:, 4]-1)**2)
            FunctionValue[:, 1] = (Population[:, 0] ** 2) + \
                (Population[:, 1] ** 2) + \
                (Population[:, 2] ** 2) + \
                (Population[:, 3] ** 2) + \
                (Population[:, 4] ** 2) + \
                (Population[:, 5] ** 2)
        elif funct == 4:
            # Binh and Korn
            FunctionValue[:, 0] = (4 * (Population[:, 0]**2)) + \
                (4 * (Population[:, 1]**2))
            FunctionValue[:, 1] = ((Population[:, 0]-5)**2) + \
                ((Population[:, 1]-5)**2)

        # print(FunctionValue)
        return FunctionValue
