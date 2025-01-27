from typing import List

from app.models.solution.obj import Solution
from .base import PopulationBase


class Population(PopulationBase):
    solutions: List[Solution] = []
