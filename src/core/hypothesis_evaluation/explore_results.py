import glob

import pandas as pd

from src.utils.tools import extract_experiment_name, find_query_name
from utils.results import iterate_in_results

error_arg = "fdr_by"
corrected_err_column = f"p-value {error_arg}"
from statsmodels.stats.multitest import multipletests
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler

scaller = MinMaxScaler()

independence_test_threshold = 0.05

error_arg = "fdr_by"

corrected_err_column = f"p-value {error_arg}"


def generate_plot_data(result, approach=1, alpha=0.05, optimize=False, factor=1):
    # Test correction
    correction = multipletests(result["p-value"], method=error_arg, alpha=alpha)
    result[corrected_err_column] = correction[1]
    result = result[correction[0]]
    if result.shape[0] == 0:
        return pd.DataFrame()

    budget_scale = 1
    if approach == 1:
        result = result.sort_values(corrected_err_column)
        # budget_scale = 0.5
    else:
        result = result.sort_values(["e_size", "h_size"], ascending=False)

    if optimize:
        a = result[~result["h"].duplicated()]
        b = result[~result.e.isin(a.e)]
        b = b[~b.e.duplicated()]
        result = pd.concat([a, b])
    # Budget
    budget = result[corrected_err_column].cumsum().max()
    budget = budget * factor

    result["budget"] = budget - result[corrected_err_column].cumsum()
    result["budget (NN)"] = result["budget"]
    result["budget"] = (result["budget"] - result["budget"].min()) / (result["budget"].max() - result["budget"].min())
    result = result[result["budget"] >= 0]

    # Coverage
    index_e = result["e"].drop_duplicates(keep="first").index
    index_h = result["h"].drop_duplicates(keep="first").index
    n_e = result["De_size"].unique()[0]
    n_h = result["Dh_size"].unique()[0]

    result.loc[index_e, "coverage_e"] = result.loc[index_e, "e_size"] / n_e
    result.loc[index_h, "coverage_h"] = result.loc[index_e, "h_size"] / n_h
    result["#results"] = 1
    result["#results"] = result["#results"].cumsum()
    result["coverage (#results)"] = result["#results"] / result.shape[0]
    result["coverage_e"] = result["coverage_e"].fillna(0)
    result["coverage_h"] = result["coverage_h"].fillna(0)
    result["coverage (size)"] = (result["coverage_h"] + result["coverage_e"]).cumsum() / 2
    plt.rcParams["font.size"] = "30"

    # plot_index = "coverage (#results)"
    plot_data = result[
        [corrected_err_column, "budget", "coverage (#results)", "#results", "coverage (size)", "budget (NN)", "e", "h"]]
    return plot_data


def get_plot_data(files, approach=1, alpha=0.05, optimize=False, factor=1):
    plots = pd.DataFrame()
    for i in files:
        result = pd.read_csv(i, index_col=0)
        pivot, seg = extract_experiment_name(i.split("/")[-1])
        try:
            plot_data = generate_plot_data(result, approach=approach, alpha=alpha, optimize=optimize, factor=factor)
        except Exception as e:
            print(e)
            print(i)
            continue
        plot_data["pivot"] = pivot
        plot_data["segmentation"] = seg.replace("[", "").replace(']', "").replace("'", '')
        plots = pd.concat([plots, plot_data])
    plots.segmentation = plots.segmentation.apply(
        lambda x: x.replace("10000", "10K").replace("1000", "1K").replace("2000", "2K").replace("5000", "5K"))
    plots["alpha"] = alpha
    plots["factor"] = factor
    if approach == 1:
        plots['approach'] = "p-value-based"
    else:
        plots['approach'] = "coverage-based"
    return plots


pd.options.mode.chained_assignment = None  # default='warn'


def segmentation_format(x):
    if 'Window' not in x:
        return x
    try:
        int(x.split('_')[1])
        if '000' in x:
            x = x[:-3] + "K"
        return x.replace("Window", "PWindow")
    except:
        return x.replace("Window", "TWindow")


