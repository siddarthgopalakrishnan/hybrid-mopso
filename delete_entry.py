import numpy as np


def delete_entry_(archiving_in, archiving_fit, removing, mesh_div):
    """
    Removes additional elements based on their crowding distance
    :param archiving_in: Archive population
    :param archiving_fit: Respective fitness values of archiving_in
    :param removing: Number of elements to remove
    :param mesh_div: Number of grid divisions
    Returns archive population and their fitness values after deleting the excess 
    """
    apop_size, _ = archiving_fit.shape
    # Calculate the grid location of each solution
    fmax = np.max(archiving_fit, axis=0)
    fmin = np.min(archiving_fit, axis=0)
    d = (fmax - fmin) / mesh_div
    fmin = np.tile(fmin, (apop_size, 1))
    d = np.tile(d, (apop_size, 1))
    grid_norm = np.floor((archiving_fit - fmin) / d)
    grid_norm[grid_norm >= mesh_div] = mesh_div - 1
    grid_norm[np.isnan(grid_norm)] = 0
    # Detect the grid of each solution belongs to
    _, _, grid_site = np.unique(grid_norm, return_index=True,
                                return_inverse=True, axis=0)
    # Calculate the crowd degree of each grid
    crowding = np.histogram(grid_site, np.max(grid_site)+1)[0]
    del_index = np.zeros(apop_size,) == 1

    while np.sum(del_index) < removing:
        # Grid cell with maximum density
        maxdense = np.where(crowding == max(crowding))[0]
        # Element index from this grid
        ele_ind = np.random.randint(0, len(maxdense))
        # Random element from the cell
        Grid = maxdense[ele_ind]
        InGrid = np.where(grid_site == Grid)[0]
        ele_ind = np.random.randint(0, len(InGrid))
        p = InGrid[ele_ind]
        del_index[p] = True
        grid_site[p] = -100
        crowding[Grid] = crowding[Grid] - 1

    del_index = np.where(del_index == 1)[0]
    archiving_in = np.delete(archiving_in, del_index, 0)
    archiving_fit = np.delete(archiving_fit, del_index, 0)
    return archiving_in, archiving_fit
