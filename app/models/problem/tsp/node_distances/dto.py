from typing import List

from app.models.problem.tsp.distance.dto import DistanceDTO
from app.models.problem.tsp.node_distances.base import NodeDistancesBase


class NodeDistancesDTO(NodeDistancesBase):
    node_id: int
    distances: List[DistanceDTO]
