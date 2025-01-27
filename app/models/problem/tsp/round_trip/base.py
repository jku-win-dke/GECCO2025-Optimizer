from abc import ABC

from pydantic import BaseModel


class RoundTripBase(ABC, BaseModel):
    pass
