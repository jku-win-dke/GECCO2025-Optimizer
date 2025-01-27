import numpy as np

from app.models.framework.pygad.custom.selection.utils import dominates


# TODO: pytest
def spea2_selection(fitness, num_parents, ga_instance, archive, archive_size):
    # based on Zitzler et al. (2001)
    # https://sop.tik.ee.ethz.ch/publicationListFiles/zlt2001a.pdf

    # print(f'Solutions per population: {ga_instance.sol_per_pop}')
    # print(f'Archive: {archive}')
    # print(f'Population before: {ga_instance.population}')
    # print(f'Original size of population: {len(ga_instance.population)}')
    # print(f'Original size of fitness: {len(fitness)}')

    # If the archive is not empty, the archived solutions are added to the population
    # If it contains the same solution like the population, the dominated fitness is kept
    if archive:
        for solution in archive:
            existing_solutions_idx = np.where(np.all(ga_instance.population == solution[0], axis=1))[0]
            if existing_solutions_idx.size > 0:
                current_fitness = fitness[existing_solutions_idx[0]]
                archived_fitness = solution[1]
                if dominates(archived_fitness, current_fitness):
                    fitness[existing_solutions_idx[0]] = solution[1]
            else:
                # TODO: Better work on a copy of the population?
                ga_instance.population = np.vstack((ga_instance.population, solution[0]))
                fitness = np.vstack((fitness, solution[1]))

    adjusted_population = ga_instance.population
    adjusted_fitness = fitness
    # print(f'Adjusted population size: {len(adjusted_population)}')
    # print(f'Adjusted fitness size: {len(fitness)}')
    # print(f'Fitness: {fitness}')
    # print(f'Number of parents: {num_parents}')
    # print(f'Population after: {ga_instance.population}')
    # print(f'Max archive size: {max_archive_size}')

    population_size = len(ga_instance.population)
    # print(f'Population size: {population_size}')

    # Compute the strength values
    strength = np.zeros(population_size)
    for i in range(population_size):
        for j in range(population_size):
            if i != j and dominates(fitness[i], fitness[j]):
                strength[i] += 1
    # print(f'Strength: {strength}')

    # Compute the raw fitness based on strength values
    raw_fitness = np.zeros(population_size)
    for i in range(population_size):
        for j in range(population_size):
            if i != j and dominates(fitness[j], fitness[i]):
                raw_fitness[i] += strength[j]
    # print(f'raw_fitness: {raw_fitness}')

    # Compute the matrix of euclidean distances
    distances = np.zeros((population_size, population_size))
    for i in range(population_size):
        for j in range(population_size):
            if i != j:
                distances[i, j] = np.linalg.norm(fitness[i] - fitness[j])
    # print(f'Distances:\n{distances}')

    # Compute the densities based on k-nearest neighbors
    densities = np.zeros(population_size)
    k = int(np.sqrt(population_size))
    for i in range(population_size):
        sorted_distances = np.sort(distances[i])
        densities[i] = 1 / (sorted_distances[k] + 2)
    # print(f'Densities: {densities}')

    # Compute the fitness values
    fitness_values = raw_fitness + densities
    # print(f'Fitness values: {fitness_values}')

    # Sort the parents based on their fitness values
    # The lower the value, the better the solution
    # indices_fitness_values_sorted = np.argsort(fitness_values)
    # print(f'Indices fitness sorted: {indices_fitness_values_sorted}')

    # Add the best solutions to the archive
    # TODO: truncation procedure is missing: what if the number of non-dominated solutions exceeds the archive size
    # new_archive = []
    # for i in range(max_archive_size):
    #     new_archive.append(
    #         (ga_instance.population[indices_fitness_values_sorted[i]], fitness[indices_fitness_values_sorted[i]]))
    # archive[:] = new_archive
    # print(f'Updated archive: {archive}')

    # Select indices of solutions with fitness < 1
    temp_indices = []
    for i in range(population_size):
        if fitness_values[i] < 1:
            temp_indices.append(i)

    # Fill archive with the best solutions having fitness >= 1
    if len(temp_indices) < archive_size:
        indices_fitness_values_sorted = np.argsort(fitness_values)
        for i in range(len(temp_indices), archive_size):
            temp_indices.append(indices_fitness_values_sorted[i])

    # Remove solutions from the archive based on the specified truncation operation
    elif len(temp_indices) > archive_size:
        while len(temp_indices) > archive_size:
            selected_distances = distances[:, temp_indices]
            min_distance_index = temp_indices[0]
            sorted_min_distances = sorted(selected_distances[min_distance_index])
            for i in range(1, len(temp_indices)):
                comparison_index = temp_indices[i]
                sorted_distances = sorted(selected_distances[comparison_index])
                for a, b in zip(sorted_min_distances, sorted_distances):
                    if a < b:
                        break
                    elif a > b:
                        min_distance_index = comparison_index
                        sorted_min_distances = sorted_distances
                        break

            # Remove the solution with the minimum distance
            temp_indices.remove(min_distance_index)

    # Update the archive
    temp_archive = []
    for i in range(archive_size):
        temp_archive.append((ga_instance.population[temp_indices[i]], fitness[temp_indices[i]]))
    archive[:] = temp_archive

    # TODO: Why don't you use: pygad.other.parent_selection.ParentSelection.tournament_selection()?
    #   If reusing the tournament method of pygad then the fitness values must be the inverse (*-1)
    #     because the computed fitness values are a minimization problem. But maybe its fine.
    # Perform binary tournament selection to select the parents
    parents_indices = []
    for parent_num in range(num_parents):
        # Generate random indices for the candidate solutions to compete
        # TODO: Avoid while true
        while True:
            rand_indices = np.random.randint(low=0, high=len(fitness), size=2)
            if len(set(rand_indices)) == len(rand_indices):
                break

        # print(f'Random indices: {rand_indices}')

        fitness_candidate_1 = fitness_values[rand_indices[0]]
        fitness_candidate_2 = fitness_values[rand_indices[1]]
        # print(f'Fitness candidate 1: {fitness_candidate_1}')
        # print(f'Fitness candidate 2: {fitness_candidate_2}')

        if fitness_candidate_1 < fitness_candidate_2:
            parents_indices.append(rand_indices[0])
            # print(f'Candidate 1 is better than candidate 2')
        elif fitness_candidate_2 < fitness_candidate_1:
            parents_indices.append(rand_indices[1])
            # print(f'Candidate 2 is better than candidate 1')
        else:
            if np.random.random() < 0.5:
                parents_indices.append(rand_indices[0])
                # print(f'Randomly selected candidate 1')
            else:
                parents_indices.append(rand_indices[1])
                # print(f'Randomly selected candidate 2')

    selected_parents = np.array(ga_instance.population[parents_indices])
    # print(f'Selected parents:\n{selected_parents}')
    # print(f'Selected parents indices:\n{parents_indices}')

    ga_instance.population = selected_parents
    fitness = fitness[parents_indices]
    # print(f'Population size after selection: {len(ga_instance.population)}')
    # print(f'Fitness size after selection: {len(fitness)}')

    # Modify the population and fitness to contain the selected parents
    # If the number of selected parents is smaller than the solutions per population, the n best solutions are added to the population
    # TODO: Necessary? What about placeholder solutions?
    if len(ga_instance.population) < ga_instance.sol_per_pop:
        num_additional_solutions = ga_instance.sol_per_pop - len(ga_instance.population)

        ga_instance.population = np.vstack(
            (ga_instance.population, adjusted_population[indices_fitness_values_sorted[:num_additional_solutions]]))
        fitness = np.vstack((fitness, adjusted_fitness[indices_fitness_values_sorted[:num_additional_solutions]]))

    # print(f'Population size after adding best solutions: {len(ga_instance.population)}')
    # print(f'Fitness size after adding best solutions: {len(fitness)}')
    # print(f'Population after selection: {ga_instance.population}')
    # print(f'Fitness after selection: {fitness}')

    return selected_parents, np.array(parents_indices)
