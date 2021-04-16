import numpy as np


def constraints_(in_, funct, min_, max_):
    """
    Checking for constraint violations
    :param in_: Input particles
    :param funct: For identifying test function
    :param min_: Lower bounds for the particles
    :param max_: Upper bounds for the particles
    Returns an array of <bool, int> pairs for how many constraints the particle violates
    """
    violations = np.zeros((in_.shape[0], 2))
    violations[:, 0] = True
    if funct == 1:
        """
        ZDT2 (unconstrained)
        """
        return violations
    if funct == 2:
        """
        Tanaka (constrained)
        x1^2 + x2^2 - 1 - 0.1*cos(16*arctan(x1/x2)) >= 0
        (x1-0.5)^2 + (x2-0.5)^2 <= 0.5
        """
        for i in range(in_.shape[0]):
            vcount = 0
            vcount += max(np.count_nonzero(in_[i] > max_),
                          np.count_nonzero(in_[i] < min_))
            arctan_value = np.arctan(in_[i, 0] / in_[i, 1])
            arctan_value = 16 * arctan_value
            cos_arctan_value = 0.1 * np.cos(arctan_value)
            if in_[i, 0] * in_[i, 0] + in_[i, 1] * in_[i, 1] - 1 - cos_arctan_value < 0:
                vcount += 1
            if (in_[i, 0] - 0.5) * (in_[i, 0] - 0.5) + (in_[i, 1] - 0.5) * (in_[i, 1] - 0.5) > 0.5:
                vcount += 1
            if vcount > 0:
                violations[i, 0] = False
                violations[i, 1] = vcount
        return violations
    if funct == 3:
        """
        Osyczka (constrained)
        x1 + x2 >= 2
        x1 + x2 <= 6
        x2 - x1 <= 2
        x1 - 3x2 <= 2
        (x3-3)^2 + x4 <= 4
        (x5-3)^2 + x6 >= 4
        """
        for i in range(in_.shape[0]):
            vcount = 0
            vcount += max(np.count_nonzero(in_[i] > max_),
                          np.count_nonzero(in_[i] < min_))
            if in_[i, 0] + in_[i, 1] < 2:
                vcount += 1
            if in_[i, 0] + in_[i, 1] > 6:
                vcount += 1
            if in_[i, 1] - in_[i, 0] > 2:
                vcount += 1
            if in_[i, 0] - 3*in_[i, 1] > 2:
                vcount += 1
            if (in_[i, 2] - 3) * (in_[i, 2] - 3) + in_[i, 3] > 4:
                vcount += 1
            if (in_[i, 4] - 3) * (in_[i, 4] - 3) + in_[i, 5] < 4:
                vcount += 1
            if vcount > 0:
                violations[i, 0] = False
                violations[i, 1] = vcount
        return violations
    if funct == 4:
        """
        Binh and Korn (constrained)
        (x-5)^2 + y^2 <= 25
        (x-8)^2 + (y+3)^2 >= 7.7
        """
        for i in range(in_.shape[0]):
            vcount = 0
            vcount += max(np.count_nonzero(in_[i] > max_),
                          np.count_nonzero(in_[i] < min_))
            if (in_[i, 0] - 5) * (in_[i, 0] - 5) + in_[i, 1] * in_[i, 1] > 25:
                vcount += 1
            if (in_[i, 0] - 8) * (in_[i, 0] - 8) + (in_[i, 1] + 3) * (in_[i, 1] + 3) < 7.7:
                vcount += 1
            if vcount > 0:
                violations[i, 0] = False
                violations[i, 1] = vcount
        return violations
