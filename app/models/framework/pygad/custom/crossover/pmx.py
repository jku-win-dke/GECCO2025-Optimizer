import random

import numpy as np


def partially_matched_crossover(parents, offspring_size, ga_instance):
    # based on Jenetics 8.1.0-2024
    def swap_genes(offspring, start_idx, end_idx, parent):
        # Try to insert the genes from the parent that are not in the offspring
        # If the gene is already in the offspring, try to insert the gene from the other parent
        for i in range(len(offspring)):
            if i < start_idx or i >= end_idx:
                gene_to_swap = parent[i]

                if gene_to_swap not in offspring:
                    offspring[i] = gene_to_swap
                else:
                    while True:
                        alternative_gene_idx = np.where(offspring == gene_to_swap)[0][0]
                        gene_to_swap = parent[alternative_gene_idx]

                        if gene_to_swap not in offspring:
                            offspring[i] = gene_to_swap
                            break

        return offspring

    offsprings = []

    for k in range(offspring_size[0]):
        if ga_instance.crossover_probability is not None:
            probs = np.random.random(size=parents.shape[0])
            indices = list(set(np.where(probs <= ga_instance.crossover_probability)[0]))

            # If no parent satisfied the probability, no crossover is applied and a parent is selected
            if len(indices) == 0:
                offsprings.append(parents[k % parents.shape[0], :].copy())
                continue
            elif len(indices) == 1:
                parent1_idx = indices[0]
                parent2_idx = indices[0]
            else:
                indices = random.sample(indices, 2)
                parent1_idx = indices[0]
                parent2_idx = indices[1]
        else:
            # Index of the first parent to mate
            parent1_idx = k % parents.shape[0]
            # Index of the second parent to mate
            parent2_idx = (k + 1) % parents.shape[0]

        parent_one = parents[parent1_idx, :].copy()
        parent_two = parents[parent2_idx, :].copy()

        # Add 1 to the chromosome_length to include the last element in the range.
        chromosome_length = parent_one.shape[0]
        start_idx, end_idx = sorted(random.sample(range(chromosome_length + 1), 2))

        # Initialize the offspring with parent one as the base
        offspring = np.full(chromosome_length, -1)
        offspring[start_idx:end_idx] = parent_one[start_idx:end_idx]

        # Swap the remaining genes from parent two
        offspring = swap_genes(offspring, start_idx, end_idx, parent_two)

        offsprings.append(offspring)

    return np.array(offsprings)