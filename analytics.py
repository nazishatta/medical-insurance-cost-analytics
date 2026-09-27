"""Pure, testable data operations for the Medical Insurance Cost Explorer."""

from __future__ import annotations

import pandas as pd

REQUIRED_COLUMNS = (
    "age", "sex", "bmi", "children", "smoker", "region", "charges"
)
NUMERIC_COLUMNS = ("age", "bmi", "children", "charges")
SMOKER_LABELS = {"no": "Non-smoker", "yes": "Smoker"}


def validate_insurance_data(frame: pd.DataFrame) -> pd.DataFrame:
    """Check the CSV schema; return a copy with validated numerical fields.

    Preserve every source row, including exact duplicates. The app reports data
    quality issues rather than silently removing observations.
    """
    missing_columns = [name for name in REQUIRED_COLUMNS if name not in frame]
    if missing_columns:
        raise ValueError(f"Dataset is missing columns: {', '.join(missing_columns)}")

    result = frame.loc[:, REQUIRED_COLUMNS].copy()
    for name in NUMERIC_COLUMNS:
        result[name] = pd.to_numeric(result[name], errors="raise")

    if result.isna().any().any():
        raise ValueError("Dataset contains missing values. Inspect the source CSV.")

    if (result["age"] < 0).any() or (result["bmi"] <= 0).any():
        raise ValueError("Dataset contains invalid age or BMI values.")
    if (result["charges"] < 0).any() or (result["children"] < 0).any():
        raise ValueError("Dataset contains invalid charges or children values.")

    # The provided dataset already uses lowercase codes; normalization makes
    # labels consistent while retaining the original set of observations.
    for name in ("sex", "smoker", "region"):
        result[name] = result[name].astype("string").str.strip().str.lower()
    unexpected = set(result["smoker"].unique()) - set(SMOKER_LABELS)
    if unexpected:
        raise ValueError(f"Unrecognized smoker values: {sorted(unexpected)}")
    return result


def filter_insurance_data(
    frame: pd.DataFrame,
    age_range: tuple[int, int],
    bmi_range: tuple[float, float],
    smoker_values: list[str],
    region_values: list[str],
) -> pd.DataFrame:
    """Apply all user-selected filters without modifying the cached input."""
    condition = (
        frame["age"].between(*age_range)
        & frame["bmi"].between(*bmi_range)
        & frame["smoker"].isin(smoker_values)
        & frame["region"].isin(region_values)
    )
    return frame.loc[condition].copy()


def region_summary(frame: pd.DataFrame, statistic: str) -> pd.DataFrame:
    """Prepare a region-level comparison from the currently filtered records."""
    if statistic not in ("Mean", "Median"):
        raise ValueError("statistic must be 'Mean' or 'Median'")
    agg = "mean" if statistic == "Mean" else "median"
    result = (
        frame.groupby("region", observed=True)["charges"]
        .agg(charge_value=agg, observations="size")
        .reset_index()
        .sort_values("charge_value", ascending=False)
    )
    result["region_label"] = result["region"].str.title()
    return result
