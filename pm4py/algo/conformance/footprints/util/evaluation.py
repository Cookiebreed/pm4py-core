from pm4py.algo.discovery.footprints.outputs import Outputs
from collections import Counter
from typing import List, Dict, Any


DFG = "dfg"
FOOTPRINTS_KEY = "footprints"
START_ACTIVITIES = "start_activities"
END_ACTIVITIES = "end_activities"
SEQUENCE = "sequence"
PARALLEL = "parallel"
IS_FOOTPRINTS_FIT = "is_footprints_fit"


def fp_fitness(fp_log, fp_model, conf_results, parameters=None):
    """
    Calculates the footprints fitness provided the footprints of the log,
    and the result of footprints conformance (applied to the entire log)

    Parameters
    ---------------
    fp_log
        Footprints of the log
    fp_model
        Footprints of the model
    conf_results
        Footprints conformance (applied to the entire log)
    parameters
        Parameters of the algorithm

    Returns
    ---------------
    fitness
        Fitness value (between 0.0 and 1.0)
    """
    if parameters is None:
        parameters = {}

    fit_traces = None
    if isinstance(conf_results, list):
        fit_traces = len([x for x in conf_results if x[IS_FOOTPRINTS_FIT]])/len(conf_results) * 100.0

    fp_log = flatten_fp(fp_log)
    conf_results = flatten_conf(conf_results)

    dfg = fp_log[DFG]
    num_sequence_log = len(fp_log[SEQUENCE])
    num_parallel_log = len(fp_log[PARALLEL])
    num_start_activities_log = len(fp_log[START_ACTIVITIES])
    num_end_activities_log = len(fp_log[END_ACTIVITIES])
    num_start_activities_dev = len(conf_results[START_ACTIVITIES])
    num_end_activities_dev = len(conf_results[END_ACTIVITIES])
    footprints = conf_results[FOOTPRINTS_KEY]

    if dfg:
        sum_dfg = float(sum(x for x in dfg.values()))
        sum_dev = float(sum(dfg[x] for x in footprints))

        fitness = ((1.0 - sum_dev / sum_dfg) * (num_sequence_log + num_parallel_log) + (
                    num_start_activities_log + num_end_activities_log - num_start_activities_dev - num_end_activities_dev)) / (
                           num_sequence_log + num_parallel_log + num_start_activities_log + num_end_activities_log)
    else:
        # return fitness 1.0 if DFG is empty
        fitness = 1.0

    if fit_traces is not None:
        return {"perc_fit_traces": fit_traces, "log_fitness": fitness}

    return fitness


def fp_precision(fp_log, fp_model, parameters=None):
    """
    Calculates the footprints based precision provided the two footprints
    of the log and the model.

    Parameters
    --------------
    fp_log
        Footprints of the log
    fp_model
        Footprints of the model
    parameters
        Parameters of the algorithm

    Returns
    -------------
    precision
        Precision value (between 0 and 1)
    """
    if parameters is None:
        parameters = {}

    fp_log = flatten_fp(fp_log)
    fp_model = flatten_fp(fp_model)

    log_configurations = fp_log[Outputs.SEQUENCE.value].union(fp_log[Outputs.PARALLEL.value])
    model_configurations = fp_model[Outputs.SEQUENCE.value].union(fp_model[Outputs.PARALLEL.value])

    if model_configurations:
        return float(len(log_configurations.intersection(model_configurations))) / float(len(model_configurations))

    # return precision 1.0 if model configurations are empty
    return 1.0


def flatten_fp(fp: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Flattens the trace-based footprints to the footprints of the overall log

    Parameters
    ---------------
    fp
        Trace-based footprints

    Returns
    --------------
    log_fp
        Overall log footprints
    """
    if isinstance(fp, list):
        res = {DFG: Counter(), SEQUENCE: set(), PARALLEL: set(), START_ACTIVITIES: set(), END_ACTIVITIES: set()}
        for el in fp:
            for x, y in el[DFG].items():
                res[DFG][x] += y
            res[SEQUENCE] = res[SEQUENCE].union(el[SEQUENCE])
            res[PARALLEL] = res[PARALLEL].union(el[PARALLEL])
            res[START_ACTIVITIES] = res[START_ACTIVITIES].union(el[START_ACTIVITIES])
            res[END_ACTIVITIES] = res[END_ACTIVITIES].union(el[END_ACTIVITIES])
        return res
    return fp


def flatten_conf(conf: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Flattens the trace-based conformance checking results (obtained using footprints) to the conformance checking
    results on the overall log

    Parameters
    ----------------
    conf
        Trace-based conformance checking results

    Returns
    ----------------
    log_conf
        Overall log conformance checking results
    """
    if isinstance(conf, list):
        res = {FOOTPRINTS_KEY: set(), START_ACTIVITIES: set(), END_ACTIVITIES: set()}
        for el in conf:
            res[FOOTPRINTS_KEY] = res[FOOTPRINTS_KEY].union(el[FOOTPRINTS_KEY])
            res[START_ACTIVITIES] = res[START_ACTIVITIES].union(el[START_ACTIVITIES])
            res[END_ACTIVITIES] = res[END_ACTIVITIES].union(el[END_ACTIVITIES])
        return res
    return conf
