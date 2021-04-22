import os
import numpy as np
import nondomsort
import delete_entry
import constraints
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D


def comp_show(algoA, algoB, fit_1, fit_2, fit_final):
    if fit_1.shape[1] == 2:
        plt.title(algoA + '_' + algoB + '_comparison')
        plt.xlabel('fitness_y1')
        plt.ylabel('fitness_y2')
        plt.scatter(fit_1[:, 0], fit_1[:, 1], s=30,
                    c='red', marker="|", alpha=1.0)
        plt.scatter(fit_2[:, 0], fit_2[:, 1], s=30,
                    c='green', marker="_", alpha=1.0)
        plt.scatter(fit_final[:, 0], fit_final[:, 1],
                    s=30, c='blue', marker="x", alpha=1.0)

    plt.savefig('./imgs/' + algoA + '_' + algoB + '_comparison.png')
    plt.close()


def getFile(funct):
    if funct == 1:
        path = "./coords/mopso_in.txt"
        fitpath = "./coords/mopso_fit.txt"
        algoName = "MOPSO+"
    elif funct == 2:
        path = "./coords/nsga2_in.txt"
        fitpath = "./coords/nsga2_fit.txt"
        algoName = "NSGA2"
    else:
        path = "./coords/smpso_in.txt"
        fitpath = "./coords/smpso_fit.txt"
        algoName = "SMPSO"
    return path, fitpath, algoName


def mergefiles(file1, file2):
    # Create numpy array
    archive_1 = np.loadtxt(file1)
    # print(archive_1.shape)
    archive_2 = np.loadtxt(file2)
    # print(archive_2.shape)
    archive_final = np.vstack((archive_1, archive_2))
    # print(archive_final.shape)
    return archive_1, archive_2, archive_final


def _compare_funcs(funct, min_, max_):
    print("\n\n1-MOPSO+ | 2-NSGA2 | 3-SMPSO")
    test = input("Would you like to compare algorithms? [y/n]: ")
    while(test != "n"):
        funct1 = int(input("\nEnter first algorithm: "))
        funct2 = int(input("Enter second algorithm: "))
        file1, fitpath1, algoA = getFile(funct1)
        file2, fitpath2, algoB = getFile(funct2)
        # Read both files and combine archive_in and archive_fitness
        archive_1, archive_2, archive_final = mergefiles(file1, file2)
        afit_1, afit_2, afit_final = mergefiles(fitpath1, fitpath2)
        # Check constraints
        violations_ = constraints.constraints_(
            archive_final, funct, min_, max_)

        # Call nondomsort
        first_tier_indices = nondomsort.nondomsort_(
            violations_, afit_final, archive_final.shape[0])[0] == 1
        first_tier_indices = np.reshape(first_tier_indices, (-1,))
        archive_in = archive_final[first_tier_indices]
        archive_fitness = afit_final[first_tier_indices]

        # Deleting excess elements (taking only 100 elements in the final archive)
        if archive_in.shape[0] > 100:
            removing = archive_in.shape[0] - 100
            archive_in, archive_fitness = delete_entry.delete_entry_(
                archive_in, archive_fitness, removing, 10)

        # print("Final archive shape:", archive_in.shape,
        #       "; Fitness shape:", archive_fitness.shape)

        np.savetxt("./coords/final_archive_in.txt", archive_in)
        np.savetxt("./coords/final_archive_fit.txt", archive_fitness)
        # Print graph of all three functions
        comp_show(algoA, algoB, afit_1, afit_2, archive_fitness)

        # Compare archive_final with archive_1 and archive_2
        pfA = 0
        pfB = 0
        Nc = 0
        flagA = False
        flagB = False
        for i in range(archive_fitness.shape[0]):
            flagA = False
            flagB = False
            if archive_fitness[i] in afit_1:
                # Total solutions contributed by A
                pfA += 1
                flagA = True
            if archive_fitness[i] in afit_2:
                # Total solutions contributed by B
                pfB += 1
                flagB = True
            if flagA and flagB:
                Nc += 1

        NtA = afit_1.shape[0]
        NtB = afit_2.shape[0]
        NuA = pfA - Nc
        NuB = pfB - Nc
        NrA = NtA - pfA
        NrB = NtB - pfB
        print("\tA\t|\tB")
        print("Nt =\t" + str(NtA) + "\t|\t" + str(NtB))
        print("Nc =\t" + str(Nc) + "\t|\t" + str(Nc))
        print("Nu =\t" + str(NuA) + "\t|\t" + str(NuB))
        print("Nr =\t" + str(NrA) + "\t|\t" + str(NrB))
        test = input("\nWould you like to compare algorithms? [y/n]: ")
