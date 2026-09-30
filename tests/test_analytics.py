"""Reproducible sanity checks for source integrity and interactive analysis."""

from pathlib import Path

import pandas as pd
import pytest

from analytics import filter_insurance_data, region_summary, validate_insurance_data

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "insurance.csv"


@pytest.fixture
def records():
    return validate_insurance_data(pd.read_csv(DATA_PATH))


def test_source_data_integrity(records):
    assert records.shape == (1338, 7)
    assert records.isna().sum().sum() == 0
    assert records.duplicated().sum() == 1
    assert records["age"].min() == 18
    assert records["age"].max() == 64


def test_unfiltered_view_preserves_all_rows(records):
    output = filter_insurance_data(
        records, (18, 64), (15.5, 53.5),
        ["no", "yes"], sorted(records["region"].unique().tolist())
    )
    assert len(output) == len(records)
    assert output.duplicated().sum() == 1


def test_combined_filters_restrict_every_field(records):
    output = filter_insurance_data(
        records, (30, 40), (25.0, 35.0), ["yes"], ["northeast"]
    )
    assert not output.empty
    assert output["age"].between(30, 40).all()
    assert output["bmi"].between(25, 35).all()
    assert output["smoker"].eq("yes").all()
    assert output["region"].eq("northeast").all()


def test_no_groups_selected_returns_empty(records):
    output = filter_insurance_data(
        records, (18, 64), (15.5, 53.5), [], list(records["region"].unique())
    )
    assert output.empty


def test_regional_aggregation_matches_pandas(records):
    result = region_summary(records, "Median")
    assert result["observations"].sum() == len(records)
    northeast = result.set_index("region").loc["northeast", "charge_value"]
    assert northeast == pytest.approx(records.loc[records.region.eq("northeast"), "charges"].median())


def test_wrong_schema_is_detected(records):
    with pytest.raises(ValueError, match="missing columns"):
        validate_insurance_data(records.drop(columns=["charges"]))


def test_wrong_statistic_is_rejected(records):
    with pytest.raises(ValueError, match="statistic"):
        region_summary(records, "Maximum")
