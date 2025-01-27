from typing import List

from app.models.base_mapper import BaseMapper
from app.models.problem.tsp.distance.mapper import DistanceMapper
from app.models.problem.tsp.node.obj import Node
from app.models.problem.tsp.node_distances.dto import NodeDistancesDTO
from app.models.problem.tsp.node_distances.obj import NodeDistances


class NodeDistancesMapper(BaseMapper):
    @staticmethod
    def from_dto(dto: NodeDistancesDTO, nodes: List[Node]) -> NodeDistances:
        node = None
        for n in nodes:
            if n.node_id == dto.node_id:
                node = n

        distances = [DistanceMapper.from_dto(distance, nodes) for distance in dto.distances]

        return NodeDistances(
            node=node,
            distances=distances,
        )

    @staticmethod
    def to_dto(obj: NodeDistances) -> NodeDistancesDTO:
        distances = [DistanceMapper.to_dto(distance) for distance in obj.distances]

        return NodeDistancesDTO(
            node_id=obj.node.node_id,
            distances=distances,
        )
