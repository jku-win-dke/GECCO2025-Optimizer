from typing import List, Dict

import numpy as np

from app.models.fitness.obj import Fitness
from app.models.solution.obj import Solution


def get_maximum_fitness_list(solutions: List[Solution]) -> List[Fitness]:
    """
    Get the maximum fitness based on the fitness of the solution candidates of the population.
    """
    fitness_dict: Dict[str, Fitness] = {}

    for solution in solutions:
        for fitness in solution.fitness_list:

            if fitness_dict.get(fitness.objective_id) is None:
                fitness_dict[fitness.objective_id] = Fitness(
                    objective_id=fitness.objective_id,
                    actual_fitness=fitness.actual_fitness,
                    estimated_fitness=fitness.estimated_fitness, )
            else:
                if (fitness_dict[fitness.objective_id].actual_fitness is None
                        or fitness.actual_fitness > fitness_dict[fitness.objective_id].actual_fitness):
                    fitness_dict[fitness.objective_id].actual_fitness = fitness.actual_fitness

                if (fitness_dict[fitness.objective_id].estimated_fitness is None
                        or fitness.estimated_fitness > fitness_dict[fitness.objective_id].estimated_fitness):
                    fitness_dict[fitness.objective_id].estimated_fitness = fitness.estimated_fitness

    return list(fitness_dict.values())


def get_unique_solutions(solutions: List[Solution]) -> List[Solution]:
    solution_groups: dict = {}
    for solution in solutions:
        encoding_tuple = tuple(solution.encoding)
        if solution_groups.get(encoding_tuple) is None:
            solution_groups[encoding_tuple] = []
        solution_groups[encoding_tuple].append(solution)

    unique_solutions: List[Solution] = []

    for encoding, solutions in solution_groups.items():
        maximum_fitness_list = get_maximum_fitness_list(solutions)

        unique_solution = Solution(encoding=encoding, fitness_list=maximum_fitness_list)
        unique_solutions.append(unique_solution)

    return unique_solutions


def filter_pareto_optimal_solutions(solutions: List[Solution]) -> List[Solution]:
    """
    Find the Pareto-optimal solutions based on actual fitness from a list of unique solutions.
    :param solutions: List of unique solutions
    :return: List of Pareto-optimal solutions
    """
    pareto_optimal_solutions: List[Solution] = []

    for solution in solutions:
        is_pareto_optimal = True

        fitness = np.array(
            [fitness.get_estimated_or_actual_fitness() for fitness in solution.fitness_list])

        for comparison_solution in solutions:
            if solution == comparison_solution:
                continue

            comparison_fitness = np.array(
                [fitness.get_estimated_or_actual_fitness() for fitness in comparison_solution.fitness_list])

            # Solution is dominated if for all objectives the fitness values are smaller or equal to
            # the fitness values of the comparison solution
            dominated = np.all(fitness <= comparison_fitness)

            # Solution is strictly dominated if it is dominated and the fitness value for one harmonic_objective
            # is smaller than the fitness value of the comparison solution
            strictly_dominated = dominated and np.any(fitness < comparison_fitness)

            if strictly_dominated:
                is_pareto_optimal = False
                break

        if is_pareto_optimal:
            pareto_optimal_solutions.append(solution)

    return pareto_optimal_solutions
