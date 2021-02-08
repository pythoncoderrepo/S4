from itertools import product

import pandas as pd

from source_code.core.hypothesis_evaluation.test_handler import run_tests_for
from source_code.utils.tools import experiment_name


def run_experiments(pivots, segmentations, df, test_type="mean", test_arg="Two-Samples", error_correction_test="FDR",
                    threshold=0.05,
                    plot=False, output_prefix=""):
    names = []
    print("EXPT")
    for (pivot_type, pivot_arg), (segmentation_type, segmentation_arg) in product(pivots, segmentations):
        if pivot_type is None:
            test_arg = 'One-Sample'

        name = experiment_name(pivot_type, pivot_arg, segmentation_type, segmentation_arg)
        result = run_tests_for(df, pivot_type, pivot_arg, segmentation_type, segmentation_arg, test_type, test_arg,
                               error_correction_test, threshold, plot)
        if not len(result):
            print("No result found ", name)
            continue
        names.append(f"experiments/results/{output_prefix}" + name + ".csv")
        pd.DataFrame(result).to_csv(names[-1])
        print("DDDone", name)
    return names
