import pandas as pd
from numpy import ndarray

import config


def format_split_name(df):
    if isinstance(df, ndarray):
        return df,
    if config.segmentation_type == "Demographics":
        if isinstance(config.segmentation_arg, list):
            return df[config.segmentation_arg].drop_duplicates().apply(lambda x: "_".join(str(i) for i in x))[0],
        return df[config.segmentation_arg].unique()[0],
    try:
        return df.index.min(),
    except:
        return df[0],


def encode_age(x):
    if x in [">65", '50-54', '60-64', "45-49", '40-44']:
        return ">40"
    else:
        return "<40"


def update_column_names(columns_names):
    args = columns_names.copy()
    return {
        "r": f"r_{args[0]}",
        "t": f"t_{args[1]}",
    }


def format_title(*args):
    return ' '.join(f'{i}' for i in args)


def format_temporal_pivot_name(name, prefix):
    return f"{prefix}{name.strftime('%Y-%m-%d')}"


def format_segmentation_name(segmentation_type, segmentation_arg):
    if segmentation_type == "Window":
        return f'{segmentation_type}_{segmentation_arg}'
    return segmentation_type


def format_pivot_name(pivot_type, pivot_arg):
    args = pivot_arg.copy()
    return pivot_type
    # if pivot_type == "Promotion":
    #    args = [i.strftime('%Y-%m-%d') for i in args]
    #       return 'Promotion'
    # return f'{pivot_type}_{args}'


def experiment_name(pivot_type, pivot_arg, segmentation_type, segmentation_arg):
    try:
        pivot_arg = [i.strftime("%Y-%m-%d") for i in pivot_arg]
    except:
        pass
    return " ".join(
        str(i) for i in ["pivot:", pivot_type, pivot_arg, ", segmentation:", segmentation_type, segmentation_arg])


# experiment_name(pivot_type,pivot_arg,segmentation_type,segmentation_arg)

def extract_experiment_name(name):
    name = name.replace('.csv', "").replace("temporal ['2018-12-17', '2019-02-28']", "promotion [Before,After]")
    name = name.replace('.csv', "").replace("Tafeng_Promotion ['2001-01-24', '2001-01-24']",
                                            "Tafeng_Promotion [Before,After]")
    pivot = name.split(", segmentation")[0].replace("pivot: ", "").strip()
    segmentation = name.split(", segmentation:")[1].replace("segmentation:", "").strip()
    return pivot, segmentation


def format_approach_name(approach):
    if approach == 1:
        return "p-value-based"
    return "coverage-based"


def find_query_name(pivot, segmentation):
    pivot = str(pivot).replace("Retail", "")
    if pivot == "Trend":
        return "Q"
    if pivot in ["Promotion"]:
        if 'Window' in segmentation:
            return "#Q3"
        if "Demographics" in segmentation:
            return "#Q4"
        if "Trend" in segmentation:
            return "#Q12"
        if 'None' in segmentation:
            return "#Q5"

    if pivot in ["Demographics"]:
        if 'Window' in segmentation:
            return "#Q9"
        if "Demographics" in segmentation:
            return "#Q7"
        if "Trend" in segmentation:
            return "#Q10"
        if 'None' in segmentation:
            return "#Q2"
    if pivot in ["None"]:
        if 'Window' in segmentation:
            return "#Q1"
        if "Demographics" in segmentation:
            return "#Q6"
        if "Trend" in segmentation:
            return "#Q8"
        if 'None' in segmentation:
            return "#Q11"
    print(pivot, " ,", segmentation)
    raise Exception("Not implemented")
