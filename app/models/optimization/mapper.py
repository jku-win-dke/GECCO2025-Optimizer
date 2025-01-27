from app.models.base_mapper import BaseMapper
from app.models.framework.registry import FrameworkMapperRegistry
from app.models.problem.registry import ProblemMapperRegistry
from app.models.statistics.mapper import StatisticsMapper
from .dto import OptimizationInputDTO, OptimizationOutputDTO, OptimizationOutputBaseDTO, \
    OptimizationOutputStatisticsDTO, OptimizationOutputResultDTO
from .obj import Optimization


class OptimizationMapper(BaseMapper):

    @staticmethod
    def to_dto(obj: Optimization) -> OptimizationOutputDTO:
        statistics = StatisticsMapper.to_dto(obj.statistics)

        problem_mapper = ProblemMapperRegistry.get_mapper(obj.problem.problem_type)
        problem = problem_mapper.to_dto(obj=obj.problem)

        framework_mapper = FrameworkMapperRegistry.get_mapper(obj.framework.framework_type)
        framework = framework_mapper.to_dto(obj=obj.framework)

        return OptimizationOutputDTO(
            optimization_id=obj.optimization_id,
            status=obj.status,
            statistics=statistics,
            problem=problem,
            framework=framework
        )

    @staticmethod
    def to_base_dto(obj: Optimization) -> OptimizationOutputBaseDTO:
        return OptimizationOutputBaseDTO(
            optimization_id=obj.optimization_id,
            status=obj.status
        )

    @staticmethod
    def to_statistics_dto(obj: Optimization) -> OptimizationOutputStatisticsDTO:
        statistics_dto = StatisticsMapper.to_dto(obj.statistics)

        return OptimizationOutputStatisticsDTO(
            optimization_id=obj.optimization_id,
            status=obj.status,
            statistics=statistics_dto
        )

    @staticmethod
    def to_result_dto(obj: Optimization) -> OptimizationOutputResultDTO:
        problem_mapper = ProblemMapperRegistry.get_mapper(obj.problem.problem_type)
        problem_dto = problem_mapper.to_result_dto(obj=obj.problem)

        return OptimizationOutputResultDTO(
            optimization_id=obj.optimization_id,
            status=obj.status,
            problem=problem_dto
        )

    @staticmethod
    def from_dto(dto: OptimizationInputDTO) -> Optimization:
        problem_mapper = ProblemMapperRegistry.get_mapper(dto.problem.problem_type)
        problem = problem_mapper.from_dto(dto=dto.problem)

        framework_mapper = FrameworkMapperRegistry.get_mapper(dto.framework.framework_type)
        framework = framework_mapper.from_dto(dto=dto.framework)

        return Optimization(
            problem=problem,
            framework=framework,
        )
