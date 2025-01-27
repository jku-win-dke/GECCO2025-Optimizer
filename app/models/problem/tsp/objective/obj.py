from typing import List, Any

import numpy as np

from app.models.fitness.obj import Fitness
from app.models.objective.obj import Objective
from app.models.problem.tsp.node.obj import Node
from app.models.problem.tsp.node_distances.obj import NodeDistances
from app.models.problem.tsp.objective.base import TspObjectiveBase


class TspObjective(TspObjectiveBase, Objective):
    node_distances: List[NodeDistances]
    matrix: Any = None

    def _get_fitness(self, encoding: List[int]) -> Fitness:
        fitness = 0

        for i in range(len(encoding) - 1):
            fitness = fitness + self.matrix[encoding[i]][encoding[i + 1]]

        fitness = fitness + self.matrix[encoding[len(encoding) - 1]][encoding[0]]

        return Fitness(objective_id=self.objective_id, actual_fitness=fitness)

    def init_evaluation_setup(self, nodes: List[Node]) -> None:
        if isinstance(self.node_distances[0].distances[0].value, int):
            node_ids = [node.node_id for node in nodes]

            self.matrix = np.zeros((len(nodes), len(nodes)), dtype=np.integer)

            for node_distance in self.node_distances:
                from_node_idx = node_ids.index(node_distance.node.node_id)
                for distance in node_distance.distances:
                    to_node_idx = node_ids.index(distance.node.node_id)
                    self.matrix[from_node_idx][to_node_idx] = distance.value

        if self.privacy_engine:
            raise RuntimeError("Privacy Engine is not implemented yet")
