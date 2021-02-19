import pandas  as pd
import pytest

from src.core.segmentation_handler import SegmentationHandler
from src.models.models import get_data


@pytest.mark.parametrize('segmentation_type,segmentation_arg', [
    ("Demographics", ["gender"]),
    ("Trend", ["Up"],),
    ("Window", 200,),

])
def test_segmentation_handler(segmentation_type, segmentation_arg):
    s = SegmentationHandler()
    df = get_data(4112)
    R, T = s.segment(segmentation_type, df[:10000], df[10000:], segmentation_arg)
    assert all(isinstance(r, pd.DataFrame) and isinstance(t, pd.DataFrame) for r, t in zip(R, T))


if __name__ == '__main__':
    pytest.main(["-vv", __file__])
