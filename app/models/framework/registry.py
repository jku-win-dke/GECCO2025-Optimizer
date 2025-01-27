from app.models.base_mapper import BaseMapper
from .pygad.mapper import PygadFrameworkMapper


class FrameworkMapperRegistry:
    _mapper_registry: dict[str, BaseMapper] = {
        "pygad": PygadFrameworkMapper,
    }

    @staticmethod
    def get_mapper(framework_type: str) -> BaseMapper:
        """
        Gets the mapper for the specified optimization framework type.
        :param framework_type: Optimization framework type
        :return: Mapper for the specified optimization framework type
        """
        return FrameworkMapperRegistry._mapper_registry.get(framework_type)
