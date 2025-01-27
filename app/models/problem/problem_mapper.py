from abc import abstractmethod

from app.models.base_mapper import BaseMapper


class ProblemMapper(BaseMapper):

    @staticmethod
    @abstractmethod
    def to_result_dto(**kwargs):
        pass
