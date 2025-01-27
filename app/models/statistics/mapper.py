from app.models.base_mapper import BaseMapper
from app.models.population.mapper import PopulationMapper

from .dto import StatisticsDTO
from .obj import Statistics


class StatisticsMapper(BaseMapper):
    @staticmethod
    def to_dto(obj: Statistics) -> StatisticsDTO:
        populations = [PopulationMapper.to_dto(population) for population in obj.populations]

        return StatisticsDTO(
            time_optimization_created=obj.time_optimization_created,
            time_run_started=obj.time_run_started,
            time_run_stopped=obj.time_run_stopped,
            populations=populations
        )

    @staticmethod
    def from_dto(optimization_statistics_dto):
        raise Exception("Not implemented")
