from abc import ABC

from pydantic import BaseModel


class DistanceBase(ABC, BaseModel):
    value: int
