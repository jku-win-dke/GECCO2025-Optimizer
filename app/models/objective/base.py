from abc import ABC
from typing import Optional

from pydantic import BaseModel, AnyUrl


class ObjectiveBase(ABC, BaseModel):
    objective_id: str
    privacy_engine: Optional[AnyUrl] = None
