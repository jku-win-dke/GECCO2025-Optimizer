from typing import Any

from app.models.base_mapper import BaseMapper
from app.models.fitness.mapper import FitnessMapper
from app.models.problem.tsp.round_trip.dto import RoundTripDTO
from app.models.problem.tsp.round_trip.obj import RoundTrip


class RoundTripMapper(BaseMapper):
    @staticmethod
    def to_dto(obj: RoundTrip) -> RoundTripDTO:
        sequence = [node.node_id for node in obj.sequence]

        fitness_list = [FitnessMapper.to_dto(fitness) for fitness in obj.fitness_list]

        return RoundTripDTO(
            sequence=sequence,
            fitness_list=fitness_list,
        )

    @staticmethod
    def from_dto(**kwargs) -> Any:
        raise Exception("RoundtripMapper.from_dto() is not yet implemented")
