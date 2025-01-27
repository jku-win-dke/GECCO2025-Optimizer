from abc import ABC
from typing import Literal

from pydantic import BaseModel


class FrameworkBase(ABC, BaseModel):
    framework_type: Literal["scipy", "pygad", "exact"]
