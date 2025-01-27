import random

import numpy as np


def uniform_order_based_crossover(parents, offspring_size, ga_instance, keep_genes_probability):
    def assign_genes(parent, offspring, other_parent):
        # Drop the genes from the parent that are already in the offspring, sort them by the order of the other parent
        # and assign them to the offspring
        dropped_genes = [gene for gene in parent if gene not in offspring]
        other_parent_list = other_parent.tolist()
        dropped_genes_sorted = sorted(dropped_genes, key=lambda x: other_parent_list.index(x))

        for i in range(len(offspring)):
            if offspring[i] == -1:
                offspring[i] = dropped_genes_sorted.pop(0)

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

        # Create a random mask based on the keep_genes_probability to determine which genes are being kept
        mask = [1 if random.random() < keep_genes_probability else 0 for _ in range(len(parent_one))]

        # Initialize the offspring with the kept genes from parent one as base
        offspring = [parent_one[i] if mask[i] == 1 else -1 for i in range(len(parent_one))]

        # Assign the remaining genes to the offspring from parent two
        offspring = assign_genes(parent_one, offspring, parent_two)

        offsprings.append(offspring)

    return np.array(offsprings)
