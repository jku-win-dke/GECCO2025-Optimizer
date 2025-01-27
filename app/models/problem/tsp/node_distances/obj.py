from typing import List

from app.models.problem.tsp.distance.obj import Distance
from app.models.problem.tsp.node.obj import Node
from app.models.problem.tsp.node_distances.base import NodeDistancesBase


class NodeDistances(NodeDistancesBase):
    node: Node
    distances: List[Distance]
