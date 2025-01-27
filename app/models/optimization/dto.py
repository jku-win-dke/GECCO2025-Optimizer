from typing import Union

from pydantic import BaseModel, Field

from app.models.framework.pygad.dto import PygadFrameworkDTO
from app.models.statistics.dto import StatisticsDTO
from .base import OptimizationBase
from ..problem.tsp.dto import TspInputDTO, TspOutputResultDTO, TspOutputDTO


class OptimizationInputDTO(BaseModel):
    problem: Union[
        TspInputDTO] = Field(
        discriminator='problem_type'
    )
    framework: Union[
        PygadFrameworkDTO] = Field(
        discriminator='framework_type',
    )


class OptimizationOutputDTO(OptimizationBase):
    problem: Union[TspOutputDTO]
    framework: Union[PygadFrameworkDTO]
    statistics: StatisticsDTO


class OptimizationOutputBaseDTO(OptimizationBase):
    pass


class OptimizationOutputStatisticsDTO(OptimizationBase):
    statistics: StatisticsDTO


class OptimizationOutputResultDTO(OptimizationBase):
    problem: Union[TspOutputResultDTO]
