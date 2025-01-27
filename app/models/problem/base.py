from abc import ABC
from typing import Literal

from pydantic import BaseModel


class ProblemBase(ABC, BaseModel):
    problem_type: Literal["harmonic", "tsp"]
