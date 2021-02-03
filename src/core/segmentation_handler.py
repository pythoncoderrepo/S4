import pandas as pd


class SegmentationHandler:
    def temporal_split(self, df, size):
        if len(df.columns) == 1:
            return df.values
        try:
            size = int(size)
            return [df.iloc[i:i + size, :] for i in range(0, len(df), size)]
        except:
            return [i for _, i in df.groupby(pd.Grouper(freq=size))]

    def demographic_segmentation(self, df, split_arg):
        return [i for _, i in df.groupby(split_arg)]

    def trend_segmentation(self, df, args):
        splitter = CumulativeSegmentsSplitter()
        result = []
        for i in splitter.split(df):
            if len(i) < 2:
                continue
            result.append(df[df.index.isin(i)])
        print("#Up trend", len(result))
        for i in splitter.split(df, arg="Down"):
            if len(i) < 2:
                continue
            result.append(df[df.index.isin(i)])
        print("#Down trend", len(result))
        return result

    def segment(self, segmentation_type, df_T, df_R, segmentation_arg):
        if segmentation_type == "Window":
            split_func = self.temporal_split
        elif segmentation_type == "Demographics":
            split_func = self.demographic_segmentation
        elif segmentation_type == "Trend":
            split_func = self.trend_segmentation
        elif segmentation_type is None:
            return [df_T], [df_R]
        else:
            raise Exception('Unknown segmentation type')

        test_result = split_func(df_T, segmentation_arg)
        if len(df_R.columns) == 1:  # None pivot
            return test_result, split_func(df_T, 1)
        return test_result, split_func(df_R, segmentation_arg)


class CumulativeSegmentsSplitter:
    def cumulate_segments(self, data, x, res, tolerance, arg="Up"):
        i = data.loc[res[-1], 'purchases']
        if arg == "Up":
            condition = x.difference <= - tolerance * (i.max() - i.min())
        else:
            condition = x.difference >= - tolerance * (i.max() - i.min())
        if condition:
            res.append([])
        res[-1].append(x.name)

    def split_cumulative_segments(self, df_transactions, tolerance, arg):
        """
        :param df_transactions:  DataFrame with dateIndex and columns ["purchases"]
        :param tolerance: float
        """
        res = [[]]
        df_transactions.apply(lambda x: self.cumulate_segments(df_transactions, x, res, tolerance, arg=arg), axis=1)
        return res

    def split(self, df, arg="Up", tolerance=0.3, freq="D"):
        data = df.groupby(pd.Grouper(freq=freq))["cust_id"].nunique().to_frame()
        data.columns = ["purchases"]
        data["difference"] = (data - data.shift()).values
        return self.split_cumulative_segments(data, tolerance, arg)
