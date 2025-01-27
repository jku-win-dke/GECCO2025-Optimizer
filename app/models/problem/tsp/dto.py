from typing import List

from app.models.problem.dto import ProblemDTO
from app.models.problem.tsp.base import TspBase
from app.models.problem.tsp.node.dto import NodeDTO
from app.models.problem.tsp.objective.dto import TspObjectiveDTO
from app.models.problem.tsp.round_trip.dto import RoundTripDTO


class TspInputDTO(TspBase, ProblemDTO):
    nodes: List[NodeDTO]
    objectives: List[TspObjectiveDTO]


class TspOutputDTO(TspBase, ProblemDTO):
    nodes: List[NodeDTO]
    objectives: List[TspObjectiveDTO]
    round_trips: List[RoundTripDTO] = []


class TspOutputResultDTO(TspBase, ProblemDTO):
    nodes: List[NodeDTO]
    round_trips: List[RoundTripDTO] = []
