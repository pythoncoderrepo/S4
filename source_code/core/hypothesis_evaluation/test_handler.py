import time
from itertools import product

import pandas as pd

import config
from config import THRESHOLD_INDEPENDENT_TEST
from source_code.core.hypothesis_evaluation.test_evaluation import StatisticalTestHandler
from source_code.core.pivot_handler import PivotHandler
from source_code.core.segmentation_handler import SegmentationHandler
from source_code.models.models import get_data
from source_code.utils.tools import format_approach_name, find_query_name


def fix_path_name(exp_path):
    exp_path = exp_path.replace("'", "").replace("[", "").replace("]", "").strip().replace(" ", "").replace(",", "_")
    return exp_path


def format_exp_name(dataset, query, pivot_arg, segmentation_arg, approach, alpha, max_coverage):
    exp_name = f'{dataset}_{query}_{pivot_arg}_{segmentation_arg}_{approach}_{alpha}_{max_coverage}'
    exp_name = exp_name.replace(" ", "").replace(",", "_")
    exp_name = fix_path_name(exp_name)
    return exp_name


def fix_pivot_arg(pivot_arg):
    try:
        pivot_arg = [i.strftime('%Y-%m-%d') for i in pivot_arg]
    except:
        pass
    return pivot_arg


def run_tests_for(dataset, pivot_type, pivot_arg, segmentation_type, segmentation_arg, test_type, test_arg, approach,
                  alpha):
    pivot_handler = PivotHandler()
    segmentation_handler = SegmentationHandler()
    test_handler = StatisticalTestHandler()
    config.segmentation_type = segmentation_type
    config.pivot_arg = pivot_arg
    config.segmentation_arg = segmentation_arg
    query = find_query_name(pivot_type, segmentation_type)

    df = get_data(dataset=dataset)
    df["purchase"] = 1

    # Pivot  + Segment
    start_time = time.time()
    (r_name, Dh), (t_name, De) = pivot_handler.pivot(pivot_type, df, pivot_arg)
    holdout_segments, exploratory_segments = segmentation_handler.segment(segmentation_type, Dh, De, segmentation_arg)
    time1 = time.time() - start_time
    len_e = len(De)
    len_h = len(Dh)
    print('Segmentation', len(holdout_segments), len(exploratory_segments))

    # Cartesian product +  Evaluate all cases + Filter results
    start_time = time.time()
    cases = product(exploratory_segments, holdout_segments)
    result = test_handler.evaluate(test_type, cases, test_arg)
    result = result[~result["p-value"].isna()]
    result = result[result["chi-squared test"] > THRESHOLD_INDEPENDENT_TEST]
    time2 = time.time() - start_time

    if config.SAVE_RESULTS:
        exp_name = format_exp_name(dataset, query, fix_pivot_arg(pivot_arg), segmentation_arg, approach, alpha, None)
        result.to_csv(f"{config.INTERMEDIATE_RESULTS_FOLDER}/{exp_name}.csv")
    results_independent = result.shape[0]

    def compute_stats(h_seg, e_seg, result):
        candidates = len(h_seg) * len(e_seg)
        min_p_value = result["p-value"].min()
        r = result.drop(["chi-squared test"], axis=1).copy()
        r = get_results_approach(approach, r, len_e, len_h, alpha=alpha, method="fdr_b")
        result_huchberg = r.shape[0]
        return candidates, min_p_value, result_huchberg

    stats = compute_stats(holdout_segments, exploratory_segments, result, )
    result = result.drop(["chi-squared test"], axis=1)

    # error correction + keep good results
    start_time = time.time()
    result = get_results_approach(approach, result, len_e, len_h, alpha=alpha)
    time3 = time.time() - start_time

    # Stats
    max_coverage = round(result.coverage.max(), 4)
    budget = result["p-value"].sum()
    results_s4 = result.shape[0]
    approach = format_approach_name(approach)
    pivot_arg = fix_pivot_arg(pivot_arg)
    exp_name = format_exp_name(dataset, query, pivot_arg, segmentation_arg, approach, alpha, max_coverage)
    time1 = round(time1, 4)
    time2 = round(time2, 4)
    time3 = round(time3, 4)
    try:
        max_coverage = round(max_coverage, 4)
    except:
        pass
    if config.SAVE_RESULTS:
        exp_path = f'{dataset}/{query}'
        exp_path = fix_path_name(exp_path)
        results_output = f'{config.RESULTS_OUTPUT_PATH}/{exp_path}/{exp_name}.csv'
        time_output = f'{config.TIME_OUTPUT_PATH}/{exp_name}.csv'
        result.to_csv(results_output, index=False)
        stats_data = [dataset, query, pivot_arg, segmentation_arg, approach, alpha, time1, time2, time3,
                      *stats, max_coverage, results_s4, budget, results_independent]
        pd.DataFrame(stats_data).to_csv(time_output, index=None)
        print("\n ### Done: ", exp_name)
    return result, exp_name, [time1, time2, time3, *stats, max_coverage]


def get_results_approach(approach, result, len_e, len_h, alpha=0.05, method="fdr_by"):
    coverage = 0
    res = []

    m = result.shape[0]

    if approach == 1:
        result = result.sort_values("p-value").reset_index(drop=True)
    else:
        result = order_coverage(result).reset_index(drop=True)
    result["e_duplicated"] = result.e.duplicated()
    result["h_duplicated"] = result.h.duplicated()
    for n, e, e_size, h, h_size, p, e_duplicated, h_duplicated in result.itertuples():
        limit = compute_limit(alpha, n + 1, m, method)

        if p >= limit:
            if approach == 1:
                break
            else:
                continue

        if not e_duplicated:
            coverage += e_size / len_e
        if not h_duplicated:
            coverage += h_size / len_h
        res.append((len(res) + 1, coverage / 2, p))
    df_results = pd.DataFrame(res, columns=["result", "coverage", "p-value"])
    df_results["capitalRisk"] = df_results["p-value"].cumsum()
    df_results["capitalRisk"] = df_results["capitalRisk"].max() - df_results["capitalRisk"]
    return df_results


def order_coverage(res):
    res["coverage"] = res.e_size * ~res.e.duplicated() + res.h_size * ~res.h.duplicated()
    res = res[res.coverage > 0]
    return res.sort_values("coverage", ascending=False).drop('coverage', axis=1)


def compute_limit(alpha, n, m, method="fdr_by"):
    if method == "fdr_by":
        return alpha * n / (m * sum(1 / ii for ii in range(1, n + 1)))
    if method == "fdr_b":
        return alpha / m
