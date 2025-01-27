from typing import List

from app.models.problem.obj import Problem
from app.models.problem.tsp.base import TspBase
from app.models.problem.tsp.node.obj import Node
from app.models.problem.tsp.objective.obj import TspObjective
from app.models.problem.tsp.round_trip.obj import RoundTrip
from app.models.solution.obj import Solution


class Tsp(TspBase, Problem):
    nodes: List[Node]
    objectives: List[TspObjective]
    round_trips: List[RoundTrip] = []

    def __init__(self, /, **data):
        super().__init__(**data)

        self.nodes = sorted(self.nodes, key=lambda node: node.node_id)

        for objective in self.objectives:
            objective.init_evaluation_setup(self.nodes)

    def update_result(self, solutions: List[Solution]) -> None:
        temp_round_trips = []

        for solution in solutions:
            sequence: List[Node] = []
            for node_idx in solution.encoding:
                sequence.append(self.nodes[node_idx])

            roundtrip = RoundTrip(sequence=sequence, fitness_list=solution.fitness_list)
            temp_round_trips.append(roundtrip)

        self.round_trips = temp_round_trips

    def get_problem_size(self) -> int:
        return len(self.nodes)

    def get_gene_space(self) -> List[int]:
        return list(range(len(self.nodes)))

    def allow_duplicate_genes(self) -> bool:
        return False
