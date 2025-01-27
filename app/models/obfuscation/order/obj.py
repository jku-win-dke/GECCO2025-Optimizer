from typing import Dict, List

from app.models.fitness.obj import Fitness
from app.models.obfuscation.obj import Obfuscation
from app.models.population.obj import Population
from .base import OrderObfuscationBase


class OrderObfuscation(OrderObfuscationBase, Obfuscation):
    endpoint_privacy_engine: str = 'computePopulationOrder'

    def obfuscate_and_estimate(self, fitness_list: List[Fitness]) -> List[Fitness]:
        fitness_values = [fitness.actual_fitness for fitness in fitness_list]

        maximum_fitness = max(fitness_values)
        estimated_min_fitness = maximum_fitness - (2 * abs(maximum_fitness))
        distance = abs((maximum_fitness - estimated_min_fitness) / (len(fitness_list) - 1))

        fitness_values.sort(reverse=True)

        for fitness in fitness_list:
            fitness.estimated_fitness = round(maximum_fitness - (fitness_values.index(fitness.actual_fitness) * distance))

        return fitness_list

    def estimate_based_on_privacy_engine(self, objective_id: str, population: Population, response: Dict) -> List[Fitness]:
        fitness_list = []

        max_fitness = response['maximum']
        order = response['order'][::-1]

        estimated_min_fitness = max_fitness - (2 * abs(max_fitness))
        distance = abs((max_fitness - estimated_min_fitness) / (len(population.solutions) - 1))

        for i in range(len(population.solutions)):
            estimated_fitness = round(max_fitness - (distance * order.index(i)))
            fitness_list.append(Fitness(objective_id=objective_id, estimated_fitness=estimated_fitness))

        return fitness_list
