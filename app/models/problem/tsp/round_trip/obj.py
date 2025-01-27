from typing import List

from app.models.fitness.obj import Fitness
from app.models.problem.tsp.node.obj import Node
from app.models.problem.tsp.round_trip.base import RoundTripBase


class RoundTrip(RoundTripBase):
    sequence: List[Node]
    fitness_list: List[Fitness]
