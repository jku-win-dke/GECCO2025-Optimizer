import random

import numpy as np

from app.models.framework.pygad.custom.selection.utils import dominates


def random_pareto_tournament_selection(fitness, num_parents, ga_instance):
    parents_indices = []

    for parent_num in range(num_parents):
        # Select random different indices to compete in the tournament
        # Select random different indices to compete in the tournament
        rand_indices = random.sample(range(len(fitness)), ga_instance.K_tournament)

        # Define the pareto front
        pareto_front = []
        for i in range(len(rand_indices)):
            is_dominated = False
            for j in range(len(rand_indices)):
                if i != j and dominates(fitness[rand_indices[j]], fitness[rand_indices[i]]):
                    is_dominated = True
                    break
            if not is_dominated:
                pareto_front.append(rand_indices[i])

        # Select a random solution from the pareto front
        selected_index = np.random.choice(pareto_front)
        parents_indices.append(selected_index)

    parents = np.array(ga_instance.population[parents_indices])

    return parents, np.array(parents_indices)
