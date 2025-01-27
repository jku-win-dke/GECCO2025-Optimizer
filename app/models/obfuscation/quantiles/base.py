from abc import ABC
from typing import Literal

from pydantic import BaseModel


class QuantilesObfuscationBase(ABC, BaseModel):
    obfuscation_type: Literal["quantiles"] = "quantiles"
    quantiles: int
