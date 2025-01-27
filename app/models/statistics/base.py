from abc import ABC
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class StatisticsBase(ABC, BaseModel):
    time_optimization_created: datetime = datetime.now()
    time_run_started: Optional[datetime] = None
    time_run_stopped: Optional[datetime] = None
