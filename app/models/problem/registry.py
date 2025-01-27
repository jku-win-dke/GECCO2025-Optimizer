from .problem_mapper import ProblemMapper
from .tsp.mapper import TspMapper


class ProblemMapperRegistry:
    _mapper_registry: dict[str, ProblemMapper] = {
        "tsp": TspMapper
    }

    @staticmethod
    def get_mapper(problem_type: str) -> ProblemMapper:
        """
        Return the mapper for a particular optimization problem type.
        :param problem_type: Optimization problem type
        :return: Mapper of the optimization problem type
        """
        return ProblemMapperRegistry._mapper_registry.get(problem_type)
