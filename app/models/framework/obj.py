from abc import abstractmethod

from app.models.problem.obj import Problem
from .base import FrameworkBase


class Framework(FrameworkBase):
    @abstractmethod
    def execute(self, problem: Problem, temp_populations, temp_dict, abortion_flag):
        """
        Abstract method that executes the optimization framework.
        :param problem: OptimizationProblem object
        :param temp_populations: List for storing the evaluated generations
        :param temp_dict: Dictionary for storing the statistics
        :param abortion_flag: Event for signaling abortion
        """
        pass
