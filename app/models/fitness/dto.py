from typing import Optional

from .base import FitnessBase


class FitnessBaseDTO(FitnessBase):
    pass


class ActualFitnessDTO(FitnessBaseDTO):
    actual_fitness: Optional[int] = None


class EstimatedFitnessDTO(FitnessBaseDTO):
    estimated_fitness: Optional[int] = None


class FitnessDTO(ActualFitnessDTO, EstimatedFitnessDTO):
    pass
