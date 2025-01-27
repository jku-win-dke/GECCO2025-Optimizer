from typing import Dict, List

from app.models.fitness.obj import Fitness
from app.models.obfuscation.obj import Obfuscation
from app.models.population.obj import Population
from .base import AboveObfuscationBase


class AboveObfuscation(AboveObfuscationBase, Obfuscation):
    endpoint_privacy_engine: str = ''

    def __init__(self, /, **data):
        super().__init__(**data)
        self.endpoint_privacy_engine = f'computeClassification/{self.threshold}'

    def obfuscate_and_estimate(self, fitness_list: List[Fitness]) -> List[Fitness]:
        fitness_values = [fitness.actual_fitness for fitness in fitness_list]

        maximum_fitness = max(fitness_values)
        estimated_min_fitness = maximum_fitness - (2 * abs(maximum_fitness))

        for fitness in fitness_list:
            if fitness.actual_fitness > maximum_fitness * (self.threshold / 100):
                fitness.estimated_fitness = maximum_fitness
            else:
                fitness.estimated_fitness = estimated_min_fitness

        return fitness_list

    def estimate_based_on_privacy_engine(self, objective_id: str, population: Population, response: Dict) -> List[Fitness]:
        fitness_list = []

        indices_above_threshold = response['indices']
        maximum_fitness = response['highest']

        estimated_min_fitness = maximum_fitness - (2 * abs(maximum_fitness))

        for i in range(len(population.solutions)):
            estimated_fitness = maximum_fitness if i in indices_above_threshold else estimated_min_fitness
            fitness_list.append(Fitness(objective_id=objective_id, estimated_fitness=estimated_fitness))

        return fitness_list
