from abc import ABC
from typing import Literal

from pydantic import BaseModel


class TspBase(ABC, BaseModel):
    problem_type: Literal["tsp"] = "tsp"
