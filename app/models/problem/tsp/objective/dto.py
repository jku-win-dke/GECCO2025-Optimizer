from typing import List

from app.models.objective.dto import ObjectiveDTO
from app.models.problem.tsp.node_distances.dto import NodeDistancesDTO
from app.models.problem.tsp.objective.base import TspObjectiveBase


class TspObjectiveDTO(TspObjectiveBase, ObjectiveDTO):
    node_distances: List[NodeDistancesDTO]
