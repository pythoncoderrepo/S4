import pandas as pd


def iterate_in_results(files):
    for i in files:
        result = pd.read_csv(i, index_col=0)
        yield i, result
