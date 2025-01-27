from abc import ABC

from pydantic import BaseModel


class FitnessBase(ABC, BaseModel):
    objective_id: str
