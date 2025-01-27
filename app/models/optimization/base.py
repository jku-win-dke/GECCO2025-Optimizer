from abc import ABC
from uuid import UUID

from pydantic import BaseModel

from app.models.status.enum import Status


class OptimizationBase(ABC, BaseModel):
    optimization_id: UUID = None
    status: Status = Status.CREATED