def generate_stats(files_filter=".", avoid_filter=None, approach=1, alpha=0.5):
    files = glob.glob('experiments/results/*.csv')
    if avoid_filter:
        files = [i for i in files if avoid_filter not in i]
    files = [i for i in files if files_filter in i]
    files = iterate_in_results(files)
    df_stats = pd.DataFrame()
    for name_1, result in files:
        name = name_1.replace('.csv', "").replace("pivot: temporal ['2018-12-17', '2019-02-28']",
                                                  "pivot: promotions [Before,After]")
        try:
            stats = generate_stats_result(result, name, approach=approach, alpha=alpha)
            stats["file"] = name_1
        except:
            continue
        name = name.replace("experiments/results/", "")
        stats["pivot"] = extract_experiment_name(name)[0].split()[0]
        seg = extract_experiment_name(name)[1]
        if 'Trend' in seg:
            seg = seg.split()[0]
        else:
            seg = '_'.join(seg.split()).replace(',_', ",").replace("'", "")
            if "," not in seg:
                seg = seg.replace('[', '').replace("]", "")
        stats["z_test"] = 'ztest' in name
        stats["segmentation"] = segmentation_format(seg)
        df_stats = pd.concat([df_stats, stats])
    df_stats["alpha"] = alpha
    df_stats["dataset"] = df_stats["pivot"].apply(lambda x: x.split("_")[0])
    df_stats["pivot"] = df_stats["pivot"].apply(lambda x: x.split("_")[-1])
    df_stats = df_stats[df_stats["pivot"] != "Trend"]
    df_stats['query#'] = df_stats.apply(lambda x: find_query_name(x["pivot"], x["segmentation"]), axis=1)
    df_stats = df_stats.set_index(["dataset", "query#", "pivot", "segmentation", "alpha"]).sort_index()
    return df_stats


def generate_stats_result(result, name, approach=1, alpha=0.5):
    n = result.shape[0]
    n_e = result["#e"].iloc[0]
    n_h = result["#h"].iloc[0]

    # khi square test results
    result = result[result["chi-squared test"] >= independence_test_threshold]

    plot_data = generate_plot_data(result.copy(), approach=approach, alpha=alpha)
    if plot_data.shape[0] != 0:
        coverage = plot_data.dropna().index.max()
    else:
        coverage = 0

    n_results = 0
    min_pvalue = 0
    budget = 0
    size_bonfero = 0

    if result.shape[0] >= 2:
        # Bonferoni
        size_bonfero = sum(multipletests(result["p-value"], alpha=alpha, method="bonferroni")[0])

        # FDR
        a = multipletests(result["p-value"], method=error_arg, alpha=alpha)
        result[corrected_err_column] = a[1]
        n_results = sum(a[0])
        min_pvalue = min(a[1])
        budget = result[a[0]][corrected_err_column].sum()

    columns = ["#(h,e)", '#e', '#h', "#results", "#result(Bonferoni)", "coverage", "min-p", "budget"]
    res = pd.DataFrame(
        [(n, n_e, n_h, n_results, size_bonfero, coverage, min_pvalue, budget)],
        columns=columns)
    return res


def fix_legend(ax, titles):
    ax.legend(loc=3, title=titles, borderpad=0, labelspacing=0, markerscale=6, handletextpad=-0.5)

    # Legend edit
    legend = ax.get_legend()
    legend.get_title().set_position((0, 50))  # -10 is a guess
    legend.get_frame().set_linewidth(3)
    legend.get_frame().set_edgecolor("black")


def plot_result(plots, segmentations, pivot, plot_columns="segmentation", index_col="coverage (#result)",
                font_size="30", remove_duplicates=True):
    i = plots[plots["pivot"].isin(pivot)]
    i = i.reset_index(drop=True)
    plt.rcParams["font.size"] = font_size
    i = i[i.segmentation.isin(segmentations)]
    fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=(20, 8))

    if remove_duplicates:
        i = i[~i[index_col].duplicated()]
        i = i.pivot(index=index_col, columns=plot_columns, values="budget").sort_index()

        for idx, col in enumerate(i.columns):
            i.reset_index().plot.scatter(x=index_col, y=col, ax=ax, label=col, color=f'C{idx}')
    else:
        for idx, (seg, ii) in enumerate(i.groupby(plot_columns)):
            ii.plot.scatter(x=index_col, y="budget", ax=ax, label=seg, color=f'C{idx}')

    ax.legend(loc=3, prop={'size': 15})
    ax.set_ylabel('Risk capital')
    x_title = "#Results"
    if index_col == "coverage (size)":
        x_title = "Coverage"
    ax.set_xlabel(x_title)

    # ax2 = ax.twinx()

    fix_legend(ax, titles=plot_columns)

    plt.ylabel("Risk capital")
    plt.xlabel(x_title)
