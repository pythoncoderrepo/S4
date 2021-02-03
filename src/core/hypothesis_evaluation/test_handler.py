from itertools import product

import matplotlib.pyplot as plt

from src.core.hypothesis_evaluation.test_evaluation import StatisticalTestHandler, StatisticalTestErrorControl
from src.core.pivot_handler import PivotHandler
from src.core.segmentation_handler import SegmentationHandler
from src.utils.tools import update_column_names, format_pivot_name, format_title, format_segmentation_name


def run_tests_for(df, pivot_type, pivot_arg, segmentation_type, segmentation_arg, test_type, test_arg,
                  error_correction_test, threshold=0.05, plot=False):
    pivot_handler = PivotHandler()
    segmentation_handler = SegmentationHandler()
    test_handler = StatisticalTestHandler()
    test_error_control = StatisticalTestErrorControl()

    # Pivot
    (r_name, Dh), (t_name, De) = pivot_handler.pivot(pivot_type, df, pivot_arg)

    # Segment
    holdout_segments, exploratory_segments = segmentation_handler.segment(segmentation_type, Dh, De, segmentation_arg)
    print('Segmentation', len(holdout_segments), len(exploratory_segments))

    # Cartesian product
    cases = product(exploratory_segments, holdout_segments)

    # Evaluate all cases
    result = test_handler.evaluate(test_type, cases, test_arg)

    # Add Details
    result["Dh_size"] = len(Dh)
    result["De_size"] = len(De)
    result = result.rename(columns=update_column_names([r_name, t_name])).dropna()

    result["#h"] = len(holdout_segments)
    result["#e"] = len(exploratory_segments)

    result["segmentation"] = format_segmentation_name(segmentation_type, segmentation_arg)
    result["pivot"] = format_pivot_name(pivot_type, pivot_arg)
    result["test"] = "_".join(str(i) for i in [test_type])

    result = result.sort_values("p-value")

    # test_error_control.compute_adjusted_pvalue(result, "FDR", threshold)

    if plot:
        res = result[[i for i in result.columns if "p-value" in i]]
        title = format_title(pivot_type, pivot_arg, segmentation_type, segmentation_arg, test_type, test_arg,
                             error_correction_test, threshold)
        res.plot.hist(stacked=True, bins=100, figsize=(20, 8), title=title)
        plt.show()
    return result
