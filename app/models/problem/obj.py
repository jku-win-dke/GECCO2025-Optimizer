import concurrent.futures
from abc import abstractmethod
from typing import List

from app.models.objective.obj import Objective
from app.models.population.obj import Population
from app.models.solution.obj import Solution
from .base import ProblemBase


class Problem(ProblemBase):
    # will be overwritten by concrete objectives in subclasses
    objectives: List[Objective]

    def evaluate_population(self, population: Population) -> Population:
        fitness_dict_population = {objective.objective_id: [] for objective in self.objectives}

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(objective.evaluate_population, population): objective for objective in self.objectives}

            # Once the future is completed, the result is stored in the dictionary with the objective_id as the key
            for future in concurrent.futures.as_completed(futures):
                objective = futures[future]
                fitness_dict_population[objective.objective_id] = future.result()

        # Assign the fitness objects to the population for each solution
        for i, solution in enumerate(population.solutions):
            solution.fitness_list = [fitness_dict_population[objective.objective_id][i] for objective in self.objectives]

        return population

    def evaluate_solution(self, solution: Solution) -> Solution:
        population = Population(population_id=-1, solutions=[solution])
        return self.evaluate_population(population).solutions[0]

    @abstractmethod
    def update_result(self, solutions: List[Solution]) -> None:
        pass

    @abstractmethod
    def get_problem_size(self) -> int:
        pass

    @abstractmethod
    def get_gene_space(self) -> List[int]:
        pass

    @abstractmethod
    def allow_duplicate_genes(self) -> bool:
        pass
