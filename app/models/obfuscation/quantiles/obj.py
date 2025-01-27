from typing import Dict, List

from app.models.fitness.obj import Fitness
from app.models.obfuscation.obj import Obfuscation
from app.models.population.obj import Population
from .base import QuantilesObfuscationBase


class QuantilesObfuscation(QuantilesObfuscationBase, Obfuscation):
    endpoint_privacy_engine: str = ''

    def __init__(self, /, **data):
        super().__init__(**data)
        self.endpoint_privacy_engine = f'computeQuantiles/{self.quantiles}'

    def obfuscate_and_estimate(self, fitness_list: List[Fitness]) -> List[Fitness]:
        fitness_values = [fitness.actual_fitness for fitness in fitness_list]

        maximum_fitness = max(fitness_values)
        estimated_min_fitness = maximum_fitness - (2 * abs(maximum_fitness))
        distance = abs((maximum_fitness - estimated_min_fitness) / (self.quantiles - 1))

        fitness_values.sort(reverse=True)

        solutions_per_quantile = len(fitness_list) // self.quantiles

        quantile_mapping = []
        for i, fitness in enumerate(fitness_values):
            quantile = i // solutions_per_quantile

            # Add the remaining solutions to the last quantile
            if quantile >= self.quantiles:
                quantile = self.quantiles - 1

            quantile_mapping.append((fitness, quantile))

        for fitness in fitness_list:
            for f, quantile in quantile_mapping:
                if f == fitness.actual_fitness:
                    fitness.estimated_fitness = round(maximum_fitness - (quantile * distance))
                    quantile_mapping.remove((f, quantile))
                    break

        return fitness_list

    def estimate_based_on_privacy_engine(self, objective_id: str, population: Population, response: Dict) -> List[Fitness]:
        fitness_list = []

        maximum_fitness = response['maximum']
        obfuscated_fitness = response['mapping']

        obfuscated_fitness = obfuscated_fitness[:len(population.solutions)]
        min_quantile = min(obfuscated_fitness)

        estimated_min_fitness = maximum_fitness - (2 * abs(maximum_fitness))
        distance = abs((maximum_fitness - estimated_min_fitness) / (self.quantiles - 1))

        for i in range(len(population.solutions)):
            estimated_fitness = round(estimated_min_fitness + (distance * (obfuscated_fitness[i] - min_quantile)))
            fitness_list.append(Fitness(objective_id=objective_id, estimated_fitness=estimated_fitness))

        return fitness_list
