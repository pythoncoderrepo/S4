import pandas as pd

from src.core.segmentation_handler import CumulativeSegmentsSplitter
from src.utils.tools import format_temporal_pivot_name


class PivotHandler:

    def Demographics_pivot(self, df, pivot_arg):
        """
        Example : (('males',r),('females',t))
        """
        unique_values = df[pivot_arg].drop_duplicates().dropna().shape[0]
        assert unique_values == 2, f'{unique_values}> 2 tuples (R,T) are possible ' \
                                   f'for demographic segmentation {pivot_arg}'
        return df.groupby(pivot_arg)

    def temporal_pivot(self, df, pivot_arg):
        print(pivot_arg)
        if pivot_arg[0] == "is_holiday":
            reference_set = df[df.is_holiday]
            test_set = df[~df.is_holiday]
            print(test_set.shape, reference_set.shape)
            return ("Holidays", reference_set), ("Non-Holidays", test_set)

        pivot_arg = [pd.to_datetime(i) for i in pivot_arg]
        if len(pivot_arg) != 2:
            pivot_arg.append(pivot_arg[-1])
        reference_set = df[df.index <= pivot_arg[0]]
        test_set = df[df.index >= pivot_arg[1]]
        return (format_temporal_pivot_name(pivot_arg[0], "<"), reference_set), (
            format_temporal_pivot_name(pivot_arg[1], ">"), test_set)

    def trend_pivot(self, df, pivot_arg=["Up", "Other"]):
        splitter = CumulativeSegmentsSplitter()

        result = splitter.split(df, arg="Up")
        res = []
        for i in result:
            if len(i) < 3:
                continue
            [res.append(ii) for ii in i]
        index1 = df.index.isin(res)
        result = splitter.split(df, arg="Down")
        res = []
        for i in result:
            if len(i) < 3:
                continue
            [res.append(ii) for ii in i]
        index2 = df.index.isin(res)
        return (pivot_arg[0], df[index1]), (pivot_arg[1], df[index2])

    def pivot(self, pivot_type, data, pivot_arg):
        if pivot_type == 'Demographics':
            return self.Demographics_pivot(data, pivot_arg)

        if pivot_type == 'Promotion':
            return self.temporal_pivot(data, pivot_arg)

        if pivot_type == 'Trend':
            return self.trend_pivot(data, pivot_arg)
        if pivot_type is None:
            return (None, pd.DataFrame(pivot_arg)), ("All", data)
        raise Exception("Undefined mode")
