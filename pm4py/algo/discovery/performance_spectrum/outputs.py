from enum import Enum

import warnings

warnings.warn("pm4py.algo.discovery.performance_spectrum.outputs is deprecated. please use the algorithm entrypoint")


class Outputs(Enum):
    LIST_ACTIVITIES = "list_activities"
    POINTS = "points"