import enum

from app.models.framework.pygad.custom.mutation.shift1 import shift_mutation_1
from app.models.framework.pygad.custom.mutation.shift2 import shift_mutation_2


class CustomMutationEnum(enum.Enum):

    SHIFT_1 = ('shift1', shift_mutation_1)
    SHIFT_2 = ('shift2', shift_mutation_2)