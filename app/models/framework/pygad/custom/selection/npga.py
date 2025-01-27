import random

import numpy as np

from app.models.framework.pygad.custom.selection.utils import dominates


# TODO: Code review
# TODO: Tests
def npga_selection(fitness, num_parents, ga_instance, comparison_sample_size, niche_radius):
    # based on Horn et al. (1997)
    # https://ieeexplore.ieee.org/abstract/document/350037
    # see Discussion section for recommendations of the comparison sample size
    # see Discussion section for references for niche radius
    # see Horn & Nafpliotis (1993) for pseudo code

    parent_indices = []

    for parent_num in range(num_parents):
        rand_indices = random.sample(range(len(fitness)), 2 + comparison_sample_size)

        candidate_1 = rand_indices[0]
        candidate_2 = rand_indices[1]
        comparison_set = rand_indices[2:]

        candidate_1_dominated = False
        candidate_2_dominated = False
        for i in range(len(comparison_set)):
            comparison_individual = comparison_set[i]

            if dominates(fitness[comparison_individual], fitness[candidate_1]):
                candidate_1_dominated = True

            if dominates(fitness[comparison_individual], fitness[candidate_2]):
                candidate_2_dominated = True

            if candidate_1_dominated and candidate_2_dominated:
                break

        if not candidate_1_dominated and candidate_2_dominated:
            parent_indices.append(candidate_1)

        elif candidate_1_dominated and not candidate_2_dominated:
            parent_indices.append(candidate_2)

        else:
            candidate_1_niche_count = 0
            candidate_2_niche_count = 0

            for i in range(len(comparison_set)):
                comparison_individual = comparison_set[i]

                if np.linalg.norm(fitness[candidate_1] - fitness[comparison_individual]) <= niche_radius:
                    candidate_1_niche_count += 1

                if np.linalg.norm(fitness[candidate_2] - fitness[comparison_individual]) <= niche_radius:
                    candidate_2_niche_count += 1

            if candidate_1_niche_count < candidate_2_niche_count:
                parent_indices.append(candidate_1)

            else:
                parent_indices.append(candidate_2)

    parents = np.array(ga_instance.population[parent_indices])

    return parents, np.array(parent_indices)
