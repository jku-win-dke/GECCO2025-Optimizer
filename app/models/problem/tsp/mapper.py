from app.models.problem.problem_mapper import ProblemMapper
from app.models.problem.tsp.dto import TspOutputResultDTO, TspOutputDTO, TspInputDTO
from app.models.problem.tsp.node.mapper import NodeMapper
from app.models.problem.tsp.obj import Tsp
from app.models.problem.tsp.objective.mapper import TspObjectiveMapper
from app.models.problem.tsp.round_trip.mapper import RoundTripMapper


class TspMapper(ProblemMapper):
    @staticmethod
    def to_result_dto(obj: Tsp) -> TspOutputResultDTO:
        nodes = [NodeMapper.to_dto(node) for node in obj.nodes]
        round_trips = [RoundTripMapper.to_dto(trip) for trip in obj.round_trips]
        return TspOutputResultDTO(
            nodes=nodes,
            round_trips=round_trips
        )

    @staticmethod
    def to_dto(obj: Tsp) -> TspOutputDTO:
        nodes = [NodeMapper.to_dto(node) for node in obj.nodes]
        objectives = [TspObjectiveMapper.to_dto(objective) for objective in obj.objectives]
        round_trips = [RoundTripMapper.to_dto(trip) for trip in obj.round_trips]
        return TspOutputDTO(
            nodes=nodes,
            objectives=objectives,
            round_trips=round_trips
        )

    @staticmethod
    def from_dto(dto: TspInputDTO) -> Tsp:
        nodes = [NodeMapper.from_dto(node) for node in dto.nodes]
        objectives = [TspObjectiveMapper.from_dto(objective, nodes) for objective in dto.objectives]
        return Tsp(
            nodes=nodes,
            objectives=objectives,
        )
