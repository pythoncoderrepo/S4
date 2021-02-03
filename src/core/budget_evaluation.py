def compute_result_budget(result, budget, corrected_err_column, plot=False, title=None, local=False):
    r = [i for i in result.columns if "e_" in i][0]
    result = result.set_index([corrected_err_column, r]).sort_index()

    ## Remove duplicates in index
    if not local:
        result = result[~result.index.get_level_values(1).duplicated(keep="first")]
    result["p-value"] = result.index.get_level_values(0)

    # Compute budget
    def compute_budget(result, budget):
        index = result.index
        for i in index:
            result.loc[i, "budget"] = budget - result.loc[:i].shape[0] * result.loc[:i, 'p-value'].max()

    compute_budget(result, budget)

    # coverage
    result["coverage"] = 1
    if local:
        result.loc[result.index.get_level_values(1).duplicated(), "coverage"] = 1
    result["coverage"] = result["coverage"].cumsum() / result["#h"].unique()[0]

    # plot
    plot_data = result[result["budget"] >= 0].reset_index()[["coverage", "budget"]]
    plot_data.loc[len(plot_data)] = [0, budget]
    plot_data = plot_data.sort_values("coverage")
    if plot:
        ax = plot_data.plot.line(x="coverage", y="budget", title=title, figsize=(20, 8))
    return plot_data
