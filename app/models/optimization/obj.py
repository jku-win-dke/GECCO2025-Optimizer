import multiprocessing
from typing import Any, List

from app.models import utils
from app.models.framework.obj import Framework
from app.models.problem.obj import Problem
from app.models.statistics.obj import Statistics
from app.models.status.enum import Status
from .base import OptimizationBase
from .custom_process.process import Process
from ..solution.obj import Solution


class Optimization(OptimizationBase):
    def __init__(self, /, **data):
        super().__init__(**data)
        self.abortion_flag = multiprocessing.Event()
        self.manager = multiprocessing.Manager()
        self.temp_populations = self.manager.list()
        self.temp_dict = self.manager.dict()

    problem: Problem
    framework: Framework
    statistics: Statistics = Statistics()
    abortion_flag: multiprocessing.Event = None
    manager: multiprocessing.Manager = None
    temp_populations: List = []
    temp_dict: dict = {}
    process: Any = None

    def run(self, async_run: bool) -> bool:
        """
        Creates a new process for the optimization run and starts it.
        :param async_run: Boolean to determine if the optimization run should be asynchronous or not.
        :return: Indicates if the optimization run was started successfully.
        """
        try:
            self.process = Process(target=self.framework.execute,
                                   args=(self.problem,
                                         self.temp_populations,
                                         self.temp_dict,
                                         self.abortion_flag),
                                   daemon=True)

            self.process.start()
            self.status = Status.RUNNING

            if not async_run:
                self.process.join()

            return True

        except Exception as e:
            self.status = Status.FAILED
            return False

    def abort(self) -> bool:
        if (self.process is None) or (not self.process.is_alive()):
            return False

        self.abortion_flag.set()
        self.process.join()
        self.update()
        self.status = Status.ABORTED
        return True

    def update(self) -> None:
        """
        Updates the attributes of the optimization object based on the current optimization status.
        If the optimization run is in progress, it creates a result object with the last solution and fitness.
        If the optimization run is finished, it creates the final results, sets the status to finished, updates the statistics, and clears the resources.
        """
        if self.process and self.process.exception:
            self.status = Status.FAILED

        if self.status != Status.RUNNING:
            return

        self.statistics.time_run_started = self.temp_dict.get(Statistics.time_run_started_key())

        # if there are no generations produced yet, skip updating the result
        if self.temp_populations:
            unique_solutions = utils.get_unique_solutions(self.temp_populations[-1].solutions)

            if len(unique_solutions) > 1:
                pareto_optimal_solutions = utils.filter_pareto_optimal_solutions(unique_solutions)
                self.problem.update_result(pareto_optimal_solutions)
            else:
                self.problem.update_result(unique_solutions)

        if not self.process.is_alive():
            self.status = Status.FINISHED
            self.statistics.time_run_stopped = self.temp_dict.get(Statistics.time_run_stopped_key())
            self.statistics.populations = self.temp_populations

            self.temp_dict.clear()
            self.temp_populations = []
