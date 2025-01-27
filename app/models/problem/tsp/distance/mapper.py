from typing import List

from app.models.base_mapper import BaseMapper
from app.models.problem.tsp.distance.dto import DistanceDTO
from app.models.problem.tsp.distance.obj import Distance
from app.models.problem.tsp.node.obj import Node


class DistanceMapper(BaseMapper):
    @staticmethod
    def to_dto(obj: Distance) -> DistanceDTO:
        return DistanceDTO(
            value=obj.value,
            node_id=obj.node.node_id,
        )

    @staticmethod
    def from_dto(dto: DistanceDTO, nodes: List[Node]) -> Distance:
        node = None
        for n in nodes:
            if n.node_id == dto.node_id:
                node = n
                break

        return Distance(
            value=dto.value,
            node=node,
        )
