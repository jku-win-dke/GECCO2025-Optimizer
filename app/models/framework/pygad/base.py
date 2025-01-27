from abc import ABC
from typing import Literal, Optional, Union, List, Tuple

from pydantic import BaseModel

from app.models.framework.pygad.custom.crossover.enum import CustomCrossoverEnum
from app.models.framework.pygad.custom.mutation.enum import CustomMutationEnum


class PygadFrameworkBase(ABC, BaseModel):
    framework_type: Literal["pygad"] = "pygad"
    # for uox
    keep_genes_probability: Optional[float] = None

    num_generations: int
    num_parents_mating: int
    sol_per_pop: int
    init_range_low: int = -4
    init_range_high: int = 4
    parent_selection_type: Literal['sss', 'rws', 'sus', 'rank', 'random', 'tournament', 'tournament_nsga2', 'nsga2']
    keep_parents: int = 0
    keep_elitism: int = 0
    K_tournament: int = 3
    crossover_type: Optional[Literal['single_point', 'two_points', 'uniform', 'scattered', CustomCrossoverEnum.PMX.value[0],
    CustomCrossoverEnum.UOX.value[0]]]
    crossover_probability: Optional[float] = None
    mutation_type: Optional[Literal['random', 'swap', 'inversion', 'scramble', 'adaptive', CustomMutationEnum.SHIFT_1.value[0],
    CustomMutationEnum.SHIFT_2.value[0]]]
    mutation_probability: Optional[float] = None
    mutation_by_replacement: bool = False
    mutation_percent_genes: int = 10
    mutation_num_genes: Optional[int] = None
    random_mutation_min_val: float = -1.0
    random_mutation_max_val: float = 1.0
    save_best_solutions: bool = False
    save_solutions: bool = False
    stop_criteria: Optional[str] = None
    parallel_processing: Optional[Union[int, List[Union[str, int]], Tuple[Union[str, int], ...]]] = None
    random_seed: Optional[int] = None

    @property
    def mutation_type_mapping(self):
        if isinstance(self.mutation_type, str):
            for mutation in CustomMutationEnum:
                if self.mutation_type == mutation.value[0]:
                    return mutation.value[1]
        return self.mutation_type

    @property
    def crossover_type_mapping(self):
        if isinstance(self.crossover_type, str):
            if self.crossover_type == CustomCrossoverEnum.UOX.value[0]:
                if self.keep_genes_probability is None:
                    raise ValueError("keep_genes_probability is None")
                return lambda parents, offspring_size, ga_instance: (
                    CustomCrossoverEnum.UOX.value[1](parents, offspring_size, ga_instance, self.keep_genes_probability))
            for crossover in CustomCrossoverEnum:
                if self.crossover_type == crossover.value[0]:
                    return crossover.value[1]
        return self.crossover_type
