import random

import numpy as np


def shift_mutation_1(offspring, ga_instance):
    # based on Kruse et al. (2022)
    for i in range(offspring.shape[0]):
        individual = offspring[i, :].copy()

        # Determine a random start index for the subsequence and calculate the end index
        start_idx = random.randint(0, len(individual) - ga_instance.mutation_num_genes)
        end_idx = start_idx + ga_instance.mutation_num_genes

        # Cut out the subsequence of the offspring
        subsequence = individual[start_idx:end_idx]

        # Remove the subsequence from the offspring and insert it at the insertion index
        individual = np.concatenate((individual[:start_idx], individual[end_idx:]))

        # Determine a new insertion index (other than the start index)
        insertion_idx = random.randint(0, len(individual) + 1)
        while insertion_idx == start_idx:
            insertion_idx = random.randint(0, len(individual) + 1)

        offspring[i, :] = np.concatenate((individual[:insertion_idx], subsequence, individual[insertion_idx:]))

    return offspring