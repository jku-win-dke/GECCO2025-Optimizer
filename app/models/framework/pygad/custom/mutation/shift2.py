import random

import numpy as np


def shift_mutation_2(offspring, ga_instance):
    # based on Jenetics 8.1.0-2024
    for i in range(offspring.shape[0]):
        individual = offspring[i, :].copy()

        # Determine a random start index for the subsequence and calculate the end index
        start_idx = random.randint(0, len(individual) - ga_instance.mutation_num_genes)
        end_idx = start_idx + ga_instance.mutation_num_genes

        subsequence = individual[start_idx:end_idx]

        split_idx = random.randint(1, len(subsequence))

        first_half = subsequence[:split_idx]
        second_half = subsequence[split_idx:]

        swapped_subsequence = np.concatenate([second_half, first_half])

        individual[start_idx:end_idx] = swapped_subsequence

        offspring[i, :] = individual

    return offspring