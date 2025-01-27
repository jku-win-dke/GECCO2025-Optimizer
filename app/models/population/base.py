from abc import ABC

from pydantic import BaseModel


class PopulationBase(ABC, BaseModel):
    population_id: int
    duration: float = 0.0
