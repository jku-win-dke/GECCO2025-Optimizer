from abc import ABC, abstractmethod
from typing import Optional, List

import requests
from requests.exceptions import ConnectionError

from app.models.fitness.obj import Fitness
from app.models.obfuscation.obj import Obfuscation
from app.models.objective.base import ObjectiveBase
from app.models.population.obj import Population


class Objective(ObjectiveBase, ABC):
    obfuscation: Optional[Obfuscation] = None

    @abstractmethod
    def _get_fitness(self, encoding: List[int]) -> Fitness:
        pass

    def get_fitness(self, encoding: List[int]) -> Fitness:
        if self.privacy_engine is None:
            return self._get_fitness(encoding)

        return Fitness(objective_id=self.objective_id, actual_fitness=None)

    def evaluate_population(self, population: Population) -> List[Fitness]:
        if self.privacy_engine:
            try:
                response = requests.get(f'{self.privacy_engine}/status')
                #response.status_code = 111

                if response.status_code == 200:
                    if self.obfuscation:
                        try:
                            endpoint = self.obfuscation.endpoint_privacy_engine

                            solution_encoding = [solution.encoding for solution in population.solutions]
                            request = requests.put(f'{self.privacy_engine}/{endpoint}', json=solution_encoding)
                            response = request.json()

                            fitness_list = self.obfuscation.estimate_based_on_privacy_engine(response=response, population=population, objective_id=self.objective_id)

                        except AttributeError:
                            raise RuntimeError('No endpoint configured for obfuscation method')

                    else:
                        fitness_list = []

                        solution_encoding = [solution.encoding for solution in population.solutions]
                        fitness = requests.put(f'{self.privacy_engine}/computeFitnessClear', json=solution_encoding)

                        for i in range(len(population.solutions)):
                            fitness_list.append(Fitness(objective_id=self.objective_id, actual_fitness=fitness.json()[i]))

                else:
                    raise RuntimeError(f'Privacy Engine for objective {self.objective_id} is available but not reachable')

            except ConnectionError as e:
                raise RuntimeError(f'Privacy Engine for objective {self.objective_id} is not available')

        else:
            fitness_list = []

            for solution in population.solutions:
                fitness_list.append(self._get_fitness(encoding=solution.encoding))

            if self.obfuscation:
                fitness_list = self.obfuscation.obfuscate_and_estimate(fitness_list=fitness_list)

        return fitness_list
