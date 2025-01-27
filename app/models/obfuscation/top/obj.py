from typing import Dict, List

from app.models.fitness.obj import Fitness
from app.models.obfuscation.obj import Obfuscation
from app.models.population.obj import Population
from .base import TopObfuscationBase


class TopObfuscation(TopObfuscationBase, Obfuscation):
    endpoint_privacy_engine: str = ''

    def __init__(self, /, **data):
        super().__init__(**data)
        self.endpoint_privacy_engine = f'computeTopIndividuals/{self.top}'

    def obfuscate_and_estimate(self, fitness_list: List[Fitness]) -> List[Fitness]:
        fitness_values = [fitness.actual_fitness for fitness in fitness_list]

        maximum_fitness = max(fitness_values)
        estimated_min_fitness = maximum_fitness - (2 * abs(maximum_fitness))

        fitness_values.sort(reverse=True)

        # only keep the top n fitness values
        fitness_values = fitness_values[:self.top]

        for fitness in fitness_list:
            if fitness.actual_fitness in fitness_values:
                fitness.estimated_fitness = maximum_fitness
                fitness_values.remove(fitness.actual_fitness)
            else:
                fitness.estimated_fitness = estimated_min_fitness

        return fitness_list

    def estimate_based_on_privacy_engine(self, objective_id: str, population: Population, response: Dict) -> List[Fitness]:
        fitness_list = []

        print(f'Response: {response}')
        #
        # for i, solution in enumerate(population.solutions):
        #     print(f'Solution {i}: {solution}')

        maximum_fitness = response['highest']
        indices_top_individuals = response['indices']

        print(indices_top_individuals)

        # Decrease the indices by the length of the population to get the correct indices
        indices_top_individuals = [idx - len(population.solutions) for idx in indices_top_individuals]

        estimated_min_fitness = maximum_fitness - (2 * abs(maximum_fitness))

        for i in range(len(population.solutions)):
            estimated_fitness = maximum_fitness if i in indices_top_individuals else estimated_min_fitness
            fitness_list.append(Fitness(objective_id=objective_id, estimated_fitness=estimated_fitness))

        # print(f'Maximum fitness: {maximum_fitness}')
        # print(f'Indices of top individuals: {indices_top_individuals}')
        # print(f'Length of population: {len(population.solutions)}')
        # print(f'Indices of top individuals: {indices_top_individuals}')

        return fitness_list
