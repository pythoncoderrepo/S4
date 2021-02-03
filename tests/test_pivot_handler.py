from datetime import datetime

import pandas as pd
import pytest

from src.core.pivot_handler import PivotHandler
from src.models.models import get_data


@pytest.mark.parametrize('pivot_type,arguments', [
    ("Demographics", ["gender"]),
    ("behavioral", ["Up", "Down"],),
    ("temporal", [datetime(2017, 12, 9), datetime(2017, 11, 16)],),

])
def test_pivot_handler(pivot_type, arguments):
    df = get_data()
    pivot_handler = PivotHandler()
    (_, reference_set), (_, test_set) = pivot_handler.pivot(pivot_type, df, arguments)
    assert isinstance(reference_set, pd.DataFrame)
    assert isinstance(test_set, pd.DataFrame)


if __name__ == '__main__':
    pytest.main(["-vv", __file__])
