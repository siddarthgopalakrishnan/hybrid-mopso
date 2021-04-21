import numpy as np
import os
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D


class Plot_pareto:
    def __init__(self):
        # Create coords directory
        if os.path.exists('./coords') == False:
            os.makedirs('./coords')
            print(
                '\nCreating folder coords : Save coordinates of pareto values and fitness of all algorithms')
        # Create image directory
        if os.path.exists('./imgs') == False:
            os.makedirs('./imgs')
            print('\nCreating folder imgs : Save image of each iteration')

    def show(self, fitness_, archive_fitness, i):
        # 3D plot for 3 objectives
        # if fitness_.shape[1] == 3:
        #     fig = plt.figure()
        #     ax = fig.add_subplot(111, projection='3d')
        #     # ax.scatter(fitness_[:, 0], fitness_[:, 1],
        #     #            fitness_[:, 2], c='blue', marker='.')
        #     ax.scatter(archive_fitness[:, 0], archive_fitness[:, 1],
        #                archive_fitness[:, 2], c='red', marker='.')
        #     ax.set_title('Iteration'+str(i+1))
        #     ax.set_xlabel('fitness_y1')
        #     ax.set_ylabel('fitness_y2')
        #     ax.set_zlabel('fitness_y3')

        # 2D plot for 2 objectives
        if fitness_.shape[1] == 2:
            plt.title('MOPSO+_Iteration_'+str(i+1))
            plt.xlabel('fitness_y1')
            plt.ylabel('fitness_y2')
            plt.scatter(
                archive_fitness[:, 0], archive_fitness[:, 1], s=30, c='red', marker=".", alpha=1.0)

        plt.savefig('./imgs/MOPSO+_Iteration_'+str(i+1)+'.png')
        plt.close()
