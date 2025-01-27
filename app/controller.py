import uuid
from typing import List

from app.logger.logger_config import logger
from app.models.optimization.dto import *
from app.models.optimization.mapper import OptimizationMapper
from app.models.optimization.obj import Optimization
from app.models.status.enum import Status


class OptimizationController:

    def __init__(self):
        self.optimizations: dict[uuid.UUID, Optimization] = {}

    def create_optimization(self, optimization_input_dto: OptimizationInputDTO) -> OptimizationOutputBaseDTO:
        """
        Creates an optimization based on an input dto and adds the optimization to the optimization dict.
        :param optimization_input_dto: OptimizationInputDTO
        :return: OptimizationBaseDTO
        """
        optimization = OptimizationMapper.from_dto(optimization_input_dto)

        optimization_id = uuid.uuid4()
        while optimization_id in self.optimizations:
            optimization_id = uuid.uuid4()

        optimization.optimization_id = optimization_id

        self.optimizations[optimization_id] = optimization
        logger.info(f'optimization with id {optimization_id} created and added successfully')

        return OptimizationMapper.to_base_dto(optimization)

    def get_optimizations(self) -> List[OptimizationOutputBaseDTO]:
        """
        Update and return the optimizations of the optimization dict.
        :return: List of OptimizationBaseDTOs
        """
        for optimization in self.optimizations.values():
            optimization.update()

        return [OptimizationMapper.to_base_dto(optimization) for optimization in self.optimizations.values()]

    def get_optimization(self, optimization_id: uuid.UUID) -> Union[None, OptimizationOutputDTO]:
        """
        Update and return a specific optimization from the optimization dict.
        If the optimization does not exist, None is returned.
        :param optimization_id: UUID of the optimization
        :return: OptimizationOutputDTO | None
        """
        optimization = self.optimizations.get(optimization_id)

        if optimization is None:
            logger.info(f'optimization with ID {optimization_id} not found')
            return None

        optimization.update()

        return OptimizationMapper.to_dto(optimization)

    def get_optimization_statistics(self, optimization_id: uuid.UUID) -> Union[None, OptimizationOutputStatisticsDTO]:
        """
        Update a specific optimization from the optimization dict and return its statistics.
        If the optimization does not exist, None is returned.
        :param optimization_id: UUID of the optimization
        :return: OptimizationOutputStatisticsDTO | None
        """
        optimization = self.optimizations.get(optimization_id)

        if optimization is None:
            logger.info(f'optimization with ID {optimization_id} not found')
            return None

        optimization.update()

        return OptimizationMapper.to_statistics_dto(optimization)

    def get_optimization_result(self, optimization_id: uuid.UUID) -> Union[None, OptimizationOutputResultDTO]:
        """
        Update a specific optimization from the optimization dict and return its result.
        If the optimization does not exist, None is returned.
        :param optimization_id: UUID of the optimization
        :return: OptimizationOutputResultDTO | None
        """
        optimization = self.optimizations.get(optimization_id)

        if optimization is None:
            logger.info(f'optimization with ID {optimization_id} not found')
            return None

        optimization.update()

        return OptimizationMapper.to_result_dto(optimization)

    def start_optimization(self, optimization_id: uuid.UUID, async_run: bool) -> Union[None, OptimizationOutputBaseDTO]:
        """
        Starts the optimization run with the specified ID for the framework to use.
        If the optimization is not available, it returns None.
        :param optimization_id: UUID of the optimization to start the optimization run for
        :param async_run: Boolean to determine if the optimization run should be asynchronous
        :return: OptimizationBaseDTO | None
        """
        optimization = self.optimizations.get(optimization_id)

        if optimization is None:
            logger.info(f'optimization with ID {optimization_id} not found')
            return None

        if optimization.status != Status.CREATED:
            logger.info(f'optimization with ID {optimization_id} has already been started')
            return None

        optimization.run(async_run)

        if async_run:
            logger.info(f'optimization with ID {optimization_id} running')
        else:
            logger.info(f'optimization with ID {optimization_id} finished')
            optimization.update()

        return OptimizationMapper.to_base_dto(optimization)

    def abort_optimization(self, optimization_id: uuid.UUID) -> Union[None, OptimizationOutputBaseDTO]:
        """
        Aborts the asynchronous optimization run with the specified ID using defined event flag.
        If the optimization is not available, it returns False.
        :param optimization_id: UUID of the optimization to abort
        :return: OptimizationBaseDTO | None
        """
        optimization = self.optimizations.get(optimization_id)

        if optimization is None:
            logger.info(f'optimization with ID {optimization_id} not found')
            return None

        if not optimization.abort():
            logger.info(f'optimization with ID {optimization_id} not running')
            return None

        logger.info(f'optimization with ID {optimization_id} aborted successfully')

        return OptimizationMapper.to_base_dto(optimization)

    def delete_optimization(self, optimization_id: uuid.UUID) -> bool:
        """
        Deletes the optimization with the specified ID from the optimizations' dictionary.
        If the optimization is not available, it returns False.
        :param optimization_id: UUID of the optimization to delete
        :return: True if the optimization was deleted successfully, False otherwise
        """
        optimization = self.optimizations.get(optimization_id)

        if optimization is None:
            logger.info(f'optimization with ID {optimization_id} not found')
            return False

        optimization.update()

        if optimization.status == Status.RUNNING:
            logger.info(f'optimization with ID {optimization_id} is currently running')
            return False

        del self.optimizations[optimization_id]
        logger.info(f'optimization with ID {optimization_id} deleted successfully')

        return True
