from typing import List, Union

from app.models.fitness.dto import FitnessDTO, EstimatedFitnessDTO, ActualFitnessDTO
from .base import SolutionBase


class SolutionDTO(SolutionBase):
    fitness_list: List[Union[FitnessDTO, EstimatedFitnessDTO, ActualFitnessDTO]] = []
