from typing import List, Union

from app.models.fitness.dto import EstimatedFitnessDTO, ActualFitnessDTO, FitnessDTO
from app.models.problem.tsp.round_trip.base import RoundTripBase


class RoundTripDTO(RoundTripBase):
    sequence: List[int]
    fitness_list: List[Union[FitnessDTO, EstimatedFitnessDTO, ActualFitnessDTO]]
