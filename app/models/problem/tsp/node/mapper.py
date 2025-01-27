from app.models.base_mapper import BaseMapper
from app.models.problem.tsp.node.dto import NodeDTO
from app.models.problem.tsp.node.obj import Node


class NodeMapper(BaseMapper):
    @staticmethod
    def to_dto(obj: Node) -> NodeDTO:
        return NodeDTO(node_id=obj.node_id)

    @staticmethod
    def from_dto(dto: NodeDTO) -> Node:
        return Node(node_id=dto.node_id)
