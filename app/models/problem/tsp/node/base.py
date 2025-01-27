from abc import ABC

from pydantic import BaseModel


class NodeBase(ABC, BaseModel):
    node_id: int
