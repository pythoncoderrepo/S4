from datetime import datetime

import pandas as pd

from config import ROOT_DIR
from source_code.utils.tools import encode_age

columns_to_keep = ['article_id', "gender", "cust_id", "location", "age"]


def get_dataset_amazon(article_id):
    df = pd.read_csv(f"{ROOT_DIR}/datasets/AMAZON_DIGITAL_MUSIC.csv", header=None)
    df.columns = ["article_id", "cust_id", "rating", "transaction_date"]
    df.index = pd.to_datetime(pd.to_datetime(df.transaction_date, unit="s").dt.date, )
    index = (df.index.date >= datetime(2015, 1, 1).date()) & (df.index.date <= datetime(2018, 1, 1).date())
    df = df[index]
    df["purchase"] = 1
    return df


def get_dataset_sales(article_id):
    df = pd.read_csv(f"{ROOT_DIR}/datasets/SALES_Kaggle.csv")
    df.columns = [i.lower() for i in df.columns]
    df.columns = ["cust_id", "_", "date", "purchase", "is_holiday"]
    df.index = pd.to_datetime(df.date)
    df.sort_index(inplace=True)
    df["purchase"] = 1
    return df[["cust_id", "purchase", "is_holiday"]]


def get_data(article_id=None, dataset="retail"):
    if dataset == "Tafeng":
        return get_dataset_tafeng(article_id)
    elif dataset == "Amazon":
        return get_dataset_amazon(article_id)
    elif dataset == "Sales":
        return get_dataset_sales(article_id)
    else:
        return get_dataset_retail(article_id)


def get_dataset_retail(article_id):
    df = pd.read_csv(f"{ROOT_DIR}/datasets/RETAIL.csv")
    df.columns = map(str.lower, df.columns)
    if article_id:
        df = df[df.article_id == article_id]
    # TODO : Fix time issue
    df.index = pd.to_datetime(pd.to_datetime(df.transaction_date).dt.date)
    df = df.rename(columns={"sex": "gender", "departement": "location"})
    df["purchase"] = 1
    return df[columns_to_keep]


def get_dataset_tafeng(article_id):
    df = pd.read_csv(f"{ROOT_DIR}/datasets/TAFENG_Kaggle.csv")
    df.columns = [i.lower() for i in df.columns]
    columns = {
        "age_group": "age",
        "transaction_dt": "transaction_date",
        "product_id": "article_id",
        'customer_id': "cust_id"
    }
    df.rename(columns=columns, inplace=True)
    df.index = pd.to_datetime(pd.to_datetime(df.transaction_date).dt.date)
    df["purchase"] = 1

    df["age-range"] = df.age.apply(encode_age)
    return df


if __name__ == "__main__":
    print(get_data(dataset="Retail").index.min())
    print(get_data(dataset="Tafeng").index.min())
    print(get_data(dataset="Sales").index.min())
    print(get_data(dataset="Amazon").index.min())
