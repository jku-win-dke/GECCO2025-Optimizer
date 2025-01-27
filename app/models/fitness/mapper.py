from typing import Any

from app.models.base_mapper import BaseMapper
from .dto import FitnessBaseDTO, FitnessDTO, ActualFitnessDTO, EstimatedFitnessDTO
from .obj import Fitness


class FitnessMapper(BaseMapper):

    @staticmethod
    def to_dto(obj: Fitness) -> FitnessBaseDTO:
        if obj.actual_fitness is not None and obj.estimated_fitness is not None:
            return FitnessDTO(
                objective_id=obj.objective_id,
                actual_fitness=obj.actual_fitness,
                estimated_fitness=obj.estimated_fitness,
            )

        elif obj.actual_fitness is not None and obj.estimated_fitness is None:
            return ActualFitnessDTO(
                objective_id=obj.objective_id,
                actual_fitness=obj.actual_fitness,
            )

        elif obj.actual_fitness is None and obj.estimated_fitness is not None:
            return EstimatedFitnessDTO(
                objective_id=obj.objective_id,
                estimated_fitness=obj.estimated_fitness,
            )

        else:
            return FitnessBaseDTO(
                objective_id=obj.objective_id,
            )

    @staticmethod
    def from_dto(**kwargs) -> Any:
        raise Exception("FitnessMapper.from_dto() is not yet implemented")
