import enum

from app.models.framework.pygad.custom.selection.npga import npga_selection
from app.models.framework.pygad.custom.selection.nsga2_modified import nsga2_selection_modified
from app.models.framework.pygad.custom.selection.spea2 import spea2_selection
from app.models.framework.pygad.custom.selection.tournament_binary import binary_pareto_tournament_selection
from app.models.framework.pygad.custom.selection.tournament_random import random_pareto_tournament_selection


class CustomSelectionEnum(enum.Enum):

    NSGA2_MODIFIED = ('nsga2_modified', nsga2_selection_modified)
    SPEA2 = ('spea2', spea2_selection)
    TOURNAMENT_BINARY = ('tournament_binary', binary_pareto_tournament_selection)
    TOURNAMENT_RANDOM = ('tournament_random', random_pareto_tournament_selection)
    NPGA = ('npga', npga_selection)
