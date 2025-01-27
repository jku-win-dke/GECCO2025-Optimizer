from typing import List

from app.models.population.dto import PopulationDTO
from .base import StatisticsBase


class StatisticsDTO(StatisticsBase):
    populations: List[PopulationDTO] = []
