from typing import List

from app.models.population.obj import Population
from .base import StatisticsBase


class Statistics(StatisticsBase):
    populations: List[Population] = []

    @staticmethod
    def time_run_started_key() -> str:
        return "time_run_started"

    @staticmethod
    def time_run_stopped_key() -> str:
        return "time_run_stopped"
