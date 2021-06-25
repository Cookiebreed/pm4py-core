from enum import Enum
from typing import Optional, Dict, Any

import pandas as pd

from pm4py.util import constants, xes_constants, exec_utils


class Parameters(Enum):
    ACTIVITY_KEY = constants.PARAMETER_CONSTANT_ACTIVITY_KEY
    CASE_ID_KEY = constants.PARAMETER_CONSTANT_CASEID_KEY


INT_CASE_ACT_SIZE = "@@int_case_act_size"


def apply(df: pd.DataFrame, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, int]:
    """
    Associates to each activity (with at least one rework) the number of cases in the log for which
    the rework happened.

    Parameters
    ------------------
    df
        Dataframe
    parameters
        Parameters of the algorithm, including:
        - Parameters.ACTIVITY_KEY => the attribute to be used as activity
        - Parameters.CASE_ID_KEY => the attribute to be used as case ID

    Returns
    ------------------
    dict
        Dictionary associating to each activity the number of cases for which the rework happened
    """
    if parameters is None:
        parameters = {}

    activity_key = exec_utils.get_param_value(Parameters.ACTIVITY_KEY, parameters, xes_constants.DEFAULT_NAME_KEY)
    case_id_key = exec_utils.get_param_value(Parameters.ACTIVITY_KEY, parameters, constants.CASE_CONCEPT_NAME)

    df = df.copy()
    df = df[{activity_key, case_id_key}]
    df[INT_CASE_ACT_SIZE] = df.groupby([activity_key, case_id_key]).cumcount()
    df = df[df[INT_CASE_ACT_SIZE] > 0]
    df = df.groupby([activity_key, case_id_key]).last()
    ret = df.groupby(activity_key).size().to_dict()

    return ret