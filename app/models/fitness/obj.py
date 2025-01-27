from typing import Optional

from .base import FitnessBase


class Fitness(FitnessBase):
    actual_fitness: Optional[int] = None
    estimated_fitness: Optional[int] = None

    def get_estimated_or_actual_fitness(self) -> int:
        if isinstance(self.estimated_fitness, int):
            return self.estimated_fitness
        return self.actual_fitness
