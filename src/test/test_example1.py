from pathlib import Path
import os
import pytest

# extend path for imports
filepath = Path(__file__).parents[1]
os.sys.path.append(str(filepath))
from example1 import CerealAnalysis  # noqa


@pytest.fixture
def ca():
    file_path = Path(__file__).parents[2]
    data_path = file_path / "data" / "cereal.csv"
    ca = CerealAnalysis(data_path)
    return ca


def test_cerealanalysis(ca):
    assert ca.n_rows == 77
    assert ca.n_cols == 16
    assert ca.columns.tolist() == [
        "name",
        "mfr",
        "type",
        "calories",
        "protein",
        "fat",
        "sodium",
        "fiber",
        "carbo",
        "sugars",
        "potass",
        "vitamins",
        "shelf",
        "weight",
        "cups",
        "rating",
    ]
    assert ca.numeric_cols.tolist() == [
        "calories",
        "protein",
        "fat",
        "sodium",
        "fiber",
        "carbo",
        "sugars",
        "potass",
        "vitamins",
        "shelf",
        "weight",
        "cups",
        "rating",
    ]
    assert ca.categorical_cols.tolist() == ["name", "mfr", "type"]
    assert ca.missing_values.sum() == 0
    assert ca.unique_values["name"] == 77
    assert ca.dtypes["name"] == "object"


def test_get_numeric_summary(ca):
    numeric_summary = ca.get_numeric_summary()
    assert numeric_summary["calories"]["mean"] == pytest.approx(106.88311, 0.00001)
    assert numeric_summary["protein"]["mean"] == pytest.approx(2.54545, 0.00001)
    assert numeric_summary["fat"]["mean"] == pytest.approx(1.01298, 0.00001)
    assert numeric_summary["sodium"]["mean"] == pytest.approx(159.67532, 0.00001)
    assert numeric_summary["fiber"]["mean"] == pytest.approx(2.15194, 0.00001)
    assert numeric_summary["carbo"]["mean"] == pytest.approx(14.59740, 0.00001)
    assert numeric_summary["sugars"]["mean"] == pytest.approx(6.92207, 0.00001)
    assert numeric_summary["potass"]["mean"] == pytest.approx(96.07792, 0.00001)
    assert numeric_summary["vitamins"]["mean"] == pytest.approx(28.24675, 0.00001)
    assert numeric_summary["shelf"]["mean"] == pytest.approx(2.20779, 0.00001)
    assert numeric_summary["weight"]["mean"] == pytest.approx(1.02961, 0.00001)
    assert numeric_summary["cups"]["mean"] == pytest.approx(0.8210, 0.0001)
    assert numeric_summary["rating"]["mean"] == pytest.approx(42.66570, 0.00001)


def test_get_missing_values(ca):
    missing_values = ca.get_missing_values()
    assert missing_values.sum() == 0
