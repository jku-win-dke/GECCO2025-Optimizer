import time
from datetime import datetime
from typing import List

from pygad import pygad

from app.models.framework.obj import Framework
from app.models.framework.pygad.base import PygadFrameworkBase
from app.models.population.obj import Population
from app.models.problem.obj import Problem
from app.models.solution.obj import Solution
from app.models.statistics.obj import Statistics


class PygadFramework(PygadFrameworkBase, Framework):

    @staticmethod
    def _batch_fitness_function_factory(problem: Problem, populations):
        """
        Factory method for creating the fitness function for the genetic algorithm.
        :param problem: OptimizationProblem object
        :return: Fitness function for the genetic algorithm
        """

        def _fitness_function(ga_instance, solutions, solution_indices):
            """
            Fitness function for the genetic algorithm.
            :param ga_instance: PyGAD instance
            :param solutions: Solutions to evaluate
            :param solution_indices: Indices of the solutions
            :return: Fitness of the solutions
            """
            # convert solution encodings into a population object
            population: Population = Population(population_id=ga_instance.generations_completed)
            for solution in solutions:
                population.solutions.append(Solution(encoding=solution))

            # evaluate the population
            population = problem.evaluate_population(population)

            # store the evaluated population
            populations.append(population)

            # convert the evaluated population object into fitness values for pygad
            fitness_list = []
            for solution in population.solutions:
                solution_fitness_list = []
                for fitness in solution.fitness_list:
                    solution_fitness_list.append(fitness.get_estimated_or_actual_fitness())

                if len(solution_fitness_list) == 1:
                    fitness_list.append(solution_fitness_list[0])
                else:
                    fitness_list.append(solution_fitness_list)

            return fitness_list

        return _fitness_function

    @staticmethod
    def _on_start_factory(on_start_time):
        def _on_start(ga_instance):
            on_start_time.append(time.time())
        return _on_start

    @staticmethod
    def _on_fitness_factory(start_times):
        def _on_fitness(ga_instance, population_fitness):
            start_times.append(time.time())
        return _on_fitness

    @staticmethod
    def _on_generation_factory(abortion_flag, end_times):
        def _on_generation(ga_instance):
            end_times.append(time.time())
            if abortion_flag.is_set():
                return "stop"
        return _on_generation

    def execute(self, problem: Problem, temp_populations, temp_dict, abortion_flag):
        temp_dict[Statistics.time_run_started_key()] = datetime.now()

        on_start_time: List[float] = []
        start_times: List[float] = []
        end_times: List[float] = []

        ga_instance = pygad.GA(
            num_generations=self.num_generations,
            num_parents_mating=self.num_parents_mating,
            fitness_func=self._batch_fitness_function_factory(problem=problem, populations=temp_populations),
            fitness_batch_size=self.sol_per_pop,
            sol_per_pop=self.sol_per_pop,
            num_genes=problem.get_problem_size(),
            gene_type=int,
            init_range_low=self.init_range_low,
            init_range_high=self.init_range_high,
            parent_selection_type=self.parent_selection_type,
            keep_parents=self.keep_parents,
            keep_elitism=self.keep_elitism,
            K_tournament=self.K_tournament,
            crossover_type=self.crossover_type_mapping,
            crossover_probability=self.crossover_probability,
            mutation_type=self.mutation_type_mapping,
            mutation_probability=self.mutation_probability,
            mutation_by_replacement=self.mutation_by_replacement,
            mutation_percent_genes=self.mutation_percent_genes,
            mutation_num_genes=self.mutation_num_genes,
            random_mutation_min_val=self.random_mutation_min_val,
            random_mutation_max_val=self.random_mutation_max_val,
            gene_space=problem.get_gene_space(),
            on_start=self._on_start_factory(on_start_time),
            on_fitness=self._on_fitness_factory(start_times=start_times),
            on_generation=self._on_generation_factory(abortion_flag=abortion_flag, end_times=end_times),
            save_best_solutions=self.save_best_solutions,
            save_solutions=self.save_solutions,
            suppress_warnings=False,
            allow_duplicate_genes=problem.allow_duplicate_genes(),
            stop_criteria=self.stop_criteria,
            parallel_processing=self.parallel_processing,
            random_seed=self.random_seed,
            logger=None
        )

        ga_instance.run()

        # set duration for each population
        population = temp_populations[0]
        population.duration = start_times[0] - on_start_time[0]
        temp_populations[0] = population
        for i in range(0, len(temp_populations) - 1):
            population = temp_populations[i + 1]
            population.duration = end_times[i] - start_times[i]
            temp_populations[i + 1] = population

        temp_dict[Statistics.time_run_stopped_key()] = datetime.now()
