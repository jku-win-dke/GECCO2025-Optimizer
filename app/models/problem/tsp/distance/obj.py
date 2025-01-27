from app.models.problem.tsp.distance.base import DistanceBase
from app.models.problem.tsp.node.obj import Node


class Distance(DistanceBase):
    node: Node
    