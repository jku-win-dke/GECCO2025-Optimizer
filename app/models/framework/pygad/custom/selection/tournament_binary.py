import random

import numpy as np

from app.models.framework.pygad.custom.selection.utils import dominates


def binary_pareto_tournament_selection(fitness, num_parents, ga_instance):
    parents_indices = []

    for parent_num in range(num_parents):
        # Select random different indices to compete in the tournament
        rand_indices = random.sample(range(len(fitness)), ga_instance.K_tournament)

        # Always two solutions compete against each other until only one remains
        while len(rand_indices) > 1:
            next_round = []

            # If the number of competitors is odd, the last one is added to the next round
            if len(rand_indices) % 2 == 1:
                next_round.append(rand_indices[-1])
                rand_indices = rand_indices[:-1]

            for i in range(0, len(rand_indices), 2):
                if dominates(fitness[rand_indices[i]], fitness[rand_indices[i + 1]]):
                    next_round.append(rand_indices[i])
                elif dominates(fitness[rand_indices[i + 1]], fitness[rand_indices[i]]):
                    next_round.append(rand_indices[i + 1])
                else:
                    next_round.append(rand_indices[i] if np.random.random() < 0.5 else rand_indices[i + 1])

            rand_indices = next_round

        parents_indices.append(rand_indices[0])

    parents = np.array(ga_instance.population[parents_indices])

    return parents, np.array(parents_indices)
