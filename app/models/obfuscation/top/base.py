from abc import ABC
from typing import Literal

from pydantic import BaseModel


class TopObfuscationBase(ABC, BaseModel):
    obfuscation_type: Literal["top"] = "top"
    top: int
