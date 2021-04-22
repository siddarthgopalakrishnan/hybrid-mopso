import numpy as np


def get_objective(flag, funct, num_obj, Input):
    """
    Evaluates fitness values of the swarm
    :param flag: Flag for returning bounds and computing fitness
    :param funct: Function number
    :param num_obj: Number of objective functions
    :param Input: Input swarm
    Returns bounds and dimensions of particles when flag is "init"
    Returns computed fitness values when flag is "value"
    """
    if flag == "init":
        if funct == 1:
            # ZDT2
            dim = 30
            MaxValue = np.ones((1, dim))
            MinValue = np.zeros((1, dim))
        elif funct == 2:
            # Tanaka
            MaxValue = np.array([np.pi, np.pi])
            MinValue = np.array([0, 0])
        elif funct == 3:
            # Osyczka
            MaxValue = np.array([10, 10, 5, 6, 5, 10])
            MinValue = np.array([0, 0, 1, 0, 1, 0])
        else:
            # Binh and Korn
            MaxValue = np.array([5, 3])
            MinValue = np.array([0, 0])
        bounds = np.vstack((MinValue, MaxValue))
        return bounds
    elif flag == "value":
        FunctionValue = np.zeros((Input.shape[0], num_obj))
        if funct == 1:
            # ZDT2
            FunctionValue[:, 0] = Input[:, 0]
            c = np.sum(FunctionValue[:, 1:], axis=1)
            g = 1.0 + 9.0 * c / 29
            FunctionValue[:, 1] = g * (1 - ((FunctionValue[:, 0] / g)**2))
        elif funct == 2:
            # Tanaka
            FunctionValue[:, 0] = Input[:, 0]
            FunctionValue[:, 1] = Input[:, 1]
        elif funct == 3:
            # Osyczka
            FunctionValue[:, 0] = -25 * \
                ((Input[:, 0]-2)**2) - \
                ((Input[:, 1]-2)**2) - \
                ((Input[:, 2]-1)**2) - \
                ((Input[:, 3]-4)**2) - \
                ((Input[:, 4]-1)**2)
            FunctionValue[:, 1] = (Input[:, 0] ** 2) + \
                (Input[:, 1] ** 2) + \
                (Input[:, 2] ** 2) + \
                (Input[:, 3] ** 2) + \
                (Input[:, 4] ** 2) + \
                (Input[:, 5] ** 2)
        elif funct == 4:
            # Binh and Korn
            FunctionValue[:, 0] = (4 * (Input[:, 0]**2)) + \
                (4 * (Input[:, 1]**2))
            FunctionValue[:, 1] = ((Input[:, 0]-5)**2) + \
                ((Input[:, 1]-5)**2)
        return FunctionValue
