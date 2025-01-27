from typing import List

from app.models.base_mapper import BaseMapper
from app.models.obfuscation.registry import ObfuscationMapperRegistry
from app.models.problem.tsp.node.obj import Node
from app.models.problem.tsp.node_distances.mapper import NodeDistancesMapper
from app.models.problem.tsp.objective.dto import TspObjectiveDTO
from app.models.problem.tsp.objective.obj import TspObjective


class TspObjectiveMapper(BaseMapper):
    @staticmethod
    def to_dto(obj: TspObjective) -> TspObjectiveDTO:
        node_distances = [NodeDistancesMapper.to_dto(node_distance) for node_distance in obj.node_distances]

        obfuscation = None
        if obj.obfuscation:
            obfuscation = (ObfuscationMapperRegistry.get_mapper(obj.obfuscation.obfuscation_type)
                           .to_dto(obj=obj.obfuscation))

        return TspObjectiveDTO(
            objective_id=obj.objective_id,
            privacy_engine=obj.privacy_engine,
            node_distances=node_distances,
            obfuscation=obfuscation,
        )

    @staticmethod
    def from_dto(dto: TspObjectiveDTO, nodes: List[Node]) -> TspObjective:
        node_distances = [NodeDistancesMapper.from_dto(node_distance, nodes)
                          for node_distance in dto.node_distances]

        obfuscation = None
        if dto.obfuscation:
            obfuscation = (ObfuscationMapperRegistry.get_mapper(dto.obfuscation.obfuscation_type)
                           .from_dto(dto=dto.obfuscation))

        return TspObjective(
            objective_id=dto.objective_id,
            privacy_engine=dto.privacy_engine,
            node_distances=node_distances,
            obfuscation=obfuscation,
        )
