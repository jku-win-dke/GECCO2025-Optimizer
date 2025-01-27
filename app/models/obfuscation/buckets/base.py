from abc import ABC
from typing import Literal

from pydantic import BaseModel


class BucketsObfuscationBase(ABC, BaseModel):
    obfuscation_type: Literal["buckets"] = "buckets"
    buckets: int
